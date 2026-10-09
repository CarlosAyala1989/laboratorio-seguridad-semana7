#!/usr/bin/env bash
set -Eeuo pipefail

echo '=== Ejecución en REMnux Docker ==='
date -u '+Fecha UTC: %Y-%m-%d %H:%M:%S'
id
grep -E '^(PRETTY_NAME|VERSION_ID)=' /etc/os-release || true
echo '=== Versiones de herramientas ==='
file --version | head -n 1
exiftool -ver
md5sum --version | head -n 1
sha256sum --version | head -n 1
ssdeep -V 2>&1 | head -n 1
yara --version

echo '=== Análisis de exactamente cinco muestras benignas ==='
for archivo in /home/remnux/files/muestra_*; do
  [[ -f "$archivo" ]] || continue
  echo
  echo "--- $(basename "$archivo") ---"
  file -- "$archivo"
  echo '[ExifTool]'
  exiftool -G1 -s -- "$archivo"
  echo '[MD5]'
  md5sum -- "$archivo"
  echo '[SHA-256]'
  sha256sum -- "$archivo"
  echo '[ssdeep]'
  ssdeep "$archivo"
  echo '[YARA]'
  if resultado_yara=$(yara /home/remnux/reglas/reglas_laboratorio.yar "$archivo"); then
    if [[ -n "$resultado_yara" ]]; then
      printf '%s\n' "$resultado_yara"
      echo 'Resultado YARA: coincidencia.'
    else
      echo 'Resultado YARA: sin coincidencias.'
    fi
  else
    estado_yara=$?
    echo 'Error al ejecutar YARA.' >&2
    exit "$estado_yara"
  fi
done
