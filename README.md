# Descubrimiento, Observabilidad y Gobernanza Inteligente de Datos Abiertos del Ayuntamiento de Madrid. 

Premios a la reutilización de datos abiertos del Ayuntamiento de Madrid.  Propuestas de mejora de la calidad del Portal de Datos Abiertos


## Introducción y Objetivos Principales: De la publicación de datos a la generación de valor

El Portal de Datos Abiertos del Ayuntamiento de Madrid es ya una referencia nacional por volumen y diversidad de datos, pero aún se percibe principalmente como un repositorio de ficheros abiertos. La propuesta plantea un salto cualitativo del mismo: convertirlo en un ecosistema de datos gobernado, fiable y de alto valor, que impulse servicios innovadores, refuerce la transparencia y genere impacto económico y social real.

La propuesta implementa una plataforma de gobernanza inteligente que automatiza y mejora la descripción técnica, la validación de calidad y el descubrimiento de los conjuntos de datos. A través de la aplicación de tecnologías y herramientas como OpenMetadata y Frictionless Data, conseguimos tomar consciencia de parte de los problemas recurrentes que hoy limitan el aprovechamiento de los datos públicos: la dificultad
para evaluar su fiabilidad, la falta de documentación estructural y las diferentes barreras técnicas que se deben superar para poder utilizarlos. Actualmente, un ciudadano o periodista debe invertir esfuerzos
manuales en limpiar y verificar datasets con errores antes de poder utilizarlos. Con esta propuesta, el portal podrá ofrecer informes de calidad accesibles, así como un buscador en lenguaje natural que elimina esa fricción durante el descubrimiento de datos. Esto multiplica el número de beneficiarios potenciales al ampliar el acceso más allá de perfiles especializados, maximizando la utilidad social de los datos.

El objetivo final es claro: maximizar la transparencia, fomentar la confianza en la información pública y catalizar la creación de nuevos servicios de valor basados en datos. El portal datos.gob.es define la calidad del producto de datos como el grado en que estos satisfacen las siguientes 15 características.

Este proyecto nace con la intención de dar un paso más allá en la explotación de los datos abiertos, dotando al portal de capacidades de descubrimiento, observabilidad y gobernanza, y que permitiría al Ayuntamiento avanzar en la adopción de especificaciones como las UNE de gobierno, gestión y calidad del dato (0077, 0078, 0079 y 0080) o la familia de normas ISO 25000 y que permita atajar o minimizar algunos de los problemas más recurrentes de calidad en los datos abiertos.


## El problema actual: El potencial frenado por la calidad del dato

Un análisis preliminar del catálogo de datos abiertos del Ayuntamiento, si bien evidencia su riqueza, también saca a la luz una serie de fricciones técnicas que dificultan su uso práctico. Estos problemas, a menudo invisibles para el usuario medio, suponen una barrera significativa para la reutilización automatizada de la información de manera sencilla.

Se han detectado problemas que van desde errores estructurales en los datasets, catálogo de datos con errores de sintaxis por el uso indebido de comillas sin escapar, URIs de recursos que no son válidas al
contener espacios y caracteres especiales, etc. A un nivel más granular, es frecuente encontrar inconsistencias en los propios datasets, tales como la ausencia de cabeceras, columnas enteramente vacías, desalineaciones entre el número de columnas y sus cabeceras, o tipos de datos incoherentes.

Más adelante en esta memoria se enumeran con algo más de detalle algunos de estos errores simplemente a modo ilustrativo, si bien esta propuesta no pretende centrarse en errores concretos y persigue un enfoque
más holístico y sistémico. Aunque subsanables, cada uno de estos errores transfiere al desarrollador, ciudadano, periodista o empresa el coste de la calidad del dato, su limpieza y normalización, e impiden un
procesamiento automático fiable. Este esfuerzo extra desincentiva el uso, frena la innovación y erosiona la confianza en la información pública.

## La solución: una plataforma de Gobernanza Automatizada y Proactiva

Para resolver estos retos de manera sistémica, se ha diseñado y prototipado una solución que introduce una capa de inteligencia y control adicional sobre el catálogo de datos. La solución se articula en torno a varios componentes software trabajando de forma coordinada.

El corazón del sistema se basa en OpenMetadata, que actúa como un catálogo inteligente y un centro de control de calidad. Toda la metainformación enriquecida sobre los datasets y distribuciones se centraliza en esta potente plataforma de descubrimiento y gobernanza de datos. Los datos abiertos del Ayuntamiento se tratan como activos de primer nivel, permitiendo a los gestores tener una visión global de la salud del catálogo, asignar responsables, seguir la evolución de la calidad y definir reglas de negocio específicas.

