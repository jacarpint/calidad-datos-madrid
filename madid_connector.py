import json
import re
import traceback
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

import requests
from frictionless import FrictionlessException, describe, validate
from pydantic import BaseModel

from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest
from metadata.generated.schema.api.data.createDatabaseSchema import CreateDatabaseSchemaRequest
from metadata.generated.schema.api.data.createTable import CreateTableRequest
from metadata.generated.schema.api.domains.createDomain import CreateDomainRequest
from metadata.generated.schema.api.tests.createTestCase import CreateTestCaseRequest
from metadata.generated.schema.api.tests.createTestDefinition import \
    CreateTestDefinitionRequest
from metadata.generated.schema.entity.data.databaseSchema import DatabaseSchema
from metadata.generated.schema.entity.data.table import Column, DataType
from metadata.generated.schema.metadataIngestion.workflow import \
    Source as WorkflowSource
# MODIFICACIÓN: Se añade la importación de TestResultValue
from metadata.generated.schema.tests.basic import (TestCaseResult,
                                                    TestCaseStatus, TestResultValue)
from metadata.generated.schema.tests.testCase import TestCase
from metadata.generated.schema.tests.testDefinition import \
    TestDefinition, TestPlatform
from metadata.generated.schema.type.entityReference import EntityReference
from metadata.ingestion.api.models import Either, StackTraceError
from metadata.ingestion.api.steps import Source
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.utils.logger import ingestion_logger

logger = ingestion_logger()


class MadridOpenDataConfig(BaseModel):
    """Configuration for Madrid Open Data Connector"""
    catalog_url: str = "https://datos.madrid.es/egob/catalogo.json"
    max_datasets: Optional[int] = None
    tabular_formats: List[str] = ['.csv', '.xlsx', '.xls', '.json', '.tsv']
    validate_data: bool = True

    class Config:
        extra = "forbid"


