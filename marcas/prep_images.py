"""Recortes y conversión a webp para la página de marcas. Entrada: marcas/work/*.png y marcas/src/**. Salida: marcas/img/*.webp.
Los recortes de capturas son 3:2 (1200×800) para que las filas del camino sean iguales."""
import asyncio, os, sys, io
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
B = "/Users/deboramalqui/Documents/Resume/portfolio/marcas"; W = B + "/work"; S = B + "/src"; O = B + "/img"
os.makedirs(O, exist_ok=True)

def save(im, name, maxw=1200, q=80):
    im = im.convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(f"{O}/{name}.webp", "WEBP", quality=q, method=6); print(f"{name:26} {im.size} {os.path.getsize(O+'/'+name+'.webp')//1024} KB")

def crop(src, name, box, maxw=1200, q=80):
    im = Image.open(src); im.load(); save(im.crop(box), name, maxw, q)

# ---- capturas de exploración (3:2) ----
C = {  # nombre: (archivo, y0)   → recorte (0,y0,1200,y0+800)
 "medido-1-tablero": ("medido-tablero", 2220), "medido-2-conceptos": ("medido-conceptos2", 250),
 "medido-3-anillo": ("medido-anillo", 380), "medido-4-color": ("medido-amarillo", 120),
 "medido-5-hueco": ("medido-hueco", 0), "medido-6-entrega": ("medido-entrega", 300),
 "didi-1-original": ("didi-original", 262), "didi-2-ajustes": ("didi-ajustes", 660),
 "didi-3-fondos": ("didi-fondos", 260), "didi-4-tipografia": ("didi-tipografia", 138), "didi-5-favicon": ("didi-favicon", 0),
 "salto-tablero": ("salto-tablero", 0),
}
for n, (f, y) in ([] if "--solo-grooming" in sys.argv else C.items()): crop(f"{W}/{f}.png", n, (0, y, 1200, y + 800))
if '--solo-grooming' not in sys.argv: crop(f"{W}/medido-web-en.png", "medido-web-en", (0, 0, 1280, 853)); crop(f"{W}/medido-web-he.png", "medido-web-he", (0, 0, 1280, 853))
crop(f"{W}/didi-sitio-es.png", "didi-sitio-es", (0, 0, 1280, 853))
for n in ("medido-web-movil", "didi-sitio-movil"): save(Image.open(f"{W}/{n}.png"), n, 390)

# ---- El Salto: presentación y hojas de exploración (SVG → png con Chrome) ----
P = "/Users/deboramalqui/Documents/Resume/portfolio/marcas/src/salto"
for n, f in (("salto-propuestas", "04 Dos propuestas.png"), ("salto-favicon", "05 Favicon y versión en azul.png")):
    im = Image.open(f"{P}/{f}"); print(n, im.size); save(im, n, 700)
# (las hojas SVG de El Salto se renderizan aparte: son muy pesadas)

# ---- Grooming LATAM: páginas del manual de marca ----
import fitz
d = fitz.open("/Users/deboramalqui/Documents/Clients/2024/Grooming /DÉBORA/MANUAL DE MARCA GL.pdf")
for i, n in ((3, "signo"), (4, "modulo"), (5, "zona-minima"), (6, "variaciones-paleta"), (7, "inhibidas-tipografia"), (11, "ejemplo-en-uso")):
    pix = d[i].get_pixmap(matrix=fitz.Matrix(1.8, 1.8)); im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    print("manual", i + 1, im.size); save(im, f"grooming-manual-{n}", 1200)
