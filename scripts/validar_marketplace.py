"""Clona cada plugin del marketplace y corre `claude plugin validate` sobre él.

Escribe un reporte en Markdown. Sale con 1 si algún plugin no valida, con 2 si
el chequeo mismo falló.

Uso: python scripts/validar_marketplace.py [--reporte reporte.md]
Requiere git y el CLI `claude` en el PATH.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CLAUDE = shutil.which("claude") or "claude"


def validar(ruta):
    r = subprocess.run(
        [CLAUDE, "plugin", "validate", str(ruta), "--profile", "directory"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return r.returncode, (r.stdout + r.stderr).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reporte", default="reporte-validacion.md")
    args = ap.parse_args()

    marketplace = json.loads((RAIZ / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    resultados = []  # (nombre, repo, ok, salida)

    codigo, salida = validar(RAIZ)
    resultados.append(("ar-plugins (marketplace)", "kvothesson/ar-plugins", codigo == 0, salida))

    with tempfile.TemporaryDirectory() as tmp:
        for p in marketplace["plugins"]:
            src = p.get("source", {})
            if not isinstance(src, dict) or src.get("source") != "github":
                continue
            destino = Path(tmp) / p["name"]
            clon = subprocess.run(
                ["git", "clone", "-q", "--depth", "1", f"https://github.com/{src['repo']}", str(destino)],
                capture_output=True, text=True,
            )
            if clon.returncode != 0:
                resultados.append((p["name"], src["repo"], False, f"no se pudo clonar: {clon.stderr.strip()}"))
                continue
            codigo, salida = validar(destino)
            resultados.append((p["name"], src["repo"], codigo == 0, salida))

    malos = [r for r in resultados if not r[2]]
    lineas = [
        "# Validación de plugins",
        "",
        f"{len(resultados)} validados con `claude plugin validate --profile directory`: "
        f"{len(resultados) - len(malos)} ok, {len(malos)} con errores.",
    ]
    if malos:
        lineas += ["", "Un plugin que no valida **no se puede instalar** o el directorio oficial lo rechaza.", ""]
        for nombre, repo, _, salida in malos:
            lineas += [f"## [{nombre}](https://github.com/{repo})", "", "```", salida, "```", ""]
    lineas += ["", "| Plugin | Resultado |", "|---|---|"]
    lineas += [f"| [{n}](https://github.com/{r}) | {'ok' if ok else 'ERROR'} |" for n, r, ok, _ in resultados]

    reporte = "\n".join(lineas) + "\n"
    Path(args.reporte).write_text(reporte, encoding="utf-8")
    print(reporte)
    return 1 if malos else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        import traceback

        traceback.print_exc()
        sys.exit(2)
