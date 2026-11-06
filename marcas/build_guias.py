"""Genera la pestaña Guidelines de la sección Brands: los manuales de Kol como libros que se hojean.

Uso:
  python3 build_guias.py --render   convierte las páginas de los PDF en imágenes (guias/<libro>/NNN.webp)
                                     y una tira de miniaturas por libro (guias/<libro>/miniaturas.webp)
  python3 build_guias.py            escribe guidelines.html (vista local, junto a index.html)
  python3 build_guias.py --site     además escribe la versión del sitio en sitio-src/extra/marcas/

Páginas ocultas (HIDE): las que tienen datos internos del cliente o un teléfono. Para mostrarlas, sacarlas de la lista.
"""
import base64, colorsys, html, io, json, os, re, shutil, sys
from PIL import Image

B = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, B)
from comun import header_html, HEADER_CSS

KOL = "/Users/deboramalqui/Documents/Clients/2026/kol"
FONTS = os.path.join(os.path.dirname(B), "fuentes")
PAGE_W, THUMB_W, COLS = 1280, 160, 10

BOOKS = [
    dict(id="kol-franquicias", title="Kol Franquicias", sub="Guía de marca, versión 3", year="2026", accent="#C51172",
         what="El sistema de diseño de la red de franquicias de Kol: concepto y voz, lockup, color, tipografía, formas, espaciado, componentes, estados y movimiento, y cómo se aplica en la web.",
         pdf=KOL + "/franquicia/branding/guia/guia-marca-franquicia-presentacion-v3a-2026-10-06.pdf",
         chapters=[("Portada", 1), ("Índice", 2), ("1 · Concepto y voz", 3), ("2 · Lockup", 6), ("3 · Color", 9), ("4 · Tipografía", 16),
                   ("5 · Formas", 21), ("6 · Espaciado", 25), ("7 · Componentes", 30), ("8 · Estados y movimiento", 37),
                   ("9 · Casos de UI", 42), ("Anexo · Qué cambió", 56), ("Cierre", 66)],
         hide=[50, 51, 52, 53, 54, 55], hide_why="preguntas internas para Kol con cifras sin confirmar"),
    dict(id="kol-accesorios", title="Kol Accesorios", sub="Guía de marca para redes, versión 7", year="2026", accent="#EC2992",
         what="Cómo se ve y cómo habla Kol en Instagram: logo, color, tipografía, formas y sellos, composición, foto y video, reels, siete pilares de contenido y voz.",
         pdf=KOL + "/retail/guia-redes/GUIA-DE-MARCA-REDES-KOL-RETAIL-v7.pdf",
         chapters=None, hide=[191, 209], hide_why="un teléfono de la marca"),
]

def gdir(book): return os.path.join(B, "guias", book["id"])

