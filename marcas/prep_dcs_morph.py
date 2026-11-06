"""Capas alineadas para la animación «del clavel al símbolo» (Red Española de Danzas Circulares).
Todas las capas comparten un lienzo de 1200 × 1200 con fondo transparente, así se apilan exactas en la página.
El logo, la línea y el nombre salen del vector original (Logos-wf.ai, mesa 12, la versión entregada): SVG nítido,
con el contorno azul del mismo grosor en todo el dibujo. La foto y la síntesis siguen en WebP.
Salida: img/dcs-m-color.svg, -lineas.svg, -texto.svg, dcs-m-foto.webp, -poster.webp, img/dcs-exploracion.webp
y dcs-m-centro.json (centro de la flor en % del lienzo)."""
import os, re, json
import numpy as np
import pymupdf
from PIL import Image, ImageFilter
D = "/Users/deboramalqui/Documents/Clients/2024/Red de Focalizadores de DCS en España"
B = os.path.dirname(os.path.abspath(__file__)); O = os.path.join(B, "img"); S = 1200
NAVY = "#002f49"
doc = pymupdf.open(f"{D}/Logos-wf.ai"); pg = doc[12]
# caja de todo el dibujo (flor + nombre), medida en un render con transparencia
z = 4; pix = pg.get_pixmap(matrix=pymupdf.Matrix(z, z), alpha=True)
al = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 4)[..., 3]
ys, xs = np.nonzero(al > 10); bx0, bx1, by0, by1 = xs.min() / z, (xs.max() + 1) / z, ys.min() / z, (ys.max() + 1) / z
k = 1040 / max(bx1 - bx0, by1 - by0)
ox, oy = (S - (bx1 - bx0) * k) / 2 - bx0 * k, (S - (by1 - by0) * k) / 2 - by0 * k
# la flor: unión de las formas (el contorno azul exterior incluido)
fl = pymupdf.Rect(); [fl.include_rect(d["rect"]) for d in pg.get_drawings()]
cx, cy, r = (fl.x0 + fl.x1) / 2 * k + ox, (fl.y0 + fl.y1) / 2 * k + oy, max(fl.width, fl.height) / 2 * k
# piezas del SVG que exporta PyMuPDF: glifos en <defs>, la flor en <path>, el nombre en <use>
svg = pg.get_svg_image(text_as_path=True)
defs = re.search(r"<defs>(.*?)</defs>", svg, re.S).group(1)
body = svg[svg.index("</defs>") + 7:svg.rindex("</svg>")]
uses = "\n".join(re.findall(r"<use [^>]*/>", body))
flor = re.sub(r' inkscape:\w+="[^"]*"', "", re.sub(r"<use [^>]*/>\n?", "", body))   # sin el espacio de nombres de Inkscape
W, H = pg.rect.width, pg.rect.height
def write(name, inner, d=""):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {S} {S}" width="{S}" height="{S}">'
         f'<defs>{d}</defs><g transform="matrix({k:.6f},0,0,{k:.6f},{ox:.4f},{oy:.4f})">{inner}</g></svg>')
    open(f"{O}/dcs-m-{name}.svg", "w").write(s); print(name, len(s) // 1024, "KB")
write("color", flor, defs)
write("texto", uses, defs)
# solo la línea: una máscara donde el azul visible es blanco y todo color que lo tapa es negro; el interior queda transparente
mask = re.sub(r'fill="(#[0-9a-fA-F]{6})"', lambda m: 'fill="#fff"' if m.group(1).lower() == NAVY else 'fill="#000"', flor)
write("lineas", f'<rect width="{W}" height="{H}" fill="{NAVY}" mask="url(#solo-linea)"/>',
      defs + f'<mask id="solo-linea" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">{mask}</mask>')
layers = {}
# foto del clavel, centrada y del mismo tamaño que la flor del logo
f = Image.open(f"{D}/case_/FLOR.png").convert("RGBA"); fa = np.asarray(f)[..., 3]
pys, pxs = np.nonzero(fa > 40); pcx, pcy = (pxs.min() + pxs.max()) / 2, (pys.min() + pys.max()) / 2; pr = max(pxs.max() - pxs.min(), pys.max() - pys.min()) / 2
kp = r * 1.04 / pr; fw, fh = round(f.width * kp), round(f.height * kp)
foto = Image.new("RGBA", (S, S), (0, 0, 0, 0)); foto.alpha_composite(f.resize((fw, fh), Image.LANCZOS), (round(cx - pcx * kp), round(cy - pcy * kp)))
layers["foto"] = foto
# síntesis: cada píxel de la foto toma el color más cercano de la paleta de la marca, con formas planas
pal = np.array([(0xD6, 0x27, 0x29), (0xA8, 0x16, 0x2A), (0xF7, 0x7F, 0x00), (0xFD, 0xBF, 0x4A), (0xE9, 0xE2, 0xB6), (0x00, 0x2F, 0x49)], np.float32)
rgb = np.asarray(foto.convert("RGB").filter(ImageFilter.MedianFilter(11))).astype(np.float32); fa2 = np.asarray(foto)[..., 3]
w = np.array([1.0, 1.25, 0.8], np.float32)                                                 # el verde pesa más: separa rosa de rojo
d2 = (((rgb[:, :, None, :] - pal[None, None, :, :]) * w) ** 2).sum(-1); d2[..., 5] *= 2.2  # el azul solo en las sombras más hondas
idx = d2.argmin(-1)
post = np.zeros((S, S, 4), np.uint8); post[..., :3] = pal[idx].astype(np.uint8); post[..., 3] = np.where(fa2 > 60, 255, 0)
layers["poster"] = Image.fromarray(post, "RGBA").filter(ImageFilter.SMOOTH_MORE)
for n, im in layers.items():
    im.save(f"{O}/dcs-m-{n}.webp", "WEBP", quality=90, method=6); print(n, os.path.getsize(f"{O}/dcs-m-{n}.webp") // 1024, "KB")
# exploración propia: la ronda de personas y el molinete de pétalos (mesas 5 y 3 del archivo de Illustrator)
canvas = Image.new("RGB", (1200, 800), (255, 255, 255)); x = 40
for ab in (5, 3):
    p = doc[ab]; zz = 520 / max(p.rect.width, p.rect.height); px = p.get_pixmap(matrix=pymupdf.Matrix(zz, zz), alpha=False)
    im = Image.frombytes("RGB", (px.width, px.height), px.samples); canvas.paste(im, (x, (800 - im.height) // 2)); x += 560
canvas.save(f"{O}/dcs-exploracion.webp", "WEBP", quality=85, method=6)
json.dump({"cx": round(cx / S * 100, 3), "cy": round(cy / S * 100, 3), "r": round(r / S * 100, 3)}, open(f"{O}/dcs-m-centro.json", "w"))
print("centro %", round(cx / S * 100, 2), round(cy / S * 100, 2), "radio %", round(r / S * 100, 2))
