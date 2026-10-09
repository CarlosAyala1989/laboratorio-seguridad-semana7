#!/usr/bin/env python3
"""Crea cinco archivos benignos y documenta su identificación y huellas."""
from pathlib import Path
import csv
import hashlib
import json
import os
import subprocess
import zipfile

raiz = Path(__file__).resolve().parents[1]
muestras = raiz / "04_remnux" / "muestras"
metadatos = raiz / "04_remnux" / "metadatos"
huellas = raiz / "04_remnux" / "hashes"
herramientas = raiz / "08_herramientas" / "raiz_local"
for carpeta in [muestras, metadatos, huellas]:
    carpeta.mkdir(parents=True, exist_ok=True)

def ejecutar(comando, entorno=None):
    return subprocess.run(comando, capture_output=True, text=True, env=entorno, timeout=30)

def preparar_entorno():
    entorno = os.environ.copy()
    entorno["PATH"] = str(herramientas / "usr" / "bin") + os.pathsep + entorno.get("PATH", "")
    entorno["LD_LIBRARY_PATH"] = str(herramientas / "usr" / "lib" / "x86_64-linux-gnu") + os.pathsep + entorno.get("LD_LIBRARY_PATH", "")
    rutas_perl = [str(ruta) for ruta in (herramientas / "usr" / "share").glob("perl*")]
    entorno["PERL5LIB"] = os.pathsep.join(rutas_perl) + os.pathsep + entorno.get("PERL5LIB", "")
    return entorno

entorno = preparar_entorno()
contenidos = {
    "muestra_01_texto.txt": "Muestra benigna de laboratorio.\nMARCA_PRUEBA_YARA_CONTROLADA\nUso exclusivo para demostrar una regla YARA.\n",
    "muestra_02_datos.json": json.dumps(
        {"tipo": "muestra de laboratorio", "indicador_json_benigno": "registro_controlado", "analisis_estatico": True},
        ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ) + "\n",
    "muestra_03_registros.csv": "id,descripcion,estado\n1,registro benigno,demostrativo\n2,segundo registro,controlado\n",
    "muestra_05_script_inerte.py": "# Archivo de texto inerte para inspección estática.\n# No contiene acciones ejecutables ni se ejecutará.\n",
}
for nombre, contenido in contenidos.items():
    (muestras / nombre).write_text(contenido, encoding="utf-8")
ruta_zip = muestras / "muestra_04_paquete.zip"
with zipfile.ZipFile(ruta_zip, "w", compression=zipfile.ZIP_DEFLATED) as archivo_zip:
    entrada = zipfile.ZipInfo("LEEME.txt", date_time=(2026, 10, 8, 0, 0, 0))
    entrada.compress_type = zipfile.ZIP_DEFLATED
    archivo_zip.writestr(entrada, "Contenido benigno incluido en un ZIP de prueba.\n")

descripciones = {
    "muestra_01_texto.txt": "Texto benigno creado localmente; contiene una marca intencional para una regla YARA de demostración.",
    "muestra_02_datos.json": "JSON benigno creado localmente; contiene campos de laboratorio para una segunda regla YARA.",
    "muestra_03_registros.csv": "CSV benigno creado localmente con dos filas de datos ficticios.",
    "muestra_04_paquete.zip": "Archivo ZIP benigno creado localmente; contiene únicamente LEEME.txt.",
    "muestra_05_script_inerte.py": "Archivo de texto con comentarios; no se ejecutó y no contiene acciones.",
}
registros = []
ruta_resultados_previos = raiz / "resultados_muestras.csv"
resultados_previos = {}
if ruta_resultados_previos.exists():
    with ruta_resultados_previos.open(encoding="utf-8-sig", newline="") as archivo_previo:
        resultados_previos = {fila["nombre"]: fila for fila in csv.DictReader(archivo_previo)}