La solución incluye numerosos conectores nativos para las principales herramientas de datos (actualmente, un total de 77 herramientas), incluyendo desde APIs, bases de datos, herramientas de mensajería, inteligencia de negocio (BI), herramientas de pipeline, modelos de Machine Learning u otros sistemas de gestión de metadatos o servicios de almacenamiento de objetos, entre otras categorías. No obstante, la
solución permite la implementación de conectores personalizados, para expandir las capacidades o dar soporte a nuevas herramientas o portales. En este sentido, se ha desarrollado un conector personalizado
que consume de forma automática el catálogo completo de datos.madrid.es y lo procesa siguiendo las necesidades concretas planteadas en este proyecto.

Este conector no solo extrae la información, sino que realiza un primer procesado para corregir errores estructurales del propio catálogo. Además, cada recurso es analizado por un motor de validación, basado en
el framework Frictionless Data, que funciona como un inspector automático que revisa la estructura y coherencia de cada fichero. Este motor infiere automáticamente el esquema de cada dataset (columnas, tipos de datos, etc.) y ejecuta una batería de validaciones que detectan inconsistencias generando un informe de calidad detallado para cada fichero. Frictionless es una herramienta desarrollada por la Open Knowledge Foundation, creadores de herramientas de gran relevancia en el ecosistema de datos abiertos como CKAN u Open Data Editor.

Para democratizar el acceso a la nueva metainformación generada, se propone un asistente conversacional en lenguaje natural, conectado a OpenMetadata mediante un servidor MCP. Cualquier ciudadano podrá localizar y consultar datasets mediante preguntas sencillas, eliminando barreras técnicas y permitiendo una utilización más sencilla de los datos disponibles.

La arquitectura propuesta funciona como un 'control de calidad' inteligente y automático. El conector extrae los datasets disponibles del portal y los valida empleando el motor de Frictionless Data, mientras que
OpenMetadata presenta toda la información de forma comprensible, y nos ofrece un servidor MCP de para proporcionar de manera sencilla un chatbot que facilita el acceso a cualquier ciudadano.


## Impacto y Beneficios Transversales

La implementación de esta plataforma genera un impacto positivo y medible en todos los actores del ecosistema de datos abiertos. La mejora en calidad y gobernanza abre oportunidades en sectores clave para
Madrid: aplicaciones de movilidad con datos de tráfico y transporte en tiempo real, empresas inmobiliarias que integran datos de urbanismo y equipamientos, o startups de sostenibilidad que reutilizan datos
medioambientales y energéticos. De este modo, el portal se convierte en un motor para la innovación y emprendimiento local. Al reducir la necesidad de preprocesar los datasets, se eliminan costes ocultos que a
día de hoy limitan la viabilidad de modelos de negocio basados en información pública.

Para la ciudadanía, periodistas y organizaciones sociales, el principal beneficio es la confianza y la accesibilidad. Al disponer de informes de calidad públicos para cada dataset y una forma de buscar
información en lenguaje natural, se reduce drásticamente la barrera técnica y se fortalece la transparencia y el control democrático.

Para los desarrolladores, emprendedores y el sector privado, la mejora de la calidad de los datos del portal es un acelerador de innovación. Al eliminar la limpieza manual de datos, se reducen drásticamente costes y tiempos de desarrollo, permitiendo aplicaciones y servicios más rápidos y robustos. Esto potencia la economía del dato y abre oportunidades de negocio basadas en la reutilización de información pública.
Finalmente, para el propio Ayuntamiento de Madrid, la solución ofrece una herramienta de gobernanza proactiva que proporciona una radiografía completa y en tiempo real de la salud de los activos de datos, permitiendo tomar decisiones estratégicas basadas en la calidad. Otorga una observabilidad completa sobre la calidad técnica del portal y los diferentes activos de datos, permitiendo priorizar esfuerzos de mejora y automatizar tareas de control que a día de hoy son inexistentes o manuales en la mayoría de casos.

Este sistema es una herramienta estratégica que refuerza la imagen de una administración moderna y transparente y permite tomar decisiones basadas en datos de calidad, optimizar recursos y posicionar a Madrid como un referente en gobierno digital y economía del dato.


## Innovación, Calidad Técnica y Grado de Desarrollo

