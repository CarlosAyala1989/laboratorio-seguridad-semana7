# Índice de evidencias — Laboratorio N.° 07

Fecha de recopilación: 8 de octubre de 2026. Las capturas de ANY.RUN son capturas reales de páginas públicas consultadas en el navegador. Para los análisis de consola se preservan las salidas originales, comparaciones y metadatos de imagen Docker.

| N.° | Evidencia | Actividad y procedencia | Resultado que demuestra |
|---|---|---|---|
| Figura 1 | 06_evidencias/Figura_01_ANYRUN.png | Captura de la página pública ANY.RUN, reporte 04ad7687-3118-4123-adfd-9f85e5f7b2d3 | Encabezado, MD5, etiquetas, nota de rescate y primeros eventos asociados al caso Nemty |
| Figura 2 | 06_evidencias/Figura_02_ANYRUN.png | Captura de la página pública ANY.RUN, reporte 13ec2b18-1f69-49ed-a552-f5f8e2eacc9f | Identificación del caso papers.eml, su MD5 y vista inicial de Outlook, WinRAR y WScript |
| Figura 3 | 06_evidencias/Figura_03_ANYRUN_procesos.png | Captura desplazada del mismo reporte público | Vista de procesos y seguimiento de la cadena asociada al archivo JavaScript |
| Figura 4 | 06_evidencias/Figura_04_FILEASSASSIN_no_disponible.png | Captura del navegador al consultar la ruta oficial histórica de FileASSASSIN | La página de descargas devolvió “Invalid request”; no se descargó ni ejecutó un programa |
| E-04 | 01_diagnostico/diagnostico_entorno.txt | Salida del script diagnosticar_entorno.py | Distribución, kernel, CPU, memoria, espacio, Docker, VirtualBox y disponibilidad de herramientas |
| E-05 | 01_diagnostico/diagnostico_entorno.json | Registro JSON del diagnóstico | Datos de sistema y resultados de comandos en formato estructurado |
| E-06 | 04_remnux/muestras/ | Cinco archivos benignos generados localmente | Muestras TXT, JSON, CSV, ZIP y texto de script inerte; ninguna fue ejecutada |
| E-07 | 04_remnux/metadatos/ y 04_remnux/resultados_docker/ejecucion_remnux.log | Salidas originales de `file` y ExifTool en Ubuntu y REMnux | Tipos reconocidos y metadatos disponibles para cada muestra |
| E-08 | 04_remnux/hashes/ y 04_remnux/resultados_docker/verificacion_hashes_remnux.csv | Hashes locales y comparación de salida REMnux | Cinco MD5 y SHA-256 reproducidos; huellas ssdeep conservadas con advertencia de tamaño |
| E-09 | resultados_muestras.csv | Consolidación del análisis estático y resultados YARA | Metadatos, tamaño, hashes, validación de formato, consultas VT y resultados YARA por muestra |
| E-10 | resultados_virustotal.json | Respuestas de cinco consultas GET a la API v3 por SHA-256 | Cinco respuestas HTTP 404; no se cargaron archivos |
| E-11 | 05_yara/reglas/reglas_laboratorio.yar | Reglas fuente redactadas para la práctica | Dos patrones de demostración benigna |
| E-12 | 05_yara/resultados/ y resultados_yara.txt | Salidas de ejecutar_yara.py y repetición dentro de REMnux | Dos coincidencias controladas y tres resultados sin coincidencia |
| E-13 | 04_remnux/resultados_docker/README.md y 09_registros/remnux_docker_image.json | Metadatos y configuración de la ejecución en Docker | Digest oficial, arquitectura, tamaño de imagen, montajes en solo lectura y retirada posterior de la caché |
| E-14 | 02_malwarebytes/preparacion_windows.md | Registro de preparación y consulta de fuentes oficiales | Instalador oficial descargado; VM no iniciada por autorización de licencia pendiente; estado de FileASSASSIN |
| E-15 | 08_scripts/ | Scripts de diagnóstico, análisis, consulta, REMnux, VM Windows e informe | Procedimientos reproducibles y configuración de los montajes y el aislamiento |

## Notas de procedencia

- Los reportes de ANY.RUN son datos de sandbox remota publicados por terceros. No son evidencia de ejecución en Ubuntu ni de actividad en el equipo del laboratorio.
- Los cinco archivos fueron creados localmente para el ejercicio. La ausencia de reporte en VirusTotal se registra literalmente y no como veredicto de seguridad.
- Las cuatro capturas gráficas documentan páginas consultadas en el navegador; no se presenta como captura ninguna salida de terminal. REMnux se acredita con su registro original, el CSV de verificación y los metadatos de imagen.
- La VM de Windows y el instalador de Malwarebytes se prepararon, pero no se iniciaron ni ejecutaron; no existen capturas ni resultados de escaneo.
- El archivo independiente image.png citado en el prompt maestro no estaba entre los materiales localizados. No se le atribuye contenido.
