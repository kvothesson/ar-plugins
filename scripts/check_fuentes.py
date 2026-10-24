"""Chequea que las fuentes de datos de los plugins del marketplace respondan.

Lee .claude-plugin/marketplace.json, baja los SKILL.md de cada plugin desde
GitHub, extrae las URLs y le pega a cada una. Escribe un reporte en Markdown y
sale con código 1 si alguna fuente está rota.

Uso: python scripts/check_fuentes.py [--reporte reporte.md]
Solo usa la biblioteca estándar. Si existe GITHUB_TOKEN, lo usa para la API.
"""

import argparse
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (compatible; ar-plugins-check-fuentes/1.0; +https://github.com/kvothesson/ar-plugins)"
TIMEOUT = 25

# URLs con placeholders ([mes], {id}, <cuil>) o que terminan en "=" son plantillas,
# no fuentes: el agente las completa en el momento.
RE_URL = re.compile(r"https?://[^\s`'\"<>()\[\]{}|]+")
PLANTILLA = re.compile(r"[\[\]{}<>]|=$|\.\.\.")
# Dominios que aparecen como ejemplo en los SKILL.md, no como fuente.
EJEMPLO = re.compile(r"^https?://([^/]*\.)?(example\.(com|org)|acme\.com|localhost|127\.0\.0\.1)(:\d+)?(/|$)")


def api_github(ruta):
    req = urllib.request.Request(f"https://api.github.com/{ruta}", headers={"User-Agent": UA})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def bajar(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read().decode("utf-8", "replace")


def skills_de(repo):
    """Devuelve {ruta: texto} de cada SKILL.md del repo del plugin."""
    info = api_github(f"repos/{repo}")
    rama = info["default_branch"]
    arbol = api_github(f"repos/{repo}/git/trees/{rama}?recursive=1")
    rutas = [n["path"] for n in arbol["tree"] if n["path"].endswith("SKILL.md")]
    return {p: bajar(f"https://raw.githubusercontent.com/{repo}/{rama}/{p}") for p in rutas}


def urls_de(texto):
    vistas = []
    for u in RE_URL.findall(texto):
        u = u.rstrip(".,;:*_")
        if PLANTILLA.search(u) or EJEMPLO.match(u) or u in vistas:
            continue
        vistas.append(u)
    return vistas


def probar(url):
    """Devuelve (estado, detalle). estado: ok | bloqueada | rota."""
    ultimo = None
    for _ in range(2):  # un reintento: los sitios .gob.ar a veces tardan
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                cuerpo = r.read(200_000)
                if "format=json" in url or "/api/" in url or "dolarapi" in url:
                    try:
                        datos = json.loads(cuerpo)
                    except ValueError:
                        return "rota", f"{r.status} pero no devolvió JSON"
                    if not datos:
                        return "rota", f"{r.status} con JSON vacío"
                return "ok", str(r.status)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403, 429):
                # Anti-bots (Imperva, Cloudflare): el sitio existe pero un agente
                # no lo puede leer. Avisamos aparte, no lo contamos como roto.
                return "bloqueada", str(e.code)
            ultimo = str(e.code)
            if e.code < 500:
                break
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError) as e:
            razon = getattr(e, "reason", e)
            ultimo = f"sin respuesta ({razon})"
    return "rota", ultimo


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reporte", default="reporte-fuentes.md")
    args = ap.parse_args()

    marketplace = json.loads((RAIZ / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    usos = {}  # url -> [(plugin, archivo)]
    for p in marketplace["plugins"]:
        src = p.get("source", {})
        if not isinstance(src, dict) or src.get("source") != "github":
            continue
        for ruta, texto in skills_de(src["repo"]).items():
            for u in urls_de(texto):
                usos.setdefault(u, []).append((p["name"], src["repo"], ruta))

    with ThreadPoolExecutor(max_workers=8) as pool:
        resultados = dict(zip(usos, pool.map(probar, usos)))

    por_estado = {"rota": [], "bloqueada": [], "ok": []}
    for u, (estado, detalle) in sorted(resultados.items()):
        por_estado[estado].append((u, detalle))

    lineas = [
        "# Chequeo de fuentes",
        "",
        f"{len(usos)} URLs en los SKILL.md: {len(por_estado['ok'])} ok, "
        f"{len(por_estado['rota'])} rotas, {len(por_estado['bloqueada'])} bloqueadas para agentes.",
    ]
    titulos = {
        "rota": "Rotas (arreglar: el agente le da al usuario un dato o link que no anda)",
        "bloqueada": "Bloqueadas para agentes (el sitio existe pero devuelve 401/403/429; buscar otra fuente para WebFetch)",
    }
    for estado, titulo in titulos.items():
        if not por_estado[estado]:
            continue
        lineas += ["", f"## {titulo}", ""]
        for u, detalle in por_estado[estado]:
            donde = ", ".join(f"[{n}](https://github.com/{r}/blob/HEAD/{f})" for n, r, f in usos[u])
            lineas.append(f"- `{detalle}` {u} (en {donde})")

    reporte = "\n".join(lineas) + "\n"
    Path(args.reporte).write_text(reporte, encoding="utf-8")
    print(reporte)
    return 1 if por_estado["rota"] else 0


if __name__ == "__main__":
    # 1 = hay fuentes rotas; 2 = el chequeo mismo falló (no abrir issue por eso).
    try:
        sys.exit(main())
    except Exception:
        import traceback

        traceback.print_exc()
        sys.exit(2)
