"""Inserta los logotipos vectoriales en el manual. Uso: python3 manual/build_manual.py"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
T = {k: open(os.path.join(RAIZ, "logo", "svg", f"offmenu-{k}-plantilla.svg")).read() for k in ("logotipo", "apilado", "simbolo-off")}
src = open(os.path.join(AQUI, "manual-src.html")).read()
open(os.path.join(AQUI, "offmenu-manual.html"), "w").write(src.replace("__LOGOS__", json.dumps(T)))
print("manual/offmenu-manual.html")
