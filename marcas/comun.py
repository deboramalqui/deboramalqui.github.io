"""Piezas compartidas de la sección Brands (Logos y Guidelines): la barra con el menú del sitio y el submenú."""

LIVE = "https://deboramalqui.github.io/"
ARTIFACT_LOGOS = "https://claude.ai/artifact/VnthFpDFXkucVjFKd2USSw"
ARTIFACT_GUIDES = "https://claude.ai/artifact/1KNDm2WKVDaiFo5MNdD1Kg"

def meta_site(page, title, desc, lang="es"):
    """og:image absoluta (la tarjeta general del sitio), og:url y canonical de una página de la sección Brands publicada en /marcas/."""
    import html as _h
    url = f"{LIVE}marcas/{page}"; img = f"{LIVE}assets/og/portada.jpg"
    return (f'<link rel="canonical" href="{url}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:locale" content="es_AR">'
            f'<meta property="og:title" content="{_h.escape(title, quote=True)}"><meta property="og:description" content="{_h.escape(desc, quote=True)}">'
            f'<meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{img}">')

def header_html(site, active, main_base=None, logos_href="index.html", guides_href="guidelines.html"):
    """Menú principal del sitio arriba (para ir a donde quiera la persona) y submenú Logos | Guidelines abajo.
    site=True: enlaces relativos del sitio (../es/...). Vista previa: main_base=LIVE+'es/' y las pestañas apuntan a los artefactos."""
    if site: main_base = "../es/"
    cur = lambda k: ' aria-current="page"' if k == active else ""
    main = ""
    if main_base:
        main = (f'<nav class="mainnav" aria-label="Sitio"><a href="{main_base}index.html#casos">Casos</a>'
                f'<a href="{main_base}sobre-mi.html" class="is-section">Sobre mí</a><a href="{main_base}contacto.html">Contacto</a></nav>')
    home = f"{main_base}index.html" if main_base else "index.html"
    # 29/10/2026: esta sección existe solo en español; desde el sitio en inglés o hebreo se avisa y se ofrece volver a Sobre mí en ese idioma.
    note = ('<nav class="langnote" aria-label="Idioma"><span lang="es">Solo en español</span>'
            '<a href="../en/sobre-mi.html" lang="en" hreflang="en" translate="no">English</a>'
            '<a href="../he/sobre-mi.html" lang="he" hreflang="he" translate="no">עברית</a></nav>') if site else ""
    return (f'<header class="bar"><div class="wrap bar-main"><a class="brand" href="{home}" aria-label="DiDí, inicio">'
            '<img class="only-dark" src="logos/didi-logo.svg" alt="DiDí"><img class="only-light" src="logos/didi-logo-una-tinta-oscura.svg" alt="DiDí"></a>'
            f'{main}</div>'
            '<div class="subbar"><div class="wrap bar-sub"><span class="sublabel">Just for fun · Brands</span>'
            f'<nav class="subnav" aria-label="Brands"><a href="{logos_href}"{cur("logos")}>Logos</a><a href="{guides_href}"{cur("guidelines")}>Guidelines</a></nav>'
            f'{note}</div></div></header>')

HEADER_CSS = r"""
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--bg);border-bottom:1px solid var(--line)}
.bar .wrap.bar-main{display:flex;align-items:center;gap:16px;min-height:56px}
.bar .brand img{height:26px;width:auto}
.bar .mainnav{display:flex;gap:4px;overflow-x:auto;min-width:0;scrollbar-width:none;margin-left:auto}
.bar .mainnav a{white-space:nowrap;text-decoration:none;color:var(--muted);font:500 .9375rem/1 var(--sans);padding:12px 12px;border-radius:999px}
.bar .mainnav a:hover{color:var(--fg);background:var(--panel)}
.bar .mainnav a.is-section{color:var(--fg)}
.subbar{border-top:1px solid var(--line);background:var(--bg-2)}
.bar .wrap.bar-sub{display:flex;align-items:center;gap:8px 18px;min-height:52px;flex-wrap:wrap;padding-block:6px}
.sublabel{font:400 .75rem/1.2 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.bar .subnav{display:flex;gap:6px;margin-left:0;overflow:visible}
.bar .subnav a{white-space:nowrap;text-decoration:none;color:var(--fg);font:600 .9375rem/1 var(--sans);padding:10px 16px;border-radius:999px;border:1px solid var(--line)}
.bar .subnav a:hover{border-color:var(--accent)}
.bar .subnav a[aria-current="page"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.langnote{display:flex;align-items:center;gap:6px;margin-left:auto;font:400 .75rem/1.2 var(--mono);letter-spacing:.04em;color:var(--muted)}
.langnote span{margin-right:4px}
.langnote a{white-space:nowrap;text-decoration:none;color:var(--fg);font:600 .8125rem/1 var(--sans);padding:9px 12px;border-radius:999px;border:1px solid var(--line)}
.langnote a:hover{border-color:var(--accent)}
@media(max-width:600px){.langnote{margin-left:0;width:100%}}
.case{scroll-margin-top:124px}
"""
