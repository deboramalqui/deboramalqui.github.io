"""Capturas de evidencia para la página de marcas. Sirve carpetas locales bajo un origen falso (sin servidor)
para que las rutas que empiezan en / funcionen. Salida: marcas/work/*.png (sin recortar)."""
import asyncio, mimetypes, os, pathlib, sys, urllib.parse
from playwright.async_api import async_playwright
OUT = "/Users/deboramalqui/Documents/Resume/portfolio/marcas/work"
C = "/Users/deboramalqui/Documents/Clients"; P = "/Users/deboramalqui/Documents/Resume/portfolio"

async def mount(ctx, origin, root):
    async def h(route):
        path = urllib.parse.unquote(urllib.parse.urlparse(route.request.url).path)
        p = pathlib.Path(root) / path.lstrip("/")
        if p.is_dir(): p = p / "index.html"
        if not p.exists(): return await route.fulfill(status=404, body="nf")
        ct = mimetypes.guess_type(str(p))[0] or "application/octet-stream"
        await route.fulfill(body=p.read_bytes(), content_type=ct)
    await ctx.route(f"{origin}/**", h)

JOBS = [  # (nombre, url, ancho, alto de ventana, full_page)
 ("medido-tablero", f"file://{C}/2026/medido/exploracion/tablero-direcciones-v1.html", 1200, 900, True),
 ("medido-conceptos2", f"file://{C}/2026/medido/exploracion/logo-conceptos-v2.html", 1200, 900, True),
 ("medido-anillo", f"file://{C}/2026/medido/exploracion/logo-o-anillo-tipografias.html", 1200, 900, True),
 ("medido-hueco", f"file://{C}/2026/medido/exploracion/logo-ajustes-hueco-vav.html", 1200, 900, True),
 ("medido-amarillo", f"file://{C}/2026/medido/exploracion/logo-colores-amarillo.html", 1200, 900, True),
 ("medido-entrega", f"file://{C}/2026/medido/exploracion/logo-entrega.html", 1200, 900, True),
 ("medido-manual", f"file://{C}/2026/medido/manual/manual-marca-medido-v1.html", 1200, 900, False),
 ("didi-original", f"file://{P}/exploracion/logo-didi-original-vs-vector.html", 1200, 900, True),
 ("didi-ajustes", f"file://{P}/exploracion/logo-didi-ajustes-v1.html", 1200, 900, True),
 ("didi-fondos", f"file://{P}/exploracion/logo-didi-y-fondos-v1.html", 1200, 900, True),
 ("didi-tipografia", f"file://{P}/exploracion/tipografia-d-sin-palo-v1.html", 1200, 900, True),
 ("didi-favicon", f"file://{P}/exploracion/favicon-didi-v1.html", 1200, 900, True),
 ("salto-tablero", f"file://{C}/2026/_el-salto-branding/tablero.html", 1200, 900, True),
]
MOUNTED = [  # (nombre, origen, raíz, ruta, ancho, alto, full_page)
 ("medido-web-en", "http://medido.test", f"{C}/2026/medido/preview", "/", 1280, 900, False),
 ("medido-web-he", "http://medido.test", f"{C}/2026/medido/preview", "/he/", 1280, 900, False),
 ("medido-web-movil", "http://medido.test", f"{C}/2026/medido/preview", "/", 390, 844, False),
 ("didi-sitio-es", "http://didi.test", f"{P}/sitio", "/es/", 1280, 900, False),
 ("didi-sitio-movil", "http://didi.test", f"{P}/sitio", "/es/", 390, 844, False),
]

async def shot(pg, name, full):
    await pg.wait_for_timeout(2500)
    try: await pg.evaluate("document.fonts.ready")
    except Exception: pass
    await pg.screenshot(path=f"{OUT}/{name}.png", full_page=full)
    h = await pg.evaluate("document.documentElement.scrollHeight")
    print(f"{name:20} ok  alto={h}", flush=True)

async def main():
    only = set(sys.argv[1:])
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--allow-file-access-from-files"])
        for name, url, w, h, full in JOBS:
            if only and name not in only: continue
            pg = await b.new_page(viewport={"width": w, "height": h})
            try:
                await pg.goto(url, wait_until="domcontentloaded", timeout=60000); await shot(pg, name, full)
            except Exception as e: print(name, "FALLO", str(e)[:120], flush=True)
            await pg.close()
        for name, origin, root, path, w, h, full in MOUNTED:
            if only and name not in only: continue
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
            await mount(ctx, origin, root)
            pg = await ctx.new_page()
            try:
                await pg.goto(origin + path, wait_until="domcontentloaded", timeout=60000); await shot(pg, name, full)
            except Exception as e: print(name, "FALLO", str(e)[:120], flush=True)
            await ctx.close()
        await b.close()
asyncio.run(main())
