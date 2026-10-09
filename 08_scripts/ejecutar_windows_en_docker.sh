#!/usr/bin/env bash
set -Eeuo pipefail

raiz="/VMQEMU/laboratorio-seguridad/laboratorio_07_analisis_malware"
nombre_red="laboratorio07-windows"
nombre_contenedor="lab07-malwarebytes-windows"

if [[ "${ACEPTAR_LICENCIAS_WINDOWS:-}" != "SI" ]]; then
  echo "No se inicia la VM: el aprovisionador de Windows acepta automáticamente sus términos. Tras aceptarlos expresamente, establece ACEPTAR_LICENCIAS_WINDOWS=SI." >&2
  exit 2
fi

if [[ "${ACEPTAR_ACCESO_KVM_NET_ADMIN:-}" != "SI" ]]; then
  echo "No se inicia la VM: requiere acceso a /dev/kvm, /dev/net/tun y NET_ADMIN. Tras autorizarlo expresamente, establece ACEPTAR_ACCESO_KVM_NET_ADMIN=SI." >&2
  exit 2
fi

if docker container inspect "$nombre_contenedor" >/dev/null 2>&1; then
  echo "Ya existe el contenedor $nombre_contenedor; no se reemplaza." >&2
  exit 1
fi

if ! docker network inspect "$nombre_red" >/dev/null 2>&1; then
  docker network create "$nombre_red" >/dev/null
fi

docker run --detach \
  --name "$nombre_contenedor" \
  --stop-timeout 120 \
  --network "$nombre_red" \
  --publish 127.0.0.1:8006:8006 \
  --device /dev/kvm \
  --device /dev/net/tun \
  --cap-add NET_ADMIN \
  --env VERSION=11 \
  --env LANGUAGE=es-ES \
  --env RAM_SIZE=4G \
  --env CPU_CORES=2 \
  --env DISK_SIZE=64G \
  --env SAMBA=Y \
  --env SAMBA_READONLY=Y \
  --env SHORTCUT=Y \
  --volume "$raiz/02_malwarebytes/windows_storage:/storage" \
  --volume "$raiz/02_malwarebytes/share:/share:ro" \
  dockurr/windows:latest
