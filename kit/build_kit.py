"""Genera favicon.svg y la foto de perfil (SVG) a partir de las plantillas del logotipo.
Uso: python3 kit/build_kit.py && node kit/render_kit.js"""
import os, re
AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(AQUI)
def interior(nombre):
    s = open(os.path.join(RAIZ, "logo", "svg", nombre)).read()
    vb = list(map(float, re.search(r'viewBox="([^"]+)"', s).group(1).split()))
    inner = s[s.index('>') + 1:s.rindex('</svg>')].replace('fill="currentColor"', 'fill="#FFFFFF"').replace('style="fill:var(--line,#F5302A)"', 'fill="#F5302A"')
    return vb, inner
def cuadrado(nombre, ancho_rel, salida, ajuste_x=0.0):
    (x, y, w, h), inner = interior(nombre); S = 2048; iw = S * ancho_rel; ih = iw * h / w
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}"><rect width="{S}" height="{S}" fill="#42000E"/>'
           f'<svg x="{(S - iw) / 2 + S * ajuste_x:.1f}" y="{(S - ih) / 2:.1f}" width="{iw:.1f}" height="{ih:.1f}" viewBox="{x:.0f} {y:.0f} {w:.0f} {h:.0f}">{inner}</svg></svg>')
    open(os.path.join(AQUI, salida), "w").write(svg)
cuadrado("offmenu-simbolo-off-plantilla.svg", 0.74, "favicon/favicon.svg")
cuadrado("offmenu-apilado-plantilla.svg", 0.56, "perfil/offmenu-perfil-instagram.svg", 0.012)
print("kit/favicon/favicon.svg · kit/perfil/offmenu-perfil-instagram.svg")
