"""Genera manual/pdf-build.html (para imprimir a PDF) a partir de pdf-src.html.
Uso: python3 manual/build_pdf.py && node manual/render_pdf.js"""
import json, os, re
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
T = {k: open(os.path.join(RAIZ, "logo", "svg", f"offmenu-{k}-plantilla.svg")).read() for k in ("logotipo", "apilado", "simbolo-off")}
manual = open(os.path.join(AQUI, "manual-src.html")).read()
css = re.search(r"<style>(.*?)</style>", manual, re.S).group(1)
src = open(os.path.join(AQUI, "pdf-src.html")).read()
out = src.replace("__CSS__", css).replace("__LOGOS__", json.dumps(T))
open(os.path.join(AQUI, "pdf-build.html"), "w").write(out)
print("manual/pdf-build.html")
