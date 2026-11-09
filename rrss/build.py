"""Inserta los logotipos vectoriales en las plantillas de redes. Uso: python3 rrss/build.py"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
T = {k: open(os.path.join(RAIZ, "logo", "svg", f"offmenu-{k}-plantilla.svg")).read() for k in ("logotipo", "apilado", "simbolo-off")}
for src in ("posts-src.html", "reels-src.html", "estrategia-src.html"):
    p = os.path.join(AQUI, src)
    if os.path.exists(p):
        out = p.replace("-src.html", ".html" if src.startswith("estrategia") else "-build.html")
        open(out, "w").write(open(p).read().replace("__LOGOS__", json.dumps(T)))
        print(os.path.relpath(out, RAIZ))
