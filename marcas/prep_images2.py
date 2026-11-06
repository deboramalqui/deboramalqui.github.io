"""Segunda parte: composiciones de El Salto, recortes de Danzas Circulares, logos finales a marcas/logos/."""
import os, shutil
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
B = "/Users/deboramalqui/Documents/Resume/portfolio/marcas"; W = B + "/work"; S = B + "/src"; O = B + "/img"; L = B + "/logos"
os.makedirs(L, exist_ok=True)
def save(im, path, maxw=1200, q=80, alpha=False):
    im = im.convert("RGBA" if alpha else "RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(path, "WEBP", quality=q, method=6); print(f"{os.path.basename(path):34} {im.size} {os.path.getsize(path)//1024} KB")

# ---- El Salto: composiciones 3:2 de las pantallas de la presentación + hojas de exploración ----
def pair(a, b, name, bg=(225, 232, 244)):
    ims = [Image.open(f"{S}/salto/{f}").convert("RGB") for f in (a, b)]
    h = 760; ims = [i.resize((round(i.width * h / i.height), h), Image.LANCZOS) for i in ims]
    c = Image.new("RGB", (1200, 800), bg); x = (1200 - (ims[0].width + ims[1].width + 36)) // 2
    for i in ims: c.paste(i, (x, 20)); x += i.width + 36
    save(c, f"{O}/{name}.webp")
pair("03 Lectura semántica.png", "03 Contraste y decisión.png", "salto-1-lectura")
pair("04 Dos propuestas.png", "05 Favicon y versión en azul.png", "salto-6-propuestas")
for n, f, y in (("salto-3-tipografias", "tipografias", 0), ("salto-4-hoja-B", "hoja-exploracion-B-una-linea", 0), ("salto-5-simetria", "verificacion-simetria-B", 200), ("salto-5b-taza", "propuestas-5-C3", 0)):
    im = Image.open(f"{W}/salto-{f}.png").convert("RGB"); save(im.crop((0, y, 1200, y + 800)), f"{O}/{n}.webp")

# ---- Danzas Circulares: recortes que NO incluyen nombres ni teléfonos ----
c = Image.open(f"{S}/dcs/case.png").convert("RGB")
save(c.crop((0, 80, 2080, 1467)), f"{O}/dcs-sistema.webp"); save(c.crop((260, 2740, 1860, 3806)), f"{O}/dcs-simbolo.webp")
r = Image.open(f"{S}/dcs/remera.png").convert("RGB"); save(r.crop((250, 1180, 2950, 2980)), f"{O}/dcs-remera.webp")
p = Image.open(f"{S}/dcs/directo al corzon-redes sociales 1.png").convert("RGB"); save(p, f"{O}/dcs-redes.webp", 1000)
# paleta real del logo entregado
lg = Image.open(f"{S}/dcs/red - colores y fondo transparente.png").convert("RGBA")
print("size logo", lg.size)
bg = Image.open(f"{S}/dcs/directo al corzon-redes sociales 1.png").convert("RGB")
print("crema", "#%02X%02X%02X" % bg.getpixel((200, 3000)))
import collections
px = [q[:3] for q in lg.resize((200, 185)).getdata() if q[3] > 250]
cnt = collections.Counter((q[0] // 8 * 8, q[1] // 8 * 8, q[2] // 8 * 8) for q in px)
print("colores dominantes", ["#%02X%02X%02X" % k + f"({v})" for k, v in cnt.most_common(8)])

# ---- logos finales ----
cp = lambda src, dst: shutil.copyfile(src, f"{L}/{dst}")
for grp, files in {"didi": ["didi-logo.svg", "didi-logo-apilado.svg", "didi-logo-una-tinta-clara.svg", "didi-logo-una-tinta-oscura.svg", "didi-monograma-Di.svg", "didi-favicon-32.svg", "didi-favicon-16.svg"],
                   "medido": ["medido-logo-sobre-blanco.svg", "medido-logo-sobre-negro.svg", "medido-logo-sobre-amarillo.svg", "medido-he-sobre-negro.svg", "medido-he-sobre-blanco.svg", "medido-logo-un-color-negro.svg", "medido-logo-un-color-blanco.svg", "medido-anillo-sobre-negro.svg", "medido-favicon.svg", "medido-avatar-lupa.svg"],
                   "salto": ["El-Salto-B-color.svg", "El-Salto-B-reverso.svg", "El-Salto-C-color.svg", "El-Salto-C-reverso.svg", "favicon-B-azul-64.svg", "favicon-B-azul-32.svg", "favicon-B-azul-16.svg", "favicon-C-blanco-64.svg", "favicon-C-blanco-32.svg", "favicon-C-blanco-16.svg"]}.items():
    for f in files: cp(f"{S}/{grp}/{f}", f)
for f in ("didi-entrada.gif",): cp(f"{S}/didi/{f}", f)
for n, f in (("grooming-horizontal", "logo grooming latam redes-01.jpg"), ("grooming-vertical", "GL.png"), ("grooming-nombre", "logo grooming latam redes-04.jpg"), ("grooming-latinoamerica", "logo Grooming LATINOAMERICA-02.jpg")):
    save(Image.open(f"{S}/grooming/{f}"), f"{L}/{n}.webp", 900, 88)
for n, f in (("dcs-color", "red - colores y fondo transparente.png"), ("dcs-lineal", "red-lineal y fondo transparente.png"), ("dcs-festival", "Directo al corazon - rojo - RGB.png"), ("dcs-festival-linea", "festival.png")):
    save(Image.open(f"{S}/dcs/{f}"), f"{L}/{n}.webp", 900, 90, alpha=True)
print("gif", os.path.getsize(f"{L}/didi-entrada.gif") // 1024, "KB")
