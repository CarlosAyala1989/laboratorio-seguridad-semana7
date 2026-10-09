#!/usr/bin/env python3
"""Descarga y despliega herramientas del laboratorio bajo el directorio local."""
from pathlib import Path
import os
import subprocess
import sys

raiz = Path(__file__).resolve().parents[1]
paquetes = raiz / "08_herramientas" / "paquetes"
destino = raiz / "08_herramientas" / "raiz_local"
paquetes.mkdir(parents=True, exist_ok=True)
destino.mkdir(parents=True, exist_ok=True)
solicitados = ["libimage-exiftool-perl", "libarchive-zip-perl", "ssdeep", "libfuzzy2", "yara", "libyara10"]

descarga = subprocess.run(["apt-get", "download", *solicitados], cwd=paquetes, text=True, capture_output=True)
if descarga.returncode:
    print(descarga.stderr.strip(), file=sys.stderr)
    raise SystemExit(descarga.returncode)

for paquete in sorted(paquetes.glob("*.deb")):
    resultado = subprocess.run(["dpkg-deb", "-x", str(paquete), str(destino)], text=True, capture_output=True)
    if resultado.returncode:
        print(resultado.stderr.strip(), file=sys.stderr)
        raise SystemExit(resultado.returncode)

rutas_bin = destino / "usr" / "bin"
rutas_lib = [destino / "usr" / "lib" / "x86_64-linux-gnu", destino / "lib" / "x86_64-linux-gnu"]
rutas_perl = [str(p) for p in (destino / "usr" / "share").glob("perl*")]
entorno = os.environ.copy()
entorno["PATH"] = str(rutas_bin) + os.pathsep + entorno.get("PATH", "")
entorno["LD_LIBRARY_PATH"] = os.pathsep.join(str(p) for p in rutas_lib) + os.pathsep + entorno.get("LD_LIBRARY_PATH", "")
entorno["PERL5LIB"] = os.pathsep.join(rutas_perl) + os.pathsep + entorno.get("PERL5LIB", "")

for nombre, argumentos in [("exiftool", ["-ver"]), ("ssdeep", ["-V"]), ("yara", ["--version"]), ("yarac", ["--version"])]:
    ejecutable = rutas_bin / nombre
    if not ejecutable.exists():
        print(f"{nombre}: no se encontró el ejecutable local")
        continue
    resultado = subprocess.run([str(ejecutable), *argumentos], env=entorno, text=True, capture_output=True)
    salida = (resultado.stdout or resultado.stderr).strip().splitlines()
    print(f"{nombre}: {salida[0] if salida else 'sin salida'} (código {resultado.returncode})")
    if resultado.returncode:
        raise SystemExit(resultado.returncode)

total = sum(p.stat().st_size for p in paquetes.glob("*.deb"))
print(f"Paquetes: {len(list(paquetes.glob('*.deb')))}; descarga acumulada: {total} bytes")
print(f"Herramientas locales: {destino}")
