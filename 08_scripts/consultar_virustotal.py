#!/usr/bin/env python3
"""Consulta reportes VirusTotal v3 por SHA-256, sin cargar archivos."""
from pathlib import Path
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import csv
import json
import os
import time

raiz = Path(__file__).resolve().parents[1]
ruta_csv = raiz / "resultados_muestras.csv"
ruta_json = raiz / "resultados_virustotal.json"
ruta_evidencia = raiz / "04_remnux" / "virustotal"
ruta_evidencia.mkdir(parents=True, exist_ok=True)
clave = os.environ.get("VIRUSTOTAL_API_KEY", "")
if not clave:
    raise SystemExit("No está configurada la variable VIRUSTOTAL_API_KEY; no se realizó ninguna consulta.")

with ruta_csv.open(encoding="utf-8-sig", newline="") as archivo:
    filas = list(csv.DictReader(archivo))
    campos = list(filas[0].keys()) if filas else []
if not filas:
    raise SystemExit("No hay hashes de muestra en resultados_muestras.csv.")

if ruta_json.exists():
    anterior = json.loads(ruta_json.read_text(encoding="utf-8"))
else:
    anterior = {"consultas": []}
cache = {item["sha256"]: item for item in anterior.get("consultas", []) if item.get("sha256")}
consultas = list(anterior.get("consultas", []))
solicitudes_realizadas = 0
politica = {
    "limite_usuario_por_minuto": 4,
    "limite_usuario_por_dia": 500,
    "limite_usuario_por_mes": 15500,
    "maximo_aplicado_por_minuto": 3,
    "intervalo_minimo_segundos": 26,
    "maximo_de_esta_practica": 5,
    "archivos_subidos": False,
    "consultas_solo_por": "SHA-256",
}

for fila in filas:
    sha256 = fila["sha256"]
    if sha256 in cache:
        continue
    if solicitudes_realizadas >= 5:
        break
    if solicitudes_realizadas:
        time.sleep(26)
    momento = datetime.now().astimezone().isoformat(timespec="seconds")
    peticion = Request(
        f"https://www.virustotal.com/api/v3/files/{sha256}",
        headers={"x-apikey": clave, "accept": "application/json", "user-agent": "Laboratorio-07-Analisis-Estatico/1.0"},
        method="GET",
    )
    entrada = {
        "identificador": fila["identificador"],
        "nombre": fila["nombre"],
        "sha256": sha256,
        "fecha_hora_consulta": momento,
        "endpoint": f"https://www.virustotal.com/api/v3/files/{sha256}",
        "archivo_subido": False,
    }
    try:
        with urlopen(peticion, timeout=25) as respuesta:
            codigo = respuesta.status
            contenido = respuesta.read()
        cuerpo = json.loads(contenido.decode("utf-8"))
        atributos = cuerpo.get("data", {}).get("attributes", {})
        estadisticas = atributos.get("last_analysis_stats", {})
        fecha_analisis = atributos.get("last_analysis_date")
        entrada.update({
            "http_status": codigo,
            "estado": "reporte_disponible",
            "nombre_conocido": atributos.get("meaningful_name") or (atributos.get("names") or [None])[0],
            "fecha_analisis_unix": fecha_analisis,
            "estadisticas": {
                "maliciosos": estadisticas.get("malicious", 0),
                "sospechosos": estadisticas.get("suspicious", 0),
                "no_detectados": estadisticas.get("undetected", 0),
                "inofensivos": estadisticas.get("harmless", 0),
                "total_informado": sum(estadisticas.values()) if estadisticas else 0,
            },
            "url_reporte": f"https://www.virustotal.com/gui/file/{sha256}",
        })
    except HTTPError as error:
        codigo = error.code
        cuerpo_error = error.read()
        try:
            detalle = json.loads(cuerpo_error.decode("utf-8")).get("error", {}).get("code", "Error HTTP")
        except Exception:
            detalle = "Error HTTP"
        entrada.update({"http_status": codigo, "estado": "sin_reporte" if codigo == 404 else "error_http", "detalle": detalle})
    except (URLError, TimeoutError, OSError) as error:
        entrada.update({"http_status": None, "estado": "error_red", "detalle": type(error).__name__})
    except Exception as error:
        entrada.update({"http_status": None, "estado": "error_respuesta", "detalle": type(error).__name__})
    consultas.append(entrada)
    cache[sha256] = entrada
    solicitudes_realizadas += 1
    anterior = {
        "fecha_generacion": datetime.now().astimezone().isoformat(timespec="seconds"),
        "politica_de_consulta": politica,
        "cantidad_consultas_registradas": len(consultas),
        "cantidad_consultas_nuevas_en_esta_ejecucion": solicitudes_realizadas,
        "consultas": consultas,
    }
    texto = json.dumps(anterior, ensure_ascii=False, indent=2) + "\n"
    ruta_json.write_text(texto, encoding="utf-8")
    (ruta_evidencia / "resultados_virustotal.json").write_text(texto, encoding="utf-8")
    print(f"{fila['identificador']}: HTTP {entrada.get('http_status')} - {entrada['estado']}")
    if entrada.get("http_status") in (401, 403, 429):
        break
    if entrada["estado"].startswith("error_"):
        break

for fila in filas:
    entrada = cache.get(fila["sha256"])
    if not entrada:
        fila["consulta_virustotal"] = "no consultado"
        fila["vt_estado"] = "no consultado"
        fila["vt_maliciosos"] = ""
        fila["vt_sospechosos"] = ""
        fila["vt_no_detectados"] = ""
        fila["vt_fecha_analisis"] = ""
        continue
    estado = entrada.get("estado", "sin dato")
    fila["consulta_virustotal"] = f"{estado} (HTTP {entrada.get('http_status')})"
    fila["vt_estado"] = estado
    estadisticas = entrada.get("estadisticas", {})
    fila["vt_maliciosos"] = estadisticas.get("maliciosos", "")
    fila["vt_sospechosos"] = estadisticas.get("sospechosos", "")
    fila["vt_no_detectados"] = estadisticas.get("no_detectados", "")
    fecha = entrada.get("fecha_analisis_unix")
    fila["vt_fecha_analisis"] = datetime.fromtimestamp(fecha, tz=timezone.utc).isoformat() if fecha else ""
for nombre in ["vt_estado", "vt_maliciosos", "vt_sospechosos", "vt_no_detectados", "vt_fecha_analisis"]:
    if nombre not in campos:
        campos.append(nombre)
with ruta_csv.open("w", encoding="utf-8-sig", newline="") as archivo:
    escritor = csv.DictWriter(archivo, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(filas)
(ruta_evidencia / "politica_consultas.md").write_text(
    "Las consultas de VirusTotal se realizaron mediante GET al endpoint de reportes API v3 usando SHA-256. "
    "No se cargó el contenido de ninguna muestra. El presupuesto se limitó a cinco hashes únicos, con 26 segundos entre solicitudes, "
    "caché de respuestas y detención ante HTTP 401, 403 o 429. La clave se recibió por variable de entorno temporal y no se guardó.\n",
    encoding="utf-8",
)
print(f"Consultas nuevas: {solicitudes_realizadas}; muestras: {len(filas)}")
