# Usa la imagen base de la versión correcta de OpenMetadata
FROM openmetadata/ingestion:1.8.8

# El directorio de trabajo ya está configurado en la imagen base
WORKDIR /opt/airflow

# Cambiamos al usuario 'airflow' para mantener la consistencia
USER airflow

# Copia tu código y el archivo de configuración del paquete
COPY ./connector /opt/airflow/connector
COPY setup.py /opt/airflow/setup.py

# Instala tu conector personalizado
RUN pip install requests frictionless frictionless[excel] pydantic
RUN pip install .
