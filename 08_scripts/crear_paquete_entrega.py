#!/usr/bin/env python3
"""Crea un ZIP compacto con el informe y sus evidencias verificables."""
from __future__ import annotations

import csv
import hashlib
import io
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / "entrega_laboratorio_07.zip"
OMITIR_PREFIJOS = (
    "10_fuentes/plantilla_render/",
    "10_fuentes/revision_visual_pdf/",
    "10_fuentes/render_qa/",
    "02_malwarebytes/windows_storage/",
    "02_malwarebytes/share/",
)
OMITIR_NOMBRES = {SALIDA.name, "MBSetup.exe"}
OMITIR_SUFIXOS = {".iso", ".qcow2", ".vdi", ".vmdk", ".img", ".raw"}


def es_entregable(ruta: Path) -> bool:
    relativa = ruta.relative_to(RAIZ).as_posix()
    return (
        ruta.is_file()
        and ruta.name not in OMITIR_NOMBRES
        and ruta.suffix.lower() not in OMITIR_SUFIXOS
        and not relativa.startswith(OMITIR_PREFIJOS)
        and not ruta.name.startswith("revision_")
    )


def main() -> None:
    archivos = sorted(p for p in RAIZ.rglob("*") if es_entregable(p))
    manifiesto = io.StringIO(newline="")
    escritor = csv.writer(manifiesto)
    escritor.writerow(["ruta", "tamaño_bytes", "sha256"])
    for ruta in archivos:
        datos = ruta.read_bytes()
        escritor.writerow([
            ruta.relative_to(RAIZ).as_posix(),
            len(datos),
            hashlib.sha256(datos).hexdigest(),
        ])

    with zipfile.ZipFile(SALIDA, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as paquete:
        for ruta in archivos:
            paquete.write(ruta, arcname=(Path(RAIZ.name) / ruta.relative_to(RAIZ)).as_posix())
        paquete.writestr(
            f"{RAIZ.name}/MANIFIESTO_SHA256.csv",
            manifiesto.getvalue().encode("utf-8-sig"),
        )
    print(f"ZIP: {SALIDA}")
    print(f"Archivos: {len(archivos)} más el manifiesto")
    print(f"Tamaño: {SALIDA.stat().st_size} bytes")


if __name__ == "__main__":
    main()
