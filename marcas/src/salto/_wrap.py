import asyncio, sys
from playwright.async_api import async_playwright
P="/Users/deboramalqui/Documents/Resume/portfolio/marcas/src/salto"; W="/Users/deboramalqui/Documents/Resume/portfolio/marcas/work"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--allow-file-access-from-files"])
        for n in ("hoja-exploracion-B-una-linea","verificacion-simetria-B","tipografias","propuestas-2","propuestas-5-C3"):
            open(f"{P}/_w-{n}.html","w").write(f'<body style="margin:0;background:#fff"><img id=i src="{n}.svg" style="width:1200px;display:block">')
            pg=await b.new_page(viewport={"width":1200,"height":1200})
            await pg.goto(f"file://{P}/_w-{n}.html",wait_until="load",timeout=90000)
            await pg.wait_for_timeout(1500)
            ok=await pg.evaluate("document.getElementById('i').naturalWidth")
            await pg.screenshot(path=f"{W}/salto-{n}.png",timeout=120000); print(n,"naturalWidth",ok,flush=True)
            await pg.close()
        await b.close()
asyncio.run(main())