La innovación de este proyecto reside en la adaptación de herramientas y metodologías de gobernanza de datos, tradicionalmente aplicadas al mundo empresarial, al dominio específico de los datos abiertos. No se
trata sólo de integrar tecnologías, sino de articularlas de tal forma que se genere un bucle de ingesta y validación automatizado. La solución se fundamenta en una arquitectura moderna, modular y basada íntegramente en componentes de código abierto (OpenMetadata, Apache Airflow, Elasticsearch, Frictionless, etc.), lo que garantiza su sostenibilidad e interoperabilidad, no incurriendo en costes de licencias o dependencia del proveedor (vendor lock-in) que a menudo llevan asociados este tipo de soluciones.

Se ha implementado y se dispone de un prototipo funcional operativo, que valida su viabilidad técnica más allá del diseño conceptual y que permite una rápida transición hacia pilotos productivos. Este prototipo
proporciona un entorno usable de testeo para comprobar en pruebas pilotos su utilidad en entornos reales.

Actualmente el prototipo está contenerizado mediante Docker y listo para su despliegue inmediato en un entorno de pruebas o preproducción en la infraestructura del Ayuntamiento, garantizando una posible
transición fluida hacia un piloto real. Actualmente el prototipo cuenta con OpenMetadata desplegado junto con el conector personalizado (custom connector). Dicho conector descarga el catálogo del portal, realiza un procesado del mismo e infiere para cada uno de los datasets el esquema (schema) en base a los datos que contiene y realiza una validación del dataset respecto al esquema inferido, todo ello empleando Frictionless.

Una vez realizadas estas operaciones, inserta los resultados en OpenMetadata para su explotación. Los resultados de la validación se ingestan en OpenMetadata como un test case y que muestra si el resultado
del test es satisfactorio, fallado o abortado. Además, todo el reporte completo de la validación se almacena en una custom property que puede ser visualizada desde el propio portal y ofrece información completa sobre el error concreto del dataset. Además, para los test fallados, desde la interfaz del sistema se puede asignar el incidente a un determinado usuario o grupo para su subsanación o seguimiento.

La herramienta también permite la definición de test de calidad más específicos para mejorar la observabilidad de los datasets. En este sentido, se pueden definir pruebas a nivel de tabla como que un determinado nombre de columna debe existir, el número de filas o número de columnas debe encontrarse entre un mínimo, máximo o igual a un determinado valor, o que la comparación entre dos tablas tiene menos
de un determinado número de filas de diferencia. Igualmente, se soporta la definición de test específicos a nivel de columna, en función del tipo definido para esa columna. A modo de ejemplo, para un campo de tipo numérico, los test pueden verificar si el valor se encuentra entre un máximo y mínimo, o si la media o mediana se encuentra entre unos determinados valores, o para campos tipo string si el texto sigue
determinadas expresiones regulares (regex), entre otros múltiples tests soportados.

Si bien los test a nivel de tablas y columnas se pueden definir actualmente en la interfaz, aún no ha sido implementada su ejecución en el conector personalizado, por lo que los únicos resultados que actualmente
están disponibles son los de la validación inicial mediante Frictionless durante la ingesta. 

Por último, se ha configurado un servidor MCP para la consulta de toda la metainformación contenida en el sistema empleando lenguaje natural por parte de los usuarios. En este sentido, se ha empleado Claude y el
modelo Sonnet 4 como modelo LLMs para la interacción con el sistema, obteniendo buenos resultados en las pruebas efectuadas. El sistema se puede personalizar fácilmente modificando elsystem prompt que permiten
que el estilo de la respuesta siga un determinado formato, o que el modelo del lenguaje tenga una determinada personalidad, entre otras funcionalidades. El sistema es compatible con cualquier proveedor que soporte el uso de MCPs.


## Una experiencia de uso para todoslos perfiles

La accesibilidad y la inclusión son pilares del diseño de la solución, por lo que se han definido experiencias de usuario diferenciadas y adaptadas a distintos perfiles, garantizando que tanto la ciudadanía como los responsables municipales puedan obtener el máximo valor de los datos abiertos. Aunque las experiencias están diferenciadas según el perfil, ambas se apoyan en el mismo sistema de metadatos de este modo que se proporciona en todo momento información actualizada y consistente para ambos grupos.

La ciudadanía y los consumidores de datos disfrutarán de una experiencia mucho más directa y sencilla, integrada en el propio portal de datos abiertos a través de un asistente conversacional en lenguaje natural. Esto elimina barreras técnicas y permite que cualquier persona, independientemente de su formación o conocimiento tecnológico, pueda descubrir y entender los datasets.

