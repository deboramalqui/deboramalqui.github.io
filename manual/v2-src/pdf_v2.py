"""Saca manual/manual-didi-v2.pdf del HTML, en A4 y con Chromium, como el PDF de la v1.
Uso: python3 manual/v2-src/pdf_v2.py (después de build_manual_v2.py). Con --publico usa la versión pública y escribe manual-didi-v2-publico.pdf."""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
M=pathlib.Path(__file__).resolve().parent.parent
N='manual-didi-v2-publico' if '--publico' in sys.argv else 'manual-didi-v2'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1200,'height':900})
        await pg.goto((M/f'{N}.html').as_uri(),wait_until='networkidle')
        # las capturas van con carga diferida: se piden todas antes de imprimir
        await pg.evaluate("Promise.all([...document.images].map(i=>{i.loading='eager';return i.complete?0:new Promise(r=>{i.onload=i.onerror=r})}))")
        await pg.evaluate("document.fonts.ready")
        await pg.emulate_media(media='print')
        await pg.pdf(path=str(M/f'{N}.pdf'),format='A4',print_background=True,margin={'top':'0','bottom':'0','left':'0','right':'0'})
        await b.close()
asyncio.run(main())