# ---------------------------------------------------------------- render
def render():
    import fitz
    for bk in BOOKS:
        d = fitz.open(bk["pdf"]); n = d.page_count; os.makedirs(gdir(bk), exist_ok=True)
        z = PAGE_W / d[0].rect.width; th = []
        for i in range(n):
            out = os.path.join(gdir(bk), f"{i + 1:03d}.webp")
            pix = d[i].get_pixmap(matrix=fitz.Matrix(z, z), alpha=False)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            if not os.path.exists(out): im.save(out, "WEBP", quality=72, method=5)
            th.append(im.resize((THUMB_W, round(THUMB_W * im.height / im.width)), Image.LANCZOS))
            if (i + 1) % 25 == 0: print(bk["id"], i + 1, "/", n, flush=True)
        tw, thh = th[0].size; rows = (n + COLS - 1) // COLS
        sheet = Image.new("RGB", (COLS * tw, rows * thh), (240, 240, 240))
        for k, t in enumerate(th): sheet.paste(t, ((k % COLS) * tw, (k // COLS) * thh))
        sheet.save(os.path.join(gdir(bk), "miniaturas.webp"), "WEBP", quality=62, method=5)
        json.dump({"n": n, "w": PAGE_W, "h": round(PAGE_W * d[0].rect.height / d[0].rect.width), "tw": tw, "th": thh, "cols": COLS,
                   "toc": [(t[1], t[2]) for t in d.get_toc() if t[0] == 1]}, open(os.path.join(gdir(bk), "datos.json"), "w"))
        print(bk["id"], "listo:", n, "páginas", flush=True)

def tab_color(bk, page):
    """Color dominante y saturado de la página que abre el capítulo: así cada pestaña toma el color de su capítulo."""
    im = Image.open(os.path.join(gdir(bk), f"{page:03d}.webp")).convert("RGB").resize((96, 54))
    best, score = None, 0
    counts = {}
    for c in im.getdata():
        h, s, v = colorsys.rgb_to_hsv(*(x / 255 for x in c))
        if s < .35 or v < .35: continue
        k = (c[0] // 24, c[1] // 24, c[2] // 24); counts[k] = counts.get(k, 0) + 1
    if counts:
        k = max(counts, key=counts.get)
        if counts[k] > 20: return "#%02X%02X%02X" % tuple(min(255, x * 24 + 12) for x in k)
    return bk["accent"]

# ---------------------------------------------------------------- HTML
def font_face(file, family, weight):
    b64 = base64.b64encode(open(os.path.join(FONTS, file), "rb").read()).decode()
    return f'@font-face{{font-family:"{family}";src:url(data:font/woff2;base64,{b64}) format("woff2");font-weight:{weight};font-display:swap}}'

def data_for(bk):
    meta = json.load(open(os.path.join(gdir(bk), "datos.json")))
    ch = bk["chapters"] or [(t, p) for t, p in meta["toc"]]
    chapters = [{"t": t, "p": p, "c": tab_color(bk, p)} for t, p in ch]
    shown = [p for p in range(1, meta["n"] + 1) if p not in bk["hide"]]
    return {"id": bk["id"], "title": bk["title"], "sub": bk["sub"], "year": bk["year"], "what": bk["what"], "accent": bk["accent"],
            "n": meta["n"], "pages": shown, "hidden": len(bk["hide"]), "hideWhy": bk["hide_why"],
            "w": meta["w"], "h": meta["h"], "tw": meta["tw"], "th": meta["th"], "cols": meta["cols"], "chapters": chapters,
            "dir": f"guias/{bk['id']}/"}

CSS = r"""
/* Concepto: una mesa oscura donde los manuales se ven como objetos. Cerrados muestran su grosor; abiertos se hojean como un libro. */
:root{
  --bg:#0F1B2D; --bg-2:#0B1424; --panel:#13213A; --panel-2:#172744; --line:#2B3A52;
  --fg:#E6ECF5; --muted:#AAB7C9; --accent:#70B4F4; --accent-ink:#0F1B2D; --paper:#F7F5F1; --edge:#D9D4CB; --edge-line:#BDB6AA;
  --table:#0A1322;
  --sans:"DiDi Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; --mono:"DiDi Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  color-scheme:dark;
}
@media (prefers-color-scheme: light){ :root:not([data-theme="dark"]){
  --bg:#F3F5F9; --bg-2:#E8ECF3; --panel:#FFFFFF; --panel-2:#EEF1F7; --line:#D3DAE6; --fg:#0F1B2D; --muted:#4A5A70;
  --accent:#1F5FA8; --accent-ink:#FFFFFF; --table:#DCE2EC; color-scheme:light } }
:root[data-theme="light"]{
  --bg:#F3F5F9; --bg-2:#E8ECF3; --panel:#FFFFFF; --panel-2:#EEF1F7; --line:#D3DAE6; --fg:#0F1B2D; --muted:#4A5A70;
  --accent:#1F5FA8; --accent-ink:#FFFFFF; --table:#DCE2EC; color-scheme:light }
*{box-sizing:border-box}
*{font-feature-settings:"ss20" 1 !important}
body{margin:0;background:var(--bg);color:var(--fg);font:400 1.0625rem/1.55 var(--sans);-webkit-font-smoothing:antialiased}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);background:var(--bg);z-index:30}
img{display:block;max-width:100%}
a{color:inherit}
button{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.only-light{display:none}
@media (prefers-color-scheme: light){ :root:not([data-theme="dark"]) .only-light{display:block} :root:not([data-theme="dark"]) .only-dark{display:none} }
:root[data-theme="light"] .only-light{display:block} :root[data-theme="light"] .only-dark{display:none}
.wrap{width:100%;max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}

.intro{padding-block:clamp(36px,7vw,80px) 8px}
.eyebrow{font:400 .75rem/1.2 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.intro h1{font:800 clamp(2.3rem,6.5vw,4.25rem)/1.02 var(--sans);letter-spacing:-.025em;margin:12px 0 18px;max-width:17ch;text-wrap:balance}
.intro p{max-width:60ch;color:var(--muted);font-size:1.1875rem;margin:0}

/* la mesa con los libros cerrados */
.shelf{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(24px,5vw,64px);margin-top:44px;padding:clamp(28px,5vw,64px) clamp(20px,4vw,56px);border-radius:24px;background:radial-gradient(120% 90% at 50% 0%,var(--panel-2),var(--table))}
@media (max-width:760px){ .shelf{grid-template-columns:minmax(0,1fr)} }
.tome{all:unset;cursor:pointer;display:grid;gap:18px;min-width:0}
.tome:focus-visible{outline:2px solid var(--accent);outline-offset:8px;border-radius:8px}
.tome-obj{position:relative;perspective:1600px;padding-right:var(--thick)}
.tome-3d{position:relative;transform:rotateY(-18deg) rotateX(4deg);transform-origin:left center;transform-style:preserve-3d;transition:transform .5s cubic-bezier(.2,0,0,1)}
.tome:hover .tome-3d,.tome:focus-visible .tome-3d{transform:rotateY(-8deg) rotateX(2deg) translateY(-6px)}
.tome-cover{position:relative;border-radius:3px 6px 6px 3px;overflow:hidden;box-shadow:0 30px 60px -20px rgba(0,0,0,.65),0 8px 18px rgba(0,0,0,.35);background:var(--paper)}
.tome-cover img{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
.tome-cover::after{content:"";position:absolute;inset:0 auto 0 0;width:18px;background:linear-gradient(90deg,rgba(0,0,0,.35),rgba(0,0,0,0))}
.tome-edge{position:absolute;top:3px;bottom:3px;right:calc(var(--thick) * -1);width:var(--thick);transform:rotateY(90deg);transform-origin:left center;
  background:repeating-linear-gradient(90deg,var(--edge) 0 2px,var(--edge-line) 2px 3px);border-radius:0 3px 3px 0}
.tome-foot{position:absolute;left:3px;right:0;bottom:calc(var(--thick) * -1);height:var(--thick);transform:rotateX(-90deg);transform-origin:top center;
  background:repeating-linear-gradient(180deg,var(--edge) 0 2px,var(--edge-line) 2px 3px)}
.tome-tabs{position:absolute;top:6%;bottom:6%;right:calc(var(--thick) * -1 - 8px);width:10px;display:flex;flex-direction:column;justify-content:space-between}
.tome-tabs i{display:block;height:max(4px,calc(100% / var(--nt) - 3px));border-radius:0 3px 3px 0}
.tome-meta{display:grid;gap:4px}
.tome-meta b{font:800 1.5rem/1.15 var(--sans);letter-spacing:-.01em}
.tome-meta span{color:var(--muted);font-size:.9375rem}
.tome-meta .count{font:400 .8125rem/1.3 var(--mono);color:var(--fg);letter-spacing:.04em}
.tome-meta .open{justify-self:start;margin-top:8px;font:600 .9375rem/1 var(--sans);padding:12px 18px;border-radius:999px;background:var(--accent);color:var(--accent-ink)}

/* el libro abierto */
.reader{position:fixed;inset:0;z-index:50;display:none;flex-direction:column;background:radial-gradient(130% 100% at 50% 20%,#1A2B47,#060B14);color:#E6ECF5;
  padding:max(10px,env(safe-area-inset-top,0px)) max(12px,env(safe-area-inset-right,0px)) max(10px,env(safe-area-inset-bottom,0px)) max(12px,env(safe-area-inset-left,0px))}
.reader.is-open{display:flex}
.r-top{display:flex;align-items:center;gap:12px;min-height:48px}
.r-title{min-width:0;display:flex;flex-direction:column}
.r-title b{font:800 1.125rem/1.2 var(--sans)}
.r-title small{font:400 .75rem/1.3 var(--mono);color:#AAB7C9;letter-spacing:.05em;text-transform:uppercase;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.r-close{all:unset;margin-left:auto;cursor:pointer;font:600 .9375rem/1 var(--sans);padding:11px 16px;border-radius:999px;border:1px solid rgba(255,255,255,.25)}
.r-close:focus-visible{outline:2px solid #70B4F4;outline-offset:2px}
.r-stage{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;position:relative;touch-action:pan-y}
.book{position:relative;--pw:min(calc(100vw - 230px),calc((100vh - 250px) * 16 / 9),1240px);width:var(--pw);aspect-ratio:16/9;perspective:2600px}
@media (max-width:820px){ .book{--pw:min(calc(100vw - 54px),calc((100vh - 290px) * 16 / 9))} }
.sheet{position:absolute;inset:0;border-radius:2px 5px 5px 2px;overflow:hidden;background:var(--paper) center/cover no-repeat;box-shadow:0 40px 80px -30px rgba(0,0,0,.8),0 10px 24px rgba(0,0,0,.45)}
.sheet img{width:100%;height:100%;object-fit:cover}
.sheet::after{content:"";position:absolute;inset:0 auto 0 0;width:22px;background:linear-gradient(90deg,rgba(0,0,0,.28),rgba(0,0,0,0));pointer-events:none}
.stack{position:absolute;top:4px;bottom:4px;background:repeating-linear-gradient(90deg,#E5E0D7 0 2px,#B9B2A6 2px 3px);transition:width .35s ease}
.stack.r{left:100%;border-radius:0 4px 4px 0;box-shadow:6px 8px 18px rgba(0,0,0,.35)}
.stack.l{right:100%;border-radius:4px 0 0 4px;box-shadow:-6px 8px 18px rgba(0,0,0,.35)}
.leaf{position:absolute;inset:0;transform-origin:left center;transform-style:preserve-3d;z-index:3;pointer-events:none}
.leaf .face{position:absolute;inset:0;backface-visibility:hidden;border-radius:2px 5px 5px 2px;overflow:hidden;background:var(--paper) center/cover no-repeat}
.leaf .face img{width:100%;height:100%;object-fit:cover}
.leaf .back{transform:rotateY(180deg);background:linear-gradient(90deg,#ECE8E0,#F7F5F1 60%,#E3DED5)}
.leaf .shade{position:absolute;inset:0;pointer-events:none;background:linear-gradient(90deg,rgba(0,0,0,0),rgba(0,0,0,.25));opacity:0}
.tabs{position:absolute;top:3%;bottom:3%;left:calc(100% + var(--rt, 0px) + 2px);display:flex;flex-direction:column;justify-content:flex-start;gap:3px;z-index:4}
.tab{all:unset;cursor:pointer;display:flex;align-items:center;gap:8px;height:var(--th);min-height:14px;padding:0 10px 0 8px;border-radius:0 7px 7px 0;
  background:var(--c);color:#fff;font:600 .75rem/1 var(--sans);white-space:nowrap;max-width:46px;overflow:hidden;transition:max-width .25s ease,transform .2s ease;box-shadow:3px 2px 8px rgba(0,0,0,.35)}
.tab .tn{font:400 .6875rem/1 var(--mono);opacity:.95}
.tab:hover,.tab:focus-visible,.tab.is-on{max-width:240px;transform:translateX(4px)}
.tab:focus-visible{outline:2px solid #fff;outline-offset:1px}
.tab.dark{color:#0F1B2D}
@media (max-width:820px){ .tabs{display:none} }
.chips{display:none;gap:6px;overflow-x:auto;scrollbar-width:none;padding:6px 2px}
.chips::-webkit-scrollbar{display:none}
@media (max-width:820px){ .chips{display:flex} }
.chip{all:unset;cursor:pointer;flex:none;font:600 .8125rem/1 var(--sans);padding:9px 12px;border-radius:999px;border-left:6px solid var(--c);background:rgba(255,255,255,.08)}
.chip.is-on{background:rgba(255,255,255,.22)}
.chip:focus-visible{outline:2px solid #70B4F4;outline-offset:2px}
.nav{all:unset;cursor:pointer;flex:none;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.1);font:400 1.375rem/1 var(--sans);z-index:5}
.nav:hover{background:rgba(255,255,255,.2)}
.nav:focus-visible{outline:2px solid #70B4F4;outline-offset:2px}
.r-bottom{display:grid;gap:8px;padding-top:10px}
.r-status{display:flex;gap:12px;align-items:center;flex-wrap:wrap;font:400 .8125rem/1.3 var(--mono);color:#AAB7C9}
.r-status b{color:#fff;font:600 .9375rem/1 var(--sans)}
.r-range{width:100%;accent-color:#70B4F4;height:28px}
.strip{display:flex;gap:6px;overflow-x:auto;scroll-behavior:smooth;padding:4px 2px 8px;scrollbar-color:rgba(255,255,255,.3) transparent}
.thumb{all:unset;cursor:pointer;flex:none;width:96px;aspect-ratio:16/9;border-radius:3px;background-repeat:no-repeat;outline:2px solid transparent;opacity:.72;transition:opacity .15s,transform .15s}
.thumb:hover{opacity:1;transform:translateY(-2px)}
.thumb.is-on{opacity:1;outline-color:#70B4F4}
.thumb:focus-visible{outline-color:#fff}
.zoom-note{font:400 .75rem/1.3 var(--mono);color:#7F8DA3}
.hint{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font:600 .9375rem/1.3 var(--sans);background:rgba(0,0,0,.6);padding:10px 14px;border-radius:999px;pointer-events:none;opacity:0;transition:opacity .4s}
.hint.on{opacity:1}
footer{margin-top:clamp(48px,8vw,96px);border-top:1px solid var(--line);padding-block:24px 48px;color:var(--muted);font-size:.875rem}
footer .wrap{display:flex;gap:12px 32px;flex-wrap:wrap;justify-content:space-between}
.note{color:var(--muted);font-size:.9375rem;margin-top:18px}
@media (prefers-reduced-motion: reduce){ .tome-3d,.stack,.tab,.thumb{transition:none} }
"""

JS = r"""
(function(){
const BOOKS = JSON.parse(document.getElementById('books').textContent);
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = (s, r=document) => r.querySelector(s);
const reader = $('#reader'), sheet = $('#sheet'), book = $('#book'), tabsEl = $('#tabs'), chipsEl = $('#chips'), strip = $('#strip'), range = $('#range');
let B = null, idx = 0, busy = false, lastFocus = null;
const src = (p) => B.dir + String(p).padStart(3,'0') + '.webp';
function thumbPos(p, w){ const k = p-1, s = w / B.tw; return { size: `${B.cols*B.tw*s}px auto`, pos: `${-(k % B.cols)*B.tw*s}px ${-Math.floor(k / B.cols)*B.th*s}px` }; }
function chapterOf(p){ let c = B.chapters[0]; for (const ch of B.chapters) if (ch.p <= p) c = ch; return c; }
function isDark(hex){ const n=parseInt(hex.slice(1),16), r=n>>16&255, g=n>>8&255, b=n&255; return (0.299*r+0.587*g+0.114*b) > 170; }
function placeholder(el, p){ const t = thumbPos(p, el.clientWidth || 800); el.style.backgroundImage = `url(${B.dir}miniaturas.webp)`; el.style.backgroundSize = t.size; el.style.backgroundPosition = t.pos; }
function setSheet(p){ placeholder(sheet, p); const img = sheet.querySelector('img'); img.src = src(p); img.alt = `Página ${p} de ${B.n}: ${chapterOf(p).t}`; preload(p); }
function preload(p){ const i = B.pages.indexOf(p); [1,2,-1].forEach(d => { const q = B.pages[i+d]; if (q){ const im = new Image(); im.src = src(q); } }); }
function stacks(){ const maxT = Math.min(34, 6 + B.n * 0.13), done = idx / Math.max(1, B.pages.length-1);
  $('#stack-r').style.width = Math.max(2, maxT * (1-done)) + 'px'; $('#stack-l').style.width = Math.max(idx ? 2 : 0, maxT * done) + 'px';
  book.style.setProperty('--rt', Math.max(2, maxT*(1-done)) + 'px'); }
function status(){ const p = B.pages[idx], ch = chapterOf(p);
  $('#st-page').textContent = `Página ${p} de ${B.n}`; $('#st-ch').textContent = ch.t; range.value = idx;
  document.querySelectorAll('.tab,.chip').forEach(t => t.classList.toggle('is-on', +t.dataset.p === ch.p));
  const th = strip.children[idx]; strip.querySelectorAll('.is-on').forEach(x => x.classList.remove('is-on'));
  if (th){ th.classList.add('is-on'); const s = th.offsetLeft - strip.clientWidth/2 + th.clientWidth/2; strip.scrollTo({left: s, behavior: RM ? 'auto' : 'smooth'}); }
  const chip = chipsEl.querySelector('.is-on'); if (chip) chipsEl.scrollTo({left: chip.offsetLeft - 20, behavior: 'auto'});
  stacks(); }
function go(to, animate){
  to = Math.max(0, Math.min(B.pages.length-1, to)); if (to === idx || busy) { if (!busy && to === idx) status(); return; }
  const from = idx, fwd = to > from, step = Math.abs(to-from) === 1;
  if (!animate || RM || !step){ idx = to; setSheet(B.pages[idx]); status(); return; }
  busy = true;
  const leaf = document.createElement('div'); leaf.className = 'leaf';
  const pFront = fwd ? B.pages[from] : B.pages[to];
  leaf.innerHTML = `<div class="face"><img alt="" src="${src(pFront)}"></div><div class="face back"></div><div class="shade"></div>`;
  placeholder(leaf.firstChild, pFront);
  book.appendChild(leaf);
  if (fwd){ idx = to; setSheet(B.pages[idx]); }
  const kf = fwd ? [{transform:'rotateY(0deg)'},{transform:'rotateY(-180deg)'}] : [{transform:'rotateY(-180deg)'},{transform:'rotateY(0deg)'}];
  const a = leaf.animate(kf, {duration: 720, easing: 'cubic-bezier(.3,.1,.2,1)'});
  leaf.querySelector('.shade').animate([{opacity:0},{opacity:1,offset:.5},{opacity:0}], {duration: 720});
  a.onfinish = () => { leaf.remove(); if (!fwd){ idx = to; setSheet(B.pages[idx]); } busy = false; status(); };
  if (!fwd){ /* el destino aparece cuando la hoja termina de volver */ }
  status();
}
function build(b){
  B = b; idx = 0; reader.style.setProperty('--acc', B.accent);
  $('#r-name').textContent = `${B.title} · ${B.sub}`; $('#r-meta').textContent = `${B.n} páginas · ${B.chapters.length} pestañas` ;
  const nt = B.chapters.length; book.style.setProperty('--th', `calc((100% - ${(nt-1)*3}px) / ${nt})`);
  tabsEl.innerHTML = ''; chipsEl.innerHTML = '';
  B.chapters.forEach((ch, i) => {
    const num = (ch.t.match(/^([0-9.]+|Anexo)/)||[''])[0] || (i===0 ? '·' : '');
    const label = ch.t.replace(/^([0-9.]+\s*·?\s*)/, '');
    const t = document.createElement('button'); t.className = 'tab' + (isDark(ch.c) ? ' dark' : ''); t.style.setProperty('--c', ch.c); t.dataset.p = ch.p;
    t.innerHTML = `<span class="tn">${num || '•'}</span><span>${label}</span>`; t.setAttribute('aria-label', `Ir a ${ch.t}, página ${ch.p}`);
    t.onclick = () => jumpTo(ch.p); tabsEl.appendChild(t);
    const c = document.createElement('button'); c.className = 'chip'; c.style.setProperty('--c', ch.c); c.dataset.p = ch.p; c.textContent = ch.t; c.onclick = () => jumpTo(ch.p); chipsEl.appendChild(c);
  });
  strip.innerHTML = '';
  B.pages.forEach((p, i) => { const t = document.createElement('button'); t.className = 'thumb'; t.setAttribute('aria-label', `Página ${p}`);
    const tp = thumbPos(p, 96); t.style.backgroundImage = `url(${B.dir}miniaturas.webp)`; t.style.backgroundSize = tp.size; t.style.backgroundPosition = tp.pos;
    t.onclick = () => go(i, Math.abs(i-idx) === 1); strip.appendChild(t); });
  range.max = B.pages.length-1; range.value = 0; range.setAttribute('aria-label', `Hojear: página de 1 a ${B.n}`);
  setSheet(B.pages[0]); status();
}
function jumpTo(p){ let i = B.pages.indexOf(p); if (i < 0) i = B.pages.findIndex(q => q > p); go(i, false); }
function open(id, fromEl){
  const b = BOOKS.find(x => x.id === id); if (!b) return; lastFocus = fromEl || document.activeElement;
  build(b); reader.classList.add('is-open'); document.body.style.overflow = 'hidden'; $('#r-close').focus();
  if (location.hash !== '#' + id) history.replaceState(null, '', '#' + id);
  if (!RM){ const h = $('#hint'); setTimeout(() => go(1, true), 380); h.classList.add('on'); setTimeout(() => h.classList.remove('on'), 2600); }
}
/* Dos flujos al cerrar: quien llegó desde Just for fun vuelve a la lista de guías; quien llegó desde la Campaign Suite (?desde=suite) vuelve a la suite. */
const DESDE = new URLSearchParams(location.search).get('desde');
if (DESDE === 'suite') { const c = $('#r-close'); if (c) c.textContent = '← Volver a la suite'; }
function close(){
  if (DESDE === 'suite') { if (history.length > 1 && document.referrer) history.back(); else location.href = '../index.html'; return; }
  reader.classList.remove('is-open'); document.body.style.overflow = ''; history.replaceState(null, '', location.pathname); if (lastFocus) lastFocus.focus(); }
document.querySelectorAll('[data-book]').forEach(el => el.addEventListener('click', () => open(el.dataset.book, el)));
$('#r-close').onclick = close;
$('#prev').onclick = () => go(idx-1, true); $('#next').onclick = () => go(idx+1, true);
range.addEventListener('input', () => go(+range.value, false));
sheet.addEventListener('click', e => { const r = sheet.getBoundingClientRect(); go(idx + ((e.clientX - r.left) > r.width/2 ? 1 : -1), true); });
document.addEventListener('keydown', e => { if (!reader.classList.contains('is-open')) return;
  if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight') go(idx+1, true); else if (e.key === 'ArrowLeft') go(idx-1, true);
  else if (e.key === 'Home') go(0, false); else if (e.key === 'End') go(B.pages.length-1, false);
  else if (e.key === 'PageDown' || e.key === 'PageUp'){ const p = B.pages[idx], cs = B.chapters.map(c => c.p); const n = e.key === 'PageDown' ? cs.find(c => c > p) : [...cs].reverse().find(c => c < chapterOf(p).p || (c < p && c !== chapterOf(p).p)); if (n) jumpTo(n); e.preventDefault(); } });
let sx = null; const stage = $('#stage');
stage.addEventListener('pointerdown', e => { sx = e.clientX; });
stage.addEventListener('pointerup', e => { if (sx === null) return; const dx = e.clientX - sx; sx = null; if (Math.abs(dx) > 50){ go(idx + (dx < 0 ? 1 : -1), true); e.preventDefault(); } });
const h = location.hash.slice(1); if (h && BOOKS.some(b => b.id === h)) open(h);
})();
"""

def page_html(site, artifact=False):
    books = [data_for(b) for b in BOOKS]
    fonts = "".join([font_face("DiDiSans-Regular.woff2", "DiDi Sans", 400), font_face("DiDiSans-Medium.woff2", "DiDi Sans", 500),
                     font_face("DiDiSans-Bold.woff2", "DiDi Sans", 700), font_face("DiDiSans-ExtraBold.woff2", "DiDi Sans", 800),
                     font_face("DiDiMono-Regular.woff2", "DiDi Mono", 400)])
    tomes = ""
    for b in books:
        thick = round(min(46, 8 + b["n"] * 0.16))
        tabs = "".join(f'<i style="background:{c["c"]}"></i>' for c in b["chapters"])
        tomes += (f'<button type="button" class="tome" data-book="{b["id"]}" aria-label="Abrir {html.escape(b["title"])}, {html.escape(b["sub"])}, {b["n"]} páginas">'
                  f'<div class="tome-obj" style="--thick:{thick}px;--nt:{len(b["chapters"])}"><div class="tome-3d"><div class="tome-cover"><img src="{b["dir"]}001.webp" alt="" loading="lazy"></div>'
                  f'<div class="tome-edge"></div><div class="tome-foot"></div><div class="tome-tabs">{tabs}</div></div></div>'
                  f'<div class="tome-meta"><span class="count">{b["n"]} páginas · {len(b["chapters"])} capítulos · {b["year"]}</span><b>{html.escape(b["title"])}</b>'
                  f'<span>{html.escape(b["sub"])}. {html.escape(b["what"])}</span><span class="open">Abrir el libro</span></div></button>')
    hidden_note = " ".join(f"En {b['title']} se omiten {b['hidden']} páginas: {b['hideWhy']}." for b in books if b["hidden"])
    if artifact:
        from comun import LIVE, ARTIFACT_LOGOS
        hdr = header_html(False, "guidelines", main_base=LIVE + "es/", logos_href=ARTIFACT_LOGOS, guides_href="#top")
    else:
        hdr = header_html(site, "guidelines")
    body = f'''{hdr}
<main id="top"><div class="wrap">
  <section class="intro">
    <p class="eyebrow">Débora Malqui · Guías de marca</p>
    <h1>Dos manuales de marca, para hojear.</h1>
    <p>Los escribí y diseñé para Kol: uno para la red de franquicias y otro para las redes de sus locales. Son largos a propósito: cada decisión tiene su lámina. Abrí cualquiera y pasá las páginas, saltá por las pestañas o deslizá por la tira de miniaturas.</p>
  </section>
  <div class="shelf">{tomes}</div>
</div></main>
<footer><div class="wrap"><span>Guías de marca de Débora Malqui para Kol, 2026.</span>{'<a href="../es/sobre-mi.html">Volver a Sobre mí</a>' if site else ''}</div></footer>

<div class="reader" id="reader" role="dialog" aria-modal="true" aria-labelledby="r-name">
  <div class="r-top"><div class="r-title"><b id="r-name"></b><small id="r-meta"></small></div><button type="button" class="r-close" id="r-close">Cerrar</button></div>
  <div class="chips" id="chips" aria-label="Capítulos"></div>
  <div class="r-stage" id="stage">
    <div class="book" id="book">
      <div class="stack l" id="stack-l"></div>
      <div class="sheet" id="sheet"><img alt=""></div>
      <div class="stack r" id="stack-r"></div>
      <div class="tabs" id="tabs" aria-label="Capítulos"></div>
    </div>
    <div class="hint" id="hint">Pasá las páginas con las flechas, tocá una pestaña o deslizá abajo</div>
  </div>
  <div class="r-bottom">
    <div class="r-status"><button type="button" class="nav prev" id="prev" aria-label="Página anterior">‹</button><button type="button" class="nav next" id="next" aria-label="Página siguiente">›</button><b id="st-page"></b><span id="st-ch"></span></div>
    <input type="range" class="r-range" id="range" min="0" value="0" step="1">
    <div class="strip" id="strip" aria-label="Todas las páginas"></div>
  </div>
</div>
<script type="application/json" id="books">{json.dumps(books, ensure_ascii=False)}</script>
<script>{JS}</script>'''
    title = "Guidelines · Débora Malqui" if site else "Guías de marca de Kol"
    head = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
            f'<title>{title}</title><meta name="description" content="Dos manuales de marca diseñados para Kol, el de la red de franquicias y el de las redes de los locales, para hojear como libros.">'
            f'<meta name="theme-color" content="#0F1B2D">')
    if site:
        from comun import meta_site
        head += meta_site("guidelines.html", title, "Dos manuales de marca diseñados para Kol, el de la red de franquicias y el de las redes de los locales, para hojear como libros.")
        head += '<link rel="icon" href="../assets/favicon.ico" sizes="any"><link rel="icon" type="image/svg+xml" href="../assets/favicon-32.svg">'
    css = CSS + HEADER_CSS
    if site:
        css = re.sub(r'@media \(prefers-color-scheme: light\)\{.*?\} \}', '', css, flags=re.S)
        head += '<meta name="color-scheme" content="dark">'
    if artifact:   # el visor de artefactos agrega su propio esqueleto
        return f'<title>Guías de marca de Kol</title><meta name="claude:viewport-fit-sides" content="cover"><style>{fonts}{css}</style>' + body
    return head + f"<style>{fonts}{css}</style></head><body>" + body + "</body></html>"

def main():
    if "--render" in sys.argv: render()
    open(os.path.join(B, "guidelines.html"), "w").write(page_html(site=False))
    open(os.path.join(B, "guidelines-artifact.html"), "w").write(page_html(site=False, artifact=True))
    print("guidelines.html listo")
    if "--site" in sys.argv:
        dest = os.path.join(os.path.dirname(B), "sitio-src", "extra", "marcas")
        os.makedirs(dest, exist_ok=True)
        open(os.path.join(dest, "guidelines.html"), "w").write(page_html(site=True))
        gd = os.path.join(dest, "guias")
        if os.path.exists(gd): shutil.rmtree(gd)
        for bk in BOOKS:
            os.makedirs(os.path.join(gd, bk["id"]))
            keep = {f"{p:03d}.webp" for p in data_for(bk)["pages"]} | {"miniaturas.webp"}
            for f in keep: shutil.copyfile(os.path.join(gdir(bk), f), os.path.join(gd, bk["id"], f))
        print("sitio-src/extra/marcas/guidelines.html y guias/ listos")

if __name__ == "__main__":
    main()
