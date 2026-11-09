"""Genera el logotipo de OFFMENU como vectores a partir de los contornos de Schibsted Grotesk Black.

La línea que tacha OFF es la prolongación exacta del brazo central de las F:
misma altura y mismo grosor, leídos del propio glifo. Se recorta de las letras
y se dibuja aparte, así que no depende de cómo cada navegador coloque el texto.

Uso: python3 logo/build_logo.py   (requiere fonttools, skia-pathops, uharfbuzz)
"""
import os
import pathops
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.transformPen import TransformPen

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTE = os.path.join(AQUI, "fuente", "SchibstedGrotesk-Black.ttf")
SALIDA = os.path.join(AQUI, "svg")

GRANATE, ROJO, BLANCO, NEGRO = "#42000E", "#F5302A", "#FFFFFF", "#141518"
TRACKING = -0.05      # igual que el letter-spacing del sistema
SOBRESALE = 0.10      # la línea sobresale a la izquierda de la O (en em)
INTERLINEA = 0.82     # versión apilada

font = TTFont(FUENTE)
UPM = font["head"].unitsPerEm
CAP = font["OS/2"].sCapHeight
glyphset = font.getGlyphSet()
blob = hb.Blob.from_file_path(FUENTE)
hbfont = hb.Font(hb.Face(blob))

# Brazo central de la F, leído del contorno: los dos valores intermedios de y
rec = RecordingPen()
glyphset[font.getBestCmap()[ord("F")]].draw(rec)
ys = sorted({pt[1] for _, args in rec.value for pt in args})
ARM_BOTTOM, ARM_TOP = ys[1], ys[2]
ARM_END = max(pt[0] for _, args in rec.value for pt in args if ARM_BOTTOM <= pt[1] <= ARM_TOP and pt[1] in (ARM_BOTTOM, ARM_TOP))
EPS = round(UPM * 0.004)  # solape mínimo para que no aparezcan juntas


def shape(texto):
    """Devuelve [(glifo, x)] con kerning de HarfBuzz y el tracking del sistema."""
    buf = hb.Buffer()
    buf.add_str(texto)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": False})
    x, out = 0, []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        out.append((font.getGlyphName(info.codepoint), x + pos.x_offset))
        x += pos.x_advance + TRACKING * UPM
    return out, x


def glyph_path(nombre, dx, dy=0):
    p = pathops.Path()
    glyphset[nombre].draw(TransformPen(p.getPen(), (1, 0, 0, 1, dx, dy)))
    return p


def rect(x0, y0, x1, y1):
    p = pathops.Path()
    pen = p.getPen()
    pen.moveTo((x0, y0)); pen.lineTo((x1, y0)); pen.lineTo((x1, y1)); pen.lineTo((x0, y1)); pen.closePath()
    return p


def linea_para(glifos, dy=0):
    """Rectángulo de la línea para la palabra OFF de una fila ya maquetada."""
    o_nombre, o_x = glifos[0]
    o_left = o_x + font["hmtx"][o_nombre][1]
    f2_nombre, f2_x = glifos[2]
    x0 = o_left - SOBRESALE * UPM
    x1 = f2_x + ARM_END
    return (x0, ARM_BOTTOM + dy, x1, ARM_TOP + dy)


def construir(filas):
    """filas: lista de textos (cada uno en su línea). La primera empieza por OFF."""
    letras = pathops.Path()
    linea = None
    ancho = 0
    for i, texto in enumerate(filas):
        dy = -i * INTERLINEA * UPM
        glifos, adv = shape(texto)
        ancho = max(ancho, adv - TRACKING * UPM)
        for nombre, x in glifos:
            letras = pathops.op(letras, glyph_path(nombre, x, dy), pathops.PathOp.UNION)
        if texto.startswith("OFF") and linea is None:
            linea = linea_para(glifos, dy)
    x0, y0, x1, y1 = linea
    hueco = rect(x0, y0, x1, y1)
    letras = pathops.op(letras, hueco, pathops.PathOp.DIFFERENCE)
    barra = rect(x0, y0 - EPS, x1 + EPS, y1 + EPS)
    return letras, barra, x0, ancho, len(filas)


def d(path):
    pen = SVGPathPen(None)
    path.draw(pen)
    return pen.getCommands()


def svg(filas, color_letras, color_linea, fondo=None, margen=0.12):
    letras, barra, x0, ancho, n = construir(filas)
    m = margen * UPM
    top = CAP + m
    alto = CAP + (n - 1) * INTERLINEA * UPM + 2 * m
    izq = x0 - m
    w = ancho - x0 + 2 * m
    fondo_svg = f'<rect x="{izq}" y="{-top}" width="{w}" height="{alto}" fill="{fondo}"/>' if fondo else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{izq:.0f} {-top:.0f} {w:.0f} {alto:.0f}" role="img" aria-label="OFFMENU">'
            f'{fondo_svg}<g transform="scale(1,-1)">'
            f'<path fill="{color_letras}" d="{d(letras)}"/>'
            f'<path fill="{color_linea}" d="{d(barra)}"/></g></svg>')


VARIANTES = {
    # nombre: (letras, línea, fondo)
    "blanco-sobre-granate": (BLANCO, ROJO, GRANATE),
    "granate-sobre-blanco": (GRANATE, ROJO, BLANCO),
    "blanco-sobre-negro": (BLANCO, ROJO, NEGRO),
    "granate-sobre-rojo": (GRANATE, GRANATE, ROJO),
}
FORMAS = {"logotipo": ["OFFMENU"], "simbolo-off": ["OFF"], "apilado": ["OFF", "MENU"]}

if __name__ == "__main__":
    os.makedirs(SALIDA, exist_ok=True)
    for forma, filas in FORMAS.items():
        for var, (cl, cline, bg) in VARIANTES.items():
            with open(os.path.join(SALIDA, f"offmenu-{forma}-{var}.svg"), "w") as fh:
                fh.write(svg(filas, cl, cline, bg))
            with open(os.path.join(SALIDA, f"offmenu-{forma}-{var}-transparente.svg"), "w") as fh:
                fh.write(svg(filas, cl, cline, None))
    print("brazo F:", ARM_BOTTOM, ARM_TOP, "fin:", ARM_END, "upm:", UPM)
    print("generados en", SALIDA)


def plantilla(filas):
    """SVG sin márgenes para usar en línea: letras en currentColor y línea en var(--line)."""
    letras, barra, x0, ancho, n = construir(filas)
    alto = CAP + (n - 1) * INTERLINEA * UPM
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {-CAP:.0f} {ancho - x0:.0f} {alto:.0f}" role="img" aria-label="OFFMENU">'
            f'<g transform="scale(1,-1)"><path fill="currentColor" d="{d(letras)}"/>'
            f'<path style="fill:var(--line,{ROJO})" d="{d(barra)}"/></g></svg>')


if __name__ == "__main__":
    for forma, filas in FORMAS.items():
        with open(os.path.join(SALIDA, f"offmenu-{forma}-plantilla.svg"), "w") as fh:
            fh.write(plantilla(filas))
    print("relación alto/em de la mayúscula:", CAP / UPM)
