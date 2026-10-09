#!/usr/bin/env python3
"""Registra las características del sistema y la disponibilidad de herramientas."""
from pathlib import Path
from datetime import datetime
import json
import platform
import shutil
import subprocess

raiz = Path(__file__).resolve().parents[1]
salida = raiz / "01_diagnostico"
salida.mkdir(parents=True, exist_ok=True)

def ejecutar(comando):
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=20)
        return {"codigo": resultado.returncode, "salida": resultado.stdout.strip(), "error": resultado.stderr.strip()}
    except Exception as error:
        return {"codigo": None, "salida": "", "error": str(error)}

comandos = {
    "distribucion": ["cat", "/etc/os-release"],
    "kernel": ["uname", "-a"],
    "procesador": ["lscpu"],
    "interfaces_red": ["ip", "-brief", "address"],
    "virtualizacion": ["systemd-detect-virt"],
    "memoria": ["free", "-h"],
    "espacio": ["df", "-h", "/VMQEMU"],
    "virtualbox_version": ["VBoxManage", "--version"],
    "virtualbox_maquinas": ["VBoxManage", "list", "vms"],
    "virtualbox_en_ejecucion": ["VBoxManage", "list", "runningvms"],
    "docker_version": ["docker", "info", "--format", "Servidor {{.ServerVersion}}; raíz {{.DockerRootDir}}"],
    "imagenes_remnux": ["docker", "image", "ls", "--format", "{{.Repository}}:{{.Tag}}"],
}
registro = {
    "fecha_hora": datetime.now().astimezone().isoformat(timespec="seconds"),
    "sistema": platform.platform(),
    "arquitectura": platform.machine(),
    "procesador": platform.processor(),
    "herramientas": {nombre: shutil.which(nombre) for nombre in ["file", "exiftool", "ssdeep", "yara", "yarac", "md5sum", "sha256sum", "python3", "docker", "VBoxManage", "remnux", "malwarebytes", "mbam"]},
    "herramientas_locales": {
        nombre: str(raiz / "08_herramientas" / "raiz_local" / "usr" / "bin" / nombre)
        for nombre in ["exiftool", "ssdeep", "yara", "yarac"]
    },
    "comandos": {nombre: ejecutar(comando) for nombre, comando in comandos.items()},
}
salida_imagenes = registro["comandos"]["imagenes_remnux"]["salida"]
registro["comandos"]["imagenes_remnux"]["salida"] = "\\n".join(
    linea for linea in salida_imagenes.splitlines() if "remnux" in linea.lower()
) or "No se encontró una imagen REMnux local."

(salida / "diagnostico_entorno.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
lineas = [
    "DIAGNÓSTICO DEL ENTORNO - LABORATORIO 07",
    f"Fecha y hora: {registro['fecha_hora']}",
    f"Sistema: {registro['sistema']}",
    f"Arquitectura: {registro['arquitectura']}",
    f"Procesador: {registro['procesador'] or 'No informado por el sistema'}",
    "",
    "Herramientas detectadas:",
]
for nombre, ruta in registro["herramientas"].items():
    local = registro["herramientas_locales"].get(nombre)
    lineas.append(f"- {nombre}: {ruta or (local if local and Path(local).exists() else 'no disponible')}")
lineas.append("")
for nombre, dato in registro["comandos"].items():
    lineas.append(f"[{nombre}]")
    lineas.append(dato["salida"] or dato["error"] or "(sin salida)")
    lineas.append("")
(salida / "diagnostico_entorno.txt").write_text("\n".join(lineas), encoding="utf-8")
print(salida / "diagnostico_entorno.txt")
