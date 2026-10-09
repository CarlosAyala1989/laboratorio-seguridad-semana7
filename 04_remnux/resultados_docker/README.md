# Ejecución con REMnux en Docker

- Imagen oficial: `remnux/remnux-distro:noble`
- Digest verificado: `remnux/remnux-distro@sha256:792b5ddc51074c87af4d19e868d29fa179dcd616f13846290dfaac3dd7db6b56`
- Arquitectura: `amd64`
- Tamaño local reportado por Docker: 18,796,300,564 bytes (18.8 GB).
- Las cinco muestras y la regla YARA se montaron en solo lectura.
- La ejecución usó `--network none`; no descargó ni ejecutó malware y no hizo consultas externas.
- Las huellas MD5 y SHA-256 generadas dentro del contenedor coinciden, una a una, con los valores calculados previamente.
- YARA encontró las dos marcas didácticas controladas en M01 y M02; M03–M05 no coincidieron.
- ExifTool 13.59, `file` 5.45, ssdeep 2.14.1 y YARA 4.5.0 quedaron registrados en la salida completa.
- ssdeep emitió una advertencia de tamaño insuficiente para varias muestras; las huellas difusas se conservan, pero no se interpretan como comparaciones significativas.

## Archivos

- `ejecucion_remnux.log`: transcripción completa de herramientas y resultados.
- `verificacion_hashes_remnux.csv`: comparación con el análisis previo y resultados YARA por muestra.
- Lanzador reproducible: `08_scripts/ejecutar_remnux_docker.sh`.
- Script ejecutado dentro del contenedor: `08_scripts/procesar_muestras_remnux.sh`.