Así, por ejemplo, un usuario del portal puede hacer preguntas del tipo "¿Qué datasets hay sobre terrazas en el distrito Centro?", "¿Cuál es el estado de calidad de los datos de tráfico?" o “Muéstrame los recursos relacionados con calidad del aire en 2023”. El sistema analizará estas preguntas, consultará la base de conocimiento de OpenMetadata y ofrecerá respuestas directas y enlaces a los recursos más pertinentes, democratizando de forma efectiva el acceso a la información pública y mejorando el descubrimiento de los recursos abiertos publicados y disponibles.

La imagen muestra un ejemplo de interacción con el prototipo realizando una pregunta sobre los productos y precios de Mercamadrid. El sistema consulta la información disponible al respecto empleando para ello el
servidor MCP y responde en consecuencia, usando Claude Sonnet 4 como modelo de lenguaje.

Por otro lado, los usuarios corporativos del Ayuntamiento y los proveedores de datos interactúan principalmente directamente a través de la interfaz web de OpenMetadata, donde disponen de una visión integral y gobernada del catálogo completo. Podrán visualizar dashboards y paneles de observabilidad de la calidad, acceder al detalle de un dataset, visualizar su linaje y provenance, asignar responsables y propietarios a los datasets, definir reglas de validación, configurar alertas automáticas y hacer un seguimiento de la evolución de los activos de datos, entre otras funcionalidades.


## Variedad de conjuntos de datos soportados

Una de las fortalezas principales de este proyecto es su capacidad para adaptarse a una amplia gama de conjuntos de datos de manera nativa y sin necesidad de configuraciones específicas por recurso. De manera
concreta, actualmente el sistema, a través del uso de Frictionless, es compatible con datos tabulares en CSV o Excel, así como recursos JSON Además, el sistema es fácilmente expandible para soportar otro tipo de
ficheros entre los que destacan Google Sheets, Parquet, Pandas o SQL, entre otros, que actualmente no se han considerado para el prototipo, pero están disponibles en Frictionless como plugins. El sistema también
soporta ficheros ZIP comprimidos que contienen múltiples recursos, accediendo a los mismos y analizando de manera individualizada cada uno de ellos.

Se ha analizado el catálogo de datos del portal de datos abiertos de Madrid, extrayendo que está compuesto actualmente por un total de 646 datasets y 9710 distribuciones, las cuales se distribuyen de esta manera
según formato:

De esta manera, se estima que el sistema actualmente da soporte a aproximadamente un 83% del total de distribuciones existentes, convirtiéndo a la herramienta en una solución transversal que beneficia a gran
parte del ecosistema del portal. Si bien no se ha añadido en el prototipo desarrollado, el sistema está preparado para su expansión con otras herramientas como Fiona que permitiría describir ficheros
geográficos como SHP o servicios WMS/WFS, y dando soporte a la práctica totalidad de información procesable presente en el portal de datos abiertos.

Gracias a que el sistema extrae automáticamente el catálogo completo de datasets del portal de datos abiertos y ataca directamente los enlaces a los recursos contenidos en el catálogo, el sistema escala automáticamente dando cobertura a los nuevos recursos o modificaciones en los recursos existentes, sin requerir de intervención humana.


## Descripción de los principales problemaslocalizadas durante el desarrollo de la solución

Durante la fase de análisis y prototipado de la solución se han identificado algunas deficiencias tanto en el catálogo de datos abiertos como en los propios datasets, que dificultan la reutilización y justifican la necesidad de una solución de gobernanza automatizada. Se enumeran a continuación algunos de estos casos a modo únicamente ilustrativo, no pretendiendo ser una descripción exhaustiva o completa de los problemas existentes.

