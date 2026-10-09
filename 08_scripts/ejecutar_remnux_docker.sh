#!/usr/bin/env bash
set -Eeuo pipefail

raiz="/VMQEMU/laboratorio-seguridad/laboratorio_07_analisis_malware"
docker run --rm --network none --user remnux \
  --volume "$raiz/04_remnux/muestras:/home/remnux/files:ro" \
  --volume "$raiz/05_yara/reglas/reglas_laboratorio.yar:/home/remnux/reglas/reglas_laboratorio.yar:ro" \
  --volume "$raiz/08_scripts/procesar_muestras_remnux.sh:/home/remnux/procesar_muestras_remnux.sh:ro" \
  remnux/remnux-distro:noble \
  bash /home/remnux/procesar_muestras_remnux.sh \
  > "$raiz/04_remnux/resultados_docker/ejecucion_remnux.log" 2>&1

