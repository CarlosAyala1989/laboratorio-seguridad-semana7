# Entrega — Laboratorio N.° 07: Análisis de Malware

El informe académico en Word se elaboró a partir de la plantilla proporcionada. La carpeta conserva además las versiones Markdown y HTML, los registros originales y los scripts para reproducir el análisis estático.

## Alcance ejecutado

- Se consultaron dos informes públicos de ANY.RUN y se incorporaron cuatro capturas reales.
- Se generaron y analizaron cinco muestras benignas, sin ejecutarlas ni cargarlas a servicios externos.
- Se calculó file, ExifTool, MD5, SHA-256, ssdeep y YARA localmente y en el contenedor oficial REMnux.
- REMnux se ejecutó sin red, con muestras y regla en solo lectura; sus hashes criptográficos coincidieron con el análisis local.
- VirusTotal recibió cinco consultas por SHA-256, separadas al menos 26 segundos; todas devolvieron HTTP 404, sin cargas de archivos.

## Archivos principales

- `07_informe/informe_laboratorio_07.docx`: informe académico solicitado.
- `07_informe/informe_laboratorio_07.md` y `.html`: versiones editables y visualizables.
- `07_informe/indice_evidencias.md`: inventario y procedencia de evidencias.
- `04_remnux/resultados_docker/`: salida original REMnux y comparación de hashes.
- `resultados_muestras.csv`, `resultados_virustotal.json` y `resultados_yara.txt`: tablas de resultados.
- `08_scripts/`: scripts empleados; el lanzador Windows requiere autorizaciones explícitas documentadas en `02_malwarebytes/preparacion_windows.md`.

El ZIP incluye este README y un manifiesto SHA-256 de sus archivos. No contiene el instalador de Malwarebytes, las carpetas compartidas para Windows ni imágenes de disco de la VM.