Para la extracción del catálogo completo de datos abiertos, inicialmente, se testeó el consumo del catálogo DCAT (Data Catalog Vocabulary) publicado (http://datos.madrid.es/egob/catalogo.dcat). Sin embargo, tras
un primer análisis del fichero, se detectó que el mismo no incluía la URL de acceso a las distribuciones, y contiene únicamente información a nivel de dataset. Lo mismo ocurre con el formato CSV (http://datos.madrid.es/egob/catalogo.csv). Pese a no estar documentado explícitamente en el portal de datos abiertos, se descubrió la existencia de este mismo catálogo en formato JSON (https://datos.madrid.es/egob/catalogo.json) y RDF (https://datos.madrid.es/egob/catalogo.rdf), que si que incluyen información sobre las distribuciones y las URL de acceso a los recursos.

Se han detectado otros problemas en el catálogo, que si bien son subsanables por los reutilizadores, recomendamos su adecuación. El catálogo incluye URIs no válidas, que incluyen espacios u otros caracteres
especiales como tildes. El siguiente ejemplo incluye ambas casuísticas:

Por otro lado, algunos títulos y textos incluyen comillas y caracteres que eventualmente pueden provocar problemas inesperados o invalidar la estructura del documento y hacerlo inaccesible sin un preprocesado
previo. De esta forma, encontramos, por ejemplo, que el catálogo en formato JSON no es un documento JSON válido, donde el problema principal radica en el uso de comillas dentro de títulos:

Este patrón de la inclusión de caracteres especiales y comillas sin escapar se repite habitualmente a lo largo de todo el portal, por lo que se recomienda sanitizar estos elementos de cara a facilitar el trabajo de los reutilizadores.

Igualmente, gracias al sistema desarrollado se han detectado numerosos datasets con errores estructurales frecuentes como ausencia de cabeceras, cabeceras duplicadas, columnas de datos vacías, desalineación
entre columnas y cabeceras, tipos de datos incoherentes, entre otros. A modo de ejemplo, el siguiente dataset “cuadro de clasificación” en formato CSV (https://datos.madrid.es/egob/catalogo/300737-0-archivos-cuadro-clasificación.csv) incluye numerosas columnas (primera linea) sin título en la cabecera (a partir de “NIVEL 4 (SERIE)” y “TIPOS DOCUMENTALES”), y las filas incluyen numerosas columnas sin información.

Otro escenario habitual es la presencia de filas vacías, así como la inclusión de información dentro de los archivos que hace que el fichero presente un formato no válido. Observamos en el siguiente dataset de
ejemplo (https://datos.madrid.es/egobfiles/MANUAL/300597/vehiculos_samur_pc.csv) como se incluyen ambas casuisticas. Cabe remarcar, además de la presencia de numerosas filas vacías, la inclusión al final del
archivo de la cadena de texto “Página 1 de 1”, que rompe la estructura del archivo CSV:

Lo anterior únicamente tiene como propósito remarcar algunos ejemplos de puntos de mejora que tienen los datasets del portal de datos abiertos publicados, si bien con el análisis inicial, centrado meramente en
examinar la estructura y el esquema de la información ha detectado un amplio catálogo de tipologías de problemas o puntos de mejora de los datasets, y que podría complementarse con otros checks de calidad más
específicos a nivel de filas o columnas.

Estos problemas, aunque en su mayoría subsanables, obliga a los reutilizadores en la mayoría de los casos a realizar tareas manuales o programáticas de limpieza y normalización, que provocan un mayor coste de
desarrollo de soluciones y desincentivando el uso, y representan una barrera para la reutilización de los datos públicos que deberían ser subsanados para mejorar la calidad general del portal de datos abiertos de Madrid.


### Del prototipo al impacto real

El prototipo desarrollado ya ha validado la viabilidad técnica de la solución por lo que se plantea en una siguiente fase escalar a un piloto productivo, integrando el sistema dentro del flujo de trabajo normal del equipo responsable del portal de datos abiertos, de cara a demostrar el valor en casos de uso reales. También se prevé en evoluciones posteriores del prototipo ampliar el desarrollo del conector para dar
soporte integral a formatos geográficos como SHP o WMS/WFS, abarcando un mayor porcentaje de ficheros del ecosistema de datos abiertos del Ayuntamiento. Esto permitirá incluir datasets con información
geográfica y de alto valor en ámbitos clave en la ciudad de Madrid como la movilidad, medio ambiente y urbanismo.

Uno de los principales limitantes actuales de este prototipo es la existencia de una única fuente aportando metainformación al sistema, esto es, el propio portal de datos abiertos de Madrid. Se asume que los datasets del portal en su mayoría serán el resultado de un procesado de datos provenientes de otros sistemas de información, lo cual actualmente no se refleja en la herramienta. Idealmente, el proyecto podría expandirse con la integración de herramientas existentes en el ecosistema de datos del Ayuntamiento de Madrid (bases de datos, APIs, herramientas de visualización..). Esto permitiría tener una visión holística del linaje o provenance de la información, esto es, el origen y las dependencias de cualquier activo de datos, y tener control sobre las implicaciones que el cambio o indisponibilidad de un determinado recurso de datos tiene sobre otros recursos que dependen de él.


### Despliegue

Situado en la raiz, ejecutar  ```docker build -t open-metadata-madrid-connector .``` para compilar el contenedor docker del contenedor.

Una vez creado, podemos acceder al directorio ```docker``` y realizar ```docker-compose up -d```


