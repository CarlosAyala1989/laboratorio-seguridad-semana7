#!/usr/bin/env python3
"""Compila dos reglas de demostración y las aplica a las cinco muestras."""
from pathlib import Path
import csv
import os
import subprocess

raiz = Path(__file__).resolve().parents[1]
herramientas = raiz / "08_herramientas" / "raiz_local" / "usr" / "bin"
reglas = raiz / "05_yara" / "reglas" / "reglas_laboratorio.yar"
carpeta_muestras = raiz / "04_remnux" / "muestras"
carpeta_resultados = raiz / "05_yara" / "resultados"
carpeta_resultados.mkdir(parents=True, exist_ok=True)
binario_compilado = carpeta_resultados / "reglas_laboratorio.yarc"
entorno = os.environ.copy()
entorno["PATH"] = str(herramientas) + os.pathsep + entorno.get("PATH", "")
entorno["LD_LIBRARY_PATH"] = str(raiz / "08_herramientas" / "raiz_local" / "usr" / "lib" / "x86_64-linux-gnu") + os.pathsep + entorno.get("LD_LIBRARY_PATH", "")

compilacion = subprocess.run([str(herramientas / "yarac"), str(reglas), str(binario_compilado)], capture_output=True, text=True, env=entorno)
if compilacion.returncode:
    raise SystemExit(compilacion.stderr or "La compilación de reglas YARA falló.")

lineas = [
    "RESULTADOS DE VALIDACIÓN YARA",
    f"Reglas fuente: {reglas}",
    f"Reglas compiladas: {binario_compilado}",
    f"Validación de sintaxis: correcta (yarac {compilacion.returncode})",
    "Alcance: cinco archivos benignos creados localmente; ninguno se ejecutó.",
    "",
]
coincidencias_por_archivo = {}
for muestra in sorted(carpeta_muestras.glob("muestra_*")):
    if not muestra.is_file():
        continue
    resultado = subprocess.run([str(herramientas / "yara"), "-s", str(reglas), str(muestra)], capture_output=True, text=True, env=entorno)
    if resultado.returncode not in (0, 1):
        lineas.append(f"{muestra.name}: error de procesamiento: {resultado.stderr.strip()}")
        coincidencias_por_archivo[muestra.name] = "Error de procesamiento"
        continue
    nombres_reglas = {"Cadena_Controlada_Muestra", "Marcador_JSON_Benigno"}
    coincidencias = []
    for linea in resultado.stdout.splitlines():
        partes = linea.split()
        if partes and partes[0] in nombres_reglas:
            coincidencias.append(partes[0])
    etiquetas = sorted(set(coincidencias))
    coincidencias_por_archivo[muestra.name] = "; ".join(etiquetas) if etiquetas else "Sin coincidencias"
    lineas.append(f"Muestra: {muestra.name}")
    lineas.append(f"Coincidencias: {coincidencias_por_archivo[muestra.name]}")
    lineas.append("Evidencia: " + (resultado.stdout.strip().replace("\n", " | ") if resultado.stdout.strip() else "No se encontraron cadenas definidas por las reglas."))
    lineas.append("Interpretación: las reglas marcan cadenas de demostración; la coincidencia no clasifica la muestra como maliciosa.")
    lineas.append("")
    (carpeta_resultados / f"{muestra.name}_yara.txt").write_text(
        f"Comando: yara -s {reglas} {muestra}\n"
        f"Salida:\n{resultado.stdout or '(sin coincidencias)'}"
        f"{'Error: ' + resultado.stderr if resultado.stderr else ''}\n",
        encoding="utf-8",
    )

ruta_csv = raiz / "resultados_muestras.csv"
with ruta_csv.open(encoding="utf-8-sig", newline="") as archivo:
    filas = list(csv.DictReader(archivo))
    campos = list(filas[0].keys()) if filas else []
for fila in filas:
    fila["coincidencias_yara"] = coincidencias_por_archivo.get(fila["nombre"], "Sin coincidencias")
with ruta_csv.open("w", encoding="utf-8-sig", newline="") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(filas)

resumen = f"Coincidencias positivas observadas: {sum(1 for valor in coincidencias_por_archivo.values() if valor not in ('Sin coincidencias', 'Error de procesamiento'))} de {len(coincidencias_por_archivo)} muestras."
lineas.insert(5, resumen)
(carpeta_resultados / "resultados_yara.txt").write_text("\n".join(lineas), encoding="utf-8")
(raiz / "resultados_yara.txt").write_text("\n".join(lineas), encoding="utf-8")
print(resumen)
print(raiz / "resultados_yara.txt")