class MadridOpenDataConnector(Source):
    """Custom Connector for Madrid Open Data Portal"""

    def __init__(self, config: WorkflowSource, metadata: OpenMetadata):
        super().__init__()
        self.config = config
        self.metadata = metadata
        self.service_connection = config.serviceConnection.root.config
        
        config_dict = {}
        if hasattr(self.service_connection, 'configSource') and self.service_connection.configSource:
            config_dict.update(self.service_connection.configSource.__dict__)
        if hasattr(self.service_connection, 'connectionArguments') and self.service_connection.connectionArguments:
            config_dict.update(self.service_connection.connectionArguments)
            
        self.madrid_config = MadridOpenDataConfig.parse_obj(config_dict)
        self.database_name = "madrid_open_data_portal"
        self._catalog_data_cache = None
        self.frictionless_test_definition = None 
        logger.info(f"Madrid Open Data Connector initialized with config: {self.madrid_config}")
    
    def _get_or_create_frictionless_test_definition(self) -> TestDefinition:
        """
        Crea o recupera una TestDefinition genérica para las validaciones de Frictionless.
        """
        definition_name = "frictionlessCustomValidation"
        logger.info(f"Getting or creating Test Definition: {definition_name}")
        
        existing_definition = self.metadata.get_by_name(
            entity=TestDefinition,
            fqn=definition_name
        )
        if existing_definition:
            logger.info(f"Test Definition '{definition_name}' already exists.")
            return existing_definition

        logger.info(f"Creating Test Definition '{definition_name}'...")
        test_definition_request = CreateTestDefinitionRequest(
            name=definition_name,
            displayName="Frictionless Data Validation",
            description="A custom test to store the results of a Frictionless Data validation report.",
            entityType="TABLE",
            testPlatforms=[TestPlatform.OpenMetadata],
            parameterDefinition=[]
        )
        
        created_definition = self.metadata.create_or_update(
            data=test_definition_request
        )
        logger.info(f"Test Definition '{definition_name}' created successfully.")
        return created_definition


    def prepare(self):
        logger.info("Preparing Madrid Open Data Connector...")
        try:
            response = requests.get(self.madrid_config.catalog_url, timeout=300)
            response.raise_for_status()
            logger.info("Successfully connected to Madrid Open Data API")
        except Exception as e:
            logger.error(f"Failed to connect to Madrid Open Data API: {e}")
            raise

    def _iter(self, *args, **kwargs) -> Iterable[Either]:
        try:
            logger.info("Starting Madrid Open Data ingestion...")
            
            if self.madrid_config.validate_data:
                self.frictionless_test_definition = self._get_or_create_frictionless_test_definition()

            yield from self.yield_database(self.database_name)
            
            datasets = self._fetch_catalog_data()
            if not datasets:
                 logger.warning("No datasets found to process.")
                 return

            for i, dataset in enumerate(datasets):
                if not isinstance(dataset, dict):
                    continue
                dataset_title_str = dataset.get('title', f'unknown_dataset_{i}')
                
                try:
                    schema_name = self._clean_name(dataset_title_str)
                    schema_fqn = f"{self.config.serviceName}.{self.database_name}.{schema_name}"
                    
                    existing_schema = self.metadata.get_by_name(
                        entity=DatabaseSchema,
                        fqn=schema_fqn,
                    )
                    
                    if existing_schema and existing_schema.domain:
                        logger.info(f"Skipping dataset '{dataset_title_str}' as it already exists with an assigned domain.")
                        continue
                        
                except requests.exceptions.HTTPError as http_error:
                    if http_error.response.status_code != 404:
                        logger.warning(f"Error checking for existing schema '{schema_fqn}': {http_error}. Ingestion will proceed.")
                except Exception as e:
                    logger.warning(f"Unexpected error while checking schema '{schema_fqn}': {e}. Ingestion will proceed.")

                logger.info(f"Processing dataset {i+1}/{len(datasets)}: {dataset_title_str}")
                
                yield from self.yield_database_schema(dataset)
                
                distributions = dataset.get('distribution', [])
                if not isinstance(distributions, list):
                    distributions = [distributions]

                for dist in distributions:
                    if not isinstance(dist, dict):
                        continue
                    if self._is_tabular_format(dist.get('accessURL', '')):
                        yield from self.yield_table(dist, dataset)
            
            logger.info("Madrid Open Data ingestion completed successfully")
        except Exception as e:
            logger.error(f"Error during ingestion: {e}")
            yield Either(left=self._get_stack_trace_error(e))

    @classmethod
    def create(cls, config_dict: dict, metadata: OpenMetadata, pipeline_name: Optional[str] = None) -> "MadridOpenDataConnector":
        config = WorkflowSource.parse_obj(config_dict)
        return cls(config, metadata)

    def get_database_names(self) -> Iterable[str]:
        yield self.database_name

    def get_database_schema_names(self) -> Iterable[str]:
        try:
            for dataset in self._fetch_catalog_data():
                if isinstance(dataset, dict):
                    yield self._clean_name(dataset.get('title', 'unknown_dataset'))
        except Exception as e:
            logger.error(f"Error fetching schema names: {e}")

    def get_tables_name_and_type(self) -> Iterable[tuple]:
        try:
            for dataset in self._fetch_catalog_data():
                if not isinstance(dataset, dict):
                    continue
                distributions = dataset.get('distribution', [])
                if not isinstance(distributions, list):
                    distributions = [distributions]
                
                for dist in distributions:
                    if not isinstance(dist, dict):
                        continue
                    if self._is_tabular_format(dist.get('accessURL')):
                        yield (self._clean_name(dist.get('title', 'unknown_distribution')), "Regular")
        except Exception as e:
            logger.error(f"Error fetching table names: {e}")

    def yield_database(self, database_name: str) -> Iterable[Either]:
        try:
            yield Either(right=CreateDatabaseRequest(
                name=database_name,
                displayName="Madrid Open Data Portal",
                description="Catálogo de datos abiertos del Ayuntamiento de Madrid",
                service=self.config.serviceName
            ))
        except Exception as e:
            yield Either(left=self._get_stack_trace_error(e))

    def yield_database_schema(self, dataset_info: dict) -> Iterable[Either]:
        try:
            schema_name = self._clean_name(dataset_info.get('title', 'unknown_dataset'))
            description_list = dataset_info.get('description', [])
            description = description_list[0].get('value', '') if isinstance(description_list, list) and description_list else dataset_info.get('description', '')

            domain_name = None
            schema_field = dataset_info.get('schema') or dataset_info.get('theme')
            if schema_field:
                if isinstance(schema_field, str):
                    domain_name = self._clean_name(schema_field.split('/')[-1])
                else:
                    domain_name = self._clean_name(str(schema_field))
                yield from self.yield_domain(domain_name, schema_field)

            yield Either(right=CreateDatabaseSchemaRequest(
                name=schema_name,
                displayName=dataset_info.get('title', schema_name),
                description=str(description),
                database=f"{self.config.serviceName}.{self.database_name}",
                domain=domain_name
            ))
        except Exception as e:
            yield Either(left=self._get_stack_trace_error(e))


    def yield_domain(self, domain_name: str, schema_field: str) -> Iterable[Either]:
        try:
            yield Either(right=CreateDomainRequest(
                name=domain_name,
                displayName=domain_name.replace('_', ' ').title(),
                description=f"Dominio creado a partir del campo schema/theme: {schema_field}",
                domainType="Source-aligned" 
            ))
        except Exception as e:
            yield Either(left=self._get_stack_trace_error(e))

    # ===================================================================================
    # MÉTODO `yield_table` COMPLETAMENTE MODIFICADO
    # ===================================================================================

    def yield_table(self, distribution_info: dict, dataset_info: dict) -> Iterable[Either]:
        try:
            table_name = self._clean_name(distribution_info.get('title', 'unknown_distribution'))
            access_url = distribution_info.get('accessURL')
            schema_name = self._clean_name(dataset_info.get('title', 'unknown_dataset'))
            table_fqn = f"{self.config.serviceName}.{self.database_name}.{schema_name}.{table_name}"

            columns = self._get_table_columns(access_url) if access_url else []
            if not columns:
                columns = [Column(name="data", dataType=DataType.STRING, description="Data from file")]

            # --- Lógica de validación y reporte ---
            custom_properties = {}
            # NUEVO: Inicialización explícita de las variables del resultado del test
            test_case_status = TestCaseStatus.Aborted
            result_message = '{"message": "Validation was not executed."}'
            markdown_report = "# Frictionless Validation Report\n\n**Status:** Aborted"
            test_result_values = []
            
            if self.madrid_config.validate_data and access_url:
                logger.info(f"Running Frictionless validation for {access_url}")
                try:
                    report = validate(access_url)
                    report_dict = report.to_dict()
                    stats = report_dict.get('stats', {})
                    
                    # NUEVO: Logging para depuración. Esto nos ayudará a ver si `report.valid` es correcto.
                    logger.info(f"Frictionless report for '{table_name}': valid={report.valid}, errors={stats.get('errors', 0)}")
                    
                    # Prepara las métricas para testResultValue
                    test_result_values.append(TestResultValue(name="errors", value=str(stats.get('errors', 0))))
                    test_result_values.append(TestResultValue(name="seconds", value=str(round(stats.get('seconds', 0), 2))))

                    # Prepara el reporte Markdown para la custom property (sin cambios)
                    markdown_report = f"# Frictionless Validation Report\n\n"
                    markdown_report += f"**URL:** {access_url}\n"
                    markdown_report += f"**Validation Result:** `{'Valid' if report.valid else 'Invalid'}`\n\n"
                    markdown_report += f"## Stats\n"
                    markdown_report += f"- Errors: `{stats.get('errors', 0)}`\n"
                    markdown_report += f"- Seconds: `{round(stats.get('seconds', 0), 2)}`\n\n"

                    # NUEVO: Lógica de estado y resultado reestructurada para mayor claridad
                    if report.valid:
                        test_case_status = TestCaseStatus.Success
                        result_message_dict = {
                            "status": "Success",
                            "message": "Frictionless validation passed successfully."
                        }
                        result_message = json.dumps(result_message_dict)

                    else: # Si report.valid es False
                        test_case_status = TestCaseStatus.Failed
                        errors = report_dict.get('tasks', [{}])[0].get('errors', [])
                        
                        # Mensaje de resultado para la UI de OpenMetadata (estructurado como JSON)
                        if errors:
                            first_error = errors[0]
                            result_message_dict = {
                                "status": "Failed",
                                "error_count": len(errors),
                                "first_error_code": first_error.get('code', 'N/A'),
                                "first_error_row": first_error.get('rowNumber', 'N/A'),
                                "first_error_message": first_error.get('message', 'No message')
                            }
                        else:
                            result_message_dict = {
                                "status": "Failed",
                                "message": "Validation failed with an unknown error."
                            }
                        result_message = json.dumps(result_message_dict, ensure_ascii=False)
                        
                        # Añade los errores al reporte Markdown
                        markdown_report += "## Validation Errors\n\n"
                        markdown_report += "```json\n"
                        markdown_report += json.dumps(errors, indent=2, ensure_ascii=False)
                        markdown_report += "\n```"
                        # NUEVO: Log corregido para ser más claro
                        logger.warning(f"Frictionless validation failed for table '{table_name}' (URL: {access_url})")

                except FrictionlessException as fe:
                    test_case_status = TestCaseStatus.Aborted
                    result_message = json.dumps({"status": "Aborted", "error": f"FrictionlessException: {fe}"})
                    markdown_report = f"# Frictionless Validation Report\n\n**Error:** Validation could not be completed.\n\n```\n{str(fe)}\n```"
                    logger.warning(f"Frictionless validation aborted for {access_url}: {fe}")
                except Exception as e:
                    test_case_status = TestCaseStatus.Aborted
                    result_message = json.dumps({"status": "Aborted", "error": f"Unexpected error: {e}"})
                    markdown_report = f"# Frictionless Validation Report\n\n**Error:** An unexpected error occurred.\n\n```\n{traceback.format_exc()}\n```"
                    logger.error(f"Unexpected validation error for {access_url}: {e}")
            
            custom_properties["schemaValidation"] = markdown_report

            # --- Creación de la tabla ---
            create_table_request = CreateTableRequest(
                name=table_name,
                displayName=distribution_info.get('title', table_name),
                description=f"Format: {distribution_info.get('format', {}).get('value')}. URL: {access_url}",
                columns=columns,
                databaseSchema=f"{self.config.serviceName}.{self.database_name}.{schema_name}",
                tableType="Regular",
                extension=custom_properties
            )
            yield Either(right=create_table_request)

            # --- Creación del Test Case y envío de resultados ---
            if self.madrid_config.validate_data and access_url and self.frictionless_test_definition:
                try:
                    test_case_request = CreateTestCaseRequest(
                        name="frictionless_data_validation",
                        displayName="Frictionless Data Validation",
                        entityLink=f"<#E::table::{table_fqn}>",
                        testDefinition=self.frictionless_test_definition.fullyQualifiedName.root,
                        description="Validates the data file using the Frictionless Data standard.",
                        parameterValues=[]
                    )
                    created_test_case = self.metadata.create_or_update(data=test_case_request)

                    test_result = TestCaseResult(
                        timestamp=int(datetime.now().timestamp() * 1000),
                        testCaseStatus=test_case_status,
                        result=result_message,
                        testResultValue=test_result_values
                    )
                    
                    # NUEVO: Logging justo antes de enviar los resultados para máxima claridad en la depuración
                    logger.info(
                        f"Adding test case result for '{created_test_case.fullyQualifiedName.root}': "
                        f"Status='{test_case_status.value}', Result='{result_message}'"
                    )
                    
                    self.metadata.add_test_case_results(
                        test_results=test_result,
                        test_case_fqn=created_test_case.fullyQualifiedName.root
                    )
                    logger.info(f"Successfully added test case results for {table_fqn}")

                except Exception as e:
                    logger.warning(f"Failed to add test case for table {table_fqn}. Reason: {e}")
                    logger.warning(traceback.format_exc())

        except Exception as e:
            yield Either(left=self._get_stack_trace_error(e))
            

    def _fetch_catalog_data(self) -> List[Dict[str, Any]]:
        if self._catalog_data_cache is not None:
            return self._catalog_data_cache

        logger.info(f"Fetching catalog from: {self.madrid_config.catalog_url}")
        try:
            response = requests.get(self.madrid_config.catalog_url, timeout=300)
            response.raise_for_status()
            
            data = self._safe_json_parse(response.text)
            datasets = data.get('result', {}).get('items', [])
            
            if self.madrid_config.max_datasets:
                datasets = datasets[:self.madrid_config.max_datasets]
            
            logger.info(f"Successfully fetched and parsed {len(datasets)} datasets")
            self._catalog_data_cache = datasets
            return datasets
        except Exception as e:
            logger.error(f"Fatal error fetching or parsing catalog data: {e}")
            self._catalog_data_cache = []
            raise

    def _safe_json_parse(self, json_text: str) -> Dict[str, Any]:
        try:
            return json.loads(json_text)
        except json.JSONDecodeError:
            logger.warning("Initial JSON decoding failed. Attempting to fix...")
            fixed_text = json_text
            try:
                fixed_text = re.sub(r'}\s*{', '},{', fixed_text, flags=re.DOTALL)
                fixed_text = self._fix_malformed_title_field(fixed_text)
                result = json.loads(fixed_text)
                logger.info("Successfully parsed JSON after fixes.")
                return result
            except Exception as final_error:
                logger.error(f"All JSON fixing attempts failed. Final error: {final_error}")
                raise final_error

    def _fix_malformed_title_field(self, json_text: str) -> str:
        pattern = re.compile(r'("title"\s*:\s*)(.*?)(?=,\s*"\w+"\s*:|})', re.DOTALL)
        def replacer(match):
            prefix, value = match.group(1), match.group(2).strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            fixed_value_content = value.replace('"', '\\"')
            return f'{prefix}"{fixed_value_content}"'
        return pattern.sub(replacer, json_text)

    def _get_table_columns(self, access_url: str) -> List[Column]:
        try:
            logger.info(f"Analyzing schema for: {access_url}")
            resource = describe(source=access_url)
            columns = []
            if hasattr(resource, 'schema') and hasattr(resource.schema, 'fields'):
                for i, field in enumerate(resource.schema.fields):
                    cleaned_name = self._clean_name(field.name)
                    
                    if not cleaned_name or cleaned_name == "_":
                        final_name = f"unnamed_column_{i+1}"
                        logger.warning(f"Original column name '{field.name}' was empty or invalid. Renaming to '{final_name}'.")
                    else:
                        final_name = cleaned_name

                    om_type = self._map_frictionless_type(field.type)
                    columns.append(Column(
                        name=final_name,
                        dataType=om_type,
                        description=field.description or f"Original name: '{field.name}', Frictionless type: {field.type}"
                    ))
            logger.info(f"Successfully extracted {len(columns)} columns from {access_url}")
            return columns
        except Exception as e:
            logger.warning(f"Could not analyze schema for {access_url}: {e}")
            return []

    def _map_frictionless_type(self, f_type: str) -> DataType:
        return {
            'string': DataType.STRING, 'number': DataType.DOUBLE,
            'integer': DataType.INT, 'boolean': DataType.BOOLEAN,
            'date': DataType.DATE, 'datetime': DataType.DATETIME,
            'time': DataType.TIME, 'array': DataType.ARRAY, 'object': DataType.JSON,
        }.get(f_type, DataType.STRING)

    def _is_tabular_format(self, url: Optional[str]) -> bool:
        if not url:
            return False
        return any(url.lower().endswith(ext) for ext in self.madrid_config.tabular_formats)

    def _clean_name(self, name: str) -> str:
        if not name:
            return "unnamed"
        cleaned = re.sub(r'[^\w\s-]', '', name.strip())
        cleaned = re.sub(r'[-\s]+', '_', cleaned).lower()
        return f"_{cleaned}" if cleaned and not (cleaned[0].isalpha() or cleaned[0] == '_') else cleaned or "unnamed"

    def _get_stack_trace_error(self, exc: Exception) -> StackTraceError:
        return StackTraceError(
            name=type(exc).__name__, error=f"Error in Madrid Open Data Connector: {exc}",
            stackTrace=traceback.format_exc()
        )

    def close(self):
        pass

    def test_connection(self) -> None:
        self.prepare()