archivos_muestra = sorted(ruta for ruta in muestras.glob("muestra_*") if ruta.is_file())
for numero, ruta in enumerate(archivos_muestra, start=1):
    datos = ruta.read_bytes()
    md5_python = hashlib.md5(datos).hexdigest()
    sha256_python = hashlib.sha256(datos).hexdigest()
    salida_file = ejecutar(["file", "--brief", str(ruta)])
    salida_mime = ejecutar(["file", "--brief", "--mime-type", str(ruta)])
    salida_exiftool = ejecutar(["exiftool", "-j", "-G1", "-s", "--", str(ruta)], entorno)
    salida_ssdeep = ejecutar(["ssdeep", "-b", str(ruta)], entorno)
    salida_md5 = ejecutar(["md5sum", str(ruta)])
    salida_sha256 = ejecutar(["sha256sum", str(ruta)])
    lineas_ssdeep = salida_ssdeep.stdout.splitlines()
    valor_ssdeep = lineas_ssdeep[1].split(",", 1)[0] if len(lineas_ssdeep) > 1 else ""
    try:
        datos_exiftool = json.loads(salida_exiftool.stdout)
    except json.JSONDecodeError:
        datos_exiftool = {"error": salida_exiftool.stderr or "No se pudo interpretar el resultado de ExifTool."}
    anterior = resultados_previos.get(ruta.name, {})
    registro = {
        "identificador": f"M{numero:02d}",
        "nombre": ruta.name,
        "origen": "Archivo benigno generado localmente para la práctica",
        "ruta": str(ruta),
        "tamaño_bytes": len(datos),
        "extension": ruta.suffix.lower(),
        "tipo_real": salida_file.stdout.strip(),
        "mime_type": salida_mime.stdout.strip(),
        "descripcion": descripciones[ruta.name],
        "md5": md5_python,
        "sha256": sha256_python,
        "ssdeep": valor_ssdeep or "No calculado",
        "md5_formato_valido": len(md5_python) == 32 and all(c in "0123456789abcdef" for c in md5_python),
        "sha256_formato_valido": len(sha256_python) == 64 and all(c in "0123456789abcdef" for c in sha256_python),
        "coincidencia_md5sum": salida_md5.returncode == 0 and salida_md5.stdout.split()[0] == md5_python,
        "coincidencia_sha256sum": salida_sha256.returncode == 0 and salida_sha256.stdout.split()[0] == sha256_python,
        "referencia_integridad": "No disponible; la consistencia se contrastó con hashlib de Python.",
        "consulta_virustotal": anterior.get("consulta_virustotal", "pendiente"),
        "coincidencias_yara": anterior.get("coincidencias_yara", "pendiente"),
        "vt_estado": anterior.get("vt_estado", ""),
        "vt_maliciosos": anterior.get("vt_maliciosos", ""),
        "vt_sospechosos": anterior.get("vt_sospechosos", ""),
        "vt_no_detectados": anterior.get("vt_no_detectados", ""),
        "vt_fecha_analisis": anterior.get("vt_fecha_analisis", ""),
        "estado": "procesado",
    }
    registros.append(registro)
    (metadatos / f"{ruta.name}.txt").write_text(
        f"Archivo: {ruta.name}\n"
        f"Origen: {registro['origen']}\n"
        f"Ruta: {ruta}\n"
        f"Tamaño: {len(datos)} bytes\n"
        f"Comando: file --brief --mime-type {ruta}\n{salida_file.stdout}"
        f"\nComando: exiftool -j -G1 -s -- {ruta}\n{salida_exiftool.stdout or salida_exiftool.stderr}"
        f"\nComando: ssdeep -b {ruta}\n{salida_ssdeep.stdout or salida_ssdeep.stderr}",
        encoding="utf-8",
    )
    (metadatos / f"{ruta.name}_exiftool.json").write_text(
        json.dumps(datos_exiftool, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (huellas / f"{ruta.name}_hashes.txt").write_text(
        f"Comando md5sum: {salida_md5.stdout.strip()}\n"
        f"hashlib MD5: {md5_python}\n"
        f"Comando sha256sum: {salida_sha256.stdout.strip()}\n"
        f"hashlib SHA-256: {sha256_python}\n"
        f"Coincidencia MD5: {registro['coincidencia_md5sum']}\n"
        f"Coincidencia SHA-256: {registro['coincidencia_sha256sum']}\n"
        f"ssdeep: {valor_ssdeep or salida_ssdeep.stderr.strip() or 'No calculado'}\n",
        encoding="utf-8",
    )

campos = [
    "identificador", "nombre", "origen", "ruta", "tamaño_bytes", "extension", "tipo_real", "mime_type",
    "md5", "sha256", "ssdeep", "md5_formato_valido", "sha256_formato_valido",
    "coincidencia_md5sum", "coincidencia_sha256sum", "referencia_integridad",
    "consulta_virustotal", "coincidencias_yara", "vt_estado", "vt_maliciosos", "vt_sospechosos",
    "vt_no_detectados", "vt_fecha_analisis", "estado", "descripcion"
]
with (raiz / "resultados_muestras.csv").open("w", newline="", encoding="utf-8-sig") as archivo_csv:
    escritor = csv.DictWriter(archivo_csv, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(registros)
(huellas / "resultados_huellas.json").write_text(json.dumps(registros, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(muestras / "README_muestras.md").write_text(
    "# Inventario de muestras\n\n"
    "Las cinco muestras fueron generadas localmente para esta práctica. Son benignas, no se descargaron de repositorios externos y no se ejecutaron. "
    "La marca YARA del archivo TXT y el patrón JSON fueron añadidos intencionalmente para validar reglas de demostración.\n\n"
    + "\n".join(f"- {r['identificador']}: {r['nombre']} - {r['descripcion']}" for r in registros) + "\n",
    encoding="utf-8",
)
print(f"Archivos analizados: {len(registros)}")
print(raiz / "resultados_muestras.csv")
