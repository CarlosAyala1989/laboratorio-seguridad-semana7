# Resumen de ejecución — Laboratorio N.° 07

## Actividades completadas

- Diagnóstico del sistema Ubuntu 24.04.5 LTS, arquitectura x86-64, kernel, procesador, memoria, espacio libre, Docker y VirtualBox.
- Preparación local de ExifTool 12.76, ssdeep 2.14.1 y YARA/yarac 4.5.0 en el directorio de trabajo.
- Creación y análisis de cinco muestras benignas TXT, JSON, CSV, ZIP y texto de script inerte.
- Extracción de tipos y metadatos, cálculo de MD5, SHA-256 y ssdeep, y contraste de MD5/SHA-256 con hashlib.
- Ejecución repetida del análisis estático en REMnux Docker oficial: `file`, ExifTool, `md5sum`, `sha256sum`, ssdeep y YARA. El contenedor usó `--network none` y recibió las muestras y la regla en solo lectura.
- Confirmación de que los cinco MD5 y los cinco SHA-256 coinciden entre el análisis local y REMnux. YARA repitió dos coincidencias didácticas en M01/M02 y no detectó patrones en M03–M05.
- Cinco consultas GET de VirusTotal por SHA-256, separadas por al menos 26 segundos. No se subieron archivos. Las cinco respuestas fueron HTTP 404 NotFoundError.
- Consulta de dos reportes públicos de ANY.RUN y recopilación de cuatro capturas reales (tres de ANY.RUN y una de disponibilidad de FileASSASSIN).
- Verificación de la ruta oficial histórica de FileASSASSIN: no disponible; no se usaron espejos de terceros.

## Actividades pendientes o no ejecutadas

- Instalación, actualización y escaneo de Malwarebytes, consulta de registros y cuarentena: el instalador oficial se descargó y se preparó una VM Windows aislada en Docker, pero la VM no se inició mientras se espera autorización expresa para aceptar los términos de licencia de Windows y Malwarebytes.
- FileASSASSIN no se ejecutó; la ruta oficial histórica devuelve “Invalid request” y la página de producto redirige a descargas generales.
- No se ejecutó malware real ni se hizo análisis dinámico local.
- No se localizó el archivo independiente image.png mencionado por el prompt maestro.

## Herramientas, instalaciones y espacio

Se reutilizaron `file`, `md5sum`, `sha256sum`, Python y Docker disponibles. Los paquetes auxiliares se descargaron desde repositorios Ubuntu y se extrajeron dentro de `08_herramientas`. La imagen REMnux ocupó temporalmente 18,796,300,564 bytes según Docker; se retiró tras ejecutar el análisis y guardar las salidas, recuperando ese espacio. La imagen de Windows se descargó, pero su VM no se inició. El instalador Malwarebytes queda en la carpeta de preparación y se excluye del paquete final. No se instalaron paquetes en el anfitrión fuera del directorio del laboratorio.

## Conteos y entregables

- Muestras analizadas estáticamente: 5.
- Hashes MD5: 5; hashes SHA-256: 5; huellas ssdeep: 5 (varias con advertencia de tamaño insuficiente para comparación significativa).
- Consultas VirusTotal: 5; reportes disponibles: 0; respuestas HTTP 404: 5.
- Coincidencias YARA: 2, ambas insertadas de forma intencional en archivos de prueba.
- Capturas reales incorporadas: 4, tres de ANY.RUN y una de la consulta oficial de FileASSASSIN; los resultados de REMnux se conservan como registros originales.
- Informe académico: DOCX basado en la plantilla del usuario y versiones Markdown y HTML.

## Incidencias y límites

VirtualBox estaba presente, pero el kernel no tenía cargado vboxdrv y no había máquinas registradas. Malwarebytes no está disponible para Linux; el entorno temporal Windows permanece detenido por la autorización de licencia pendiente. VirusTotal no devolvió informes para los cinco hashes nuevos. ssdeep avisó que varias muestras eran demasiado pequeñas para obtener valores comparativos útiles. Ninguna de estas condiciones se sustituyó por resultados supuestos.
