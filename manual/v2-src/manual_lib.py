"""Funciones del generador del manual DiDí: color, contraste, logo, íconos y demos de componentes."""
import pathlib, re, html
ROOT=pathlib.Path(__file__).resolve().parent.parent.parent
UI_CSS=(ROOT/'marca'/'didi-ui.css').read_text()

# ---------- color ----------
def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def lum(h):
    r,g,b=[c/255 for c in hx(h)]; f=lambda x: x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def ratio(a,b):
    la,lb=lum(a),lum(b); return (max(la,lb)+0.05)/(min(la,lb)+0.05)
def mix(a,b,t): A,B=hx(a),hx(b); return '#%02X%02X%02X'%tuple(round(A[i]*(1-t)+B[i]*t) for i in range(3))
def css_var(name):
    m=re.search(rf'--{name}:\s*(#[0-9A-Fa-f]{{6}})',UI_CSS); return m.group(1).upper()
SURF=css_var('d-surface')
LOGO={'rosa':'#E890CC','celeste':'#80ECEC','amarillo':'#DCD060','azul':'#70B4F4','verde':'#ACEC84'}
FUNC=[('rosa','accion','Acción','D abierta'),('celeste','nav','Navegación y foco','Barra'),('amarillo','atencion','Atención','D abierta (a la derecha)'),('azul','dato','Dato','Barra, radio 0'),('verde','ok','Verificado','Píldora')]
SURFS=[('surface','Superficie base'),('dim','Hundida (fondo del documento)'),('lowest','Contenedor más bajo'),('low','Contenedor bajo'),('container','Contenedor'),('high','Contenedor alto'),('highest','Contenedor más alto')]
SURF_HEX={k:css_var(f'd-{k}') for k,_ in SURFS}
def cell(r,kind='text'):
    if r>=4.5: cls='m-pass'; t='texto'
    elif r>=3: cls='m-pass'; t='gráfico'
    else: cls='m-fail'; t='no'
    return f'<td class="n {cls}">{r:.1f}:1 <span style="opacity:.7">{t}</span></td>'
def contrast_matrix():
    heads=''.join(f'<th>{k}</th>' for k,_ in SURFS)
    rows=[]
    for nombre,hexa in [(f'{n} {LOGO[n]}',LOGO[n]) for n,_,_,_ in FUNC]+[('texto #E6ECF5','#E6ECF5'),('texto variante #AAB7C9','#AAB7C9'),('contorno #6A809E',css_var('d-outline'))]:
        rows.append(f'<tr><td><span class="m-sw" style="background:{hexa}"></span>{nombre}</td>'+''.join(cell(ratio(hexa,SURF_HEX[k])) for k,_ in SURFS)+'</tr>')
    return f'<div style="overflow-x:auto"><table class="m-t" style="min-width:820px"><tr><th>Color sobre →</th>{heads}</tr>{"".join(rows)}</table></div>'

def tonal_block():
    out=[]
    for n,k,label,forma in FUNC:
        cont=css_var(f'd-{k}-cont'); on=css_var(f'd-on-{k}-cont'); c=LOGO[n]
        out.append(f'<div class="m-swatch" style="background:{cont};color:{on}"><b>{label}</b>contenedor {cont}<br>texto {on} · {ratio(on,cont):.1f}:1<br>borde/acento {c}</div>')
    return '<div class="m-swatches">'+''.join(out)+'</div>'
def func_table():
    rows=[]
    desc={'accion':'Lo que te pido que hagas: el botón «Escribime», el botón flotante de contacto, el cierre de cada caso, «Listo» en las hojas. Es la primera D: la que abre. En los casos, además, marca el tipo <b>Campañas</b>.',
          'nav':'Dónde estás y qué está activo: ítem actual, idioma elegido, migas, enlaces, índice del caso, anillo de foco. Es la primera barra: marca posición. En los casos, además, marca el tipo <b>Producto</b>.',
          'atencion':'Lo que hay que mirar: aviso, dato destacado, progreso, el único error. Es la segunda D, abierta a la derecha: señala. En los casos, además, marca el tipo <b>UX</b>.',
          'dato':'Lo medido: cifras, metadatos, campos, tablas, código. Es la segunda barra: contenido, no decoración. En los casos, además, marca los <b>trabajos académicos</b>.',
          'ok':'Lo comprobado: verificado, en vivo, disponible. Es el acento, chico e inclinado: el detalle que confirma. En los casos, además, marca el tipo <b>Automatización</b>.'}
    use={'accion':'Un botón relleno por vista. Nunca para estados.','nav':'Nunca como fondo de texto largo. Los enlaces son siempre celestes, también dentro de un caso de otro color.','atencion':'Siempre con ícono o texto, nunca solo color.','dato':'Siempre radio 0. Cifras en mono o tabulares.','ok':'Como estado, solo si hay algo comprobado detrás. Como tipo, solo en detalles del caso.'}
    for n,k,label,forma in FUNC:
        c=LOGO[n]
        rows.append(f'<tr><td><span class="m-sw" style="background:{c}"></span><b>{label}</b><br><code>{n} {c}</code><br><code>--d-{k}</code></td><td>{desc[k]}</td><td>{forma}</td><td>{use[k]}</td><td class="n">{ratio(c,SURF):.1f}:1 sobre superficie<br>{ratio(SURF,c):.1f}:1 texto oscuro encima</td></tr>')
    return '<table class="m-t"><tr><th>Color</th><th>Función</th><th>Forma</th><th>Regla</th><th>Contraste</th></tr>'+''.join(rows)+'</table>'
def surface_swatches():
    out=[]
    for k,label in SURFS:
        v=SURF_HEX[k]; fg='#E6ECF5'
        out.append(f'<div class="m-swatch" style="background:{v};color:{fg};box-shadow:inset 0 0 0 1px #2B3A52"><b>--d-{k}</b>{v}<br>{label}<br>{ratio(fg,v):.1f}:1 texto</div>')
    return '<div class="m-swatches">'+''.join(out)+'</div>'
def tokens_pre():
    m=re.search(r':root,\.didi\{(.*?)\n\}',UI_CSS,re.S); t=':root,.didi{'+m.group(1)+'\n}'
    # comentarios en español y sin el nombre de la base de componentes (regla 3 del sitio)
    for x,y in (('(escala M3 + las tres formas del logo)','(escala de radios + las tres formas del logo)'),('(M3: hover 8, foco 12, presionado 12, arrastre 16)','(al pasar el mouse 8, foco 12, presionado 12, arrastre 16)'),('movimiento (M3)','movimiento')): t=t.replace(x,y)
    return html.escape(t)

# ---------- logo ----------
def _paths(c,variant='full'):
    d1='M0 2 H67 A95 95 0 0 1 67 192 H0 V172 H67 A75 75 0 0 0 67 22 H0 Z'
    d2='M210 2 H241 A95 95 0 0 1 241 192 H210 V172 H241 A75 75 0 0 0 241 22 H210 Z'
    return (f'<path fill="{c["rosa"]}" fill-rule="evenodd" d="{d1}"/><rect fill="{c["celeste"]}" x="169" y="97" width="20" height="95"/>'
            f'<path fill="{c["amarillo"]}" fill-rule="evenodd" d="{d2}"/><rect fill="{c["azul"]}" x="343" y="97" width="20" height="95"/>'
            f'<rect fill="{c["verde"]}" x="338.36" y="55.04" width="46" height="20" rx="10" transform="rotate(-50 361.36 65.04)"/>')
def logo(c=None,w=160,extra=''):
    c=c or LOGO; return f'<svg class="d-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 193" width="{w}" style="height:auto;display:block;{extra}" role="img" aria-label="DiDí">{_paths(c)}</svg>'
def mono(ink): return {k:ink for k in LOGO}
def logo_stacked(c=None,w=110):
    c=c or LOGO
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 212 406" width="{w}" style="height:auto;display:block" role="img" aria-label="DiDí apilado">'
      f'<path fill="{c["rosa"]}" fill-rule="evenodd" d="M0 2 H67 A95 95 0 0 1 67 192 H0 V172 H67 A75 75 0 0 0 67 22 H0 Z"/><rect fill="{c["celeste"]}" x="169" y="97" width="20" height="95"/>'
      f'<path fill="{c["amarillo"]}" fill-rule="evenodd" d="M36 214 H67 A95 95 0 0 1 67 404 H36 V384 H67 A75 75 0 0 0 67 234 H36 Z"/><rect fill="{c["azul"]}" x="169" y="309" width="20" height="95"/>'
      f'<rect fill="{c["verde"]}" x="164.36" y="267.04" width="46" height="20" rx="10" transform="rotate(-50 187.36 277.04)"/></svg>')
def logo_di(c=None,w=96,bg=SURF):
    c=c or LOGO
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -10 214 214" width="{w}" height="{w}" role="img" aria-label="Dí"><rect x="0" y="-10" width="214" height="214" fill="{bg}"/>'
      f'<path fill="{c["rosa"]}" fill-rule="evenodd" d="M0 2 H67 A95 95 0 0 1 67 192 H0 V172 H67 A75 75 0 0 0 67 22 H0 Z"/><rect fill="{c["azul"]}" x="169" y="97" width="20" height="95"/>'
      f'<rect fill="{c["verde"]}" x="164.36" y="55.04" width="46" height="20" rx="10" transform="rotate(-50 187.36 65.04)"/></svg>')
def logo_anatomy():
    T='font-family="DiDi Mono,monospace" font-size="9" fill="#AAB7C9"'; L='stroke="#6A809E" stroke-width=".7" fill="none"'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-34 -34 462 290" width="100%" role="img" aria-label="Medidas del logo">
<rect x="-34" y="-34" width="462" height="290" fill="{SURF}"/>
<g opacity=".95">{_paths(LOGO)}</g>
<line x1="0" y1="97" x2="395" y2="97" {L} stroke-dasharray="3 3"/><text x="20" y="91" {T}>y 97 · eje de la D</text>
<line x1="-14" y1="2" x2="-14" y2="192" {L}/><line x1="-18" y1="2" x2="-10" y2="2" {L}/><line x1="-18" y1="192" x2="-10" y2="192" {L}/><text x="-18" y="102" {T} transform="rotate(-90 -18 102)" text-anchor="middle">190 · Ø de la D</text>
<text x="8" y="-8" {T}>trazo 20 (todas las líneas)</text><line x1="30" y1="-3" x2="30" y2="2" {L}/>
<line x1="162" y1="206" x2="162" y2="214" {L}/><line x1="169" y1="206" x2="169" y2="214" {L}/><text x="165.5" y="226" {T} text-anchor="middle">7</text>
<line x1="189" y1="206" x2="189" y2="214" {L}/><line x1="210" y1="206" x2="210" y2="214" {L}/><text x="199.5" y="226" {T} text-anchor="middle">21</text>
<line x1="336" y1="206" x2="336" y2="214" {L}/><line x1="343" y1="206" x2="343" y2="214" {L}/><text x="339.5" y="226" {T} text-anchor="middle">7</text>
<text x="179" y="244" {T} text-anchor="middle">barra 20×95</text><text x="353" y="244" {T} text-anchor="middle">barra 20×95</text>
<line x1="0" y1="196" x2="0" y2="204" {L}/><text x="0" y="214" {T}>corte: la D entra en cuadro</text>
<text x="426" y="14" {T} text-anchor="end">acento 46×20 · −50°</text><line x1="388" y1="18" x2="368" y2="44" {L}/>
<line x1="241" y1="-14" x2="336" y2="-14" {L}/><text x="289" y="-18" {T} text-anchor="middle">r 95 / 75</text>
</svg>'''

# ---------- íconos (propuesta v1: trazo 2, terminales rectos) ----------
ICONS={
 'arrow':'<path d="M4 12h15M13 6l6 6-6 6"/>','check':'<path d="M5 12.5l5 5L19 7"/>','close':'<path d="M6 6l12 12M18 6L6 18"/>','menu':'<path d="M4 7h16M4 12h16M4 17h16"/>',
 'mail':'<path d="M3 6h18v12H3zM3 6l9 7 9-7"/>','download':'<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>','external':'<path d="M14 5h5v5M19 5l-9 9M17 14v5H5V7h5"/>',
 'warn':'<path d="M12 4l9 16H3zM12 10v5M12 17.5v1"/>','plus':'<path d="M12 5v14M5 12h14"/>','search':'<path d="M10 4a6 6 0 100 12 6 6 0 000-12zM15 15l5 5"/>','copy':'<path d="M9 9h11v11H9zM5 15V4h11"/>','chev':'<path d="M7 10l5 5 5-5"/>',
}
def ic(name,size=24,extra=''):
    return f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="butt" stroke-linejoin="miter" aria-hidden="true" style="{extra}">{ICONS[name]}</svg>'

# ---------- demos de estados ----------
STATES=[('normal',''),('hover','is-hover'),('foco','is-focus'),('presionado','is-pressed'),('deshabilitado','is-disabled')]
def states_row(tag,cls,inner,attrs='',label=None,states=STATES):
    if 'd-st' not in cls.split(): cls=cls+' d-st'
    cells=[]
    for nm,sc in states:
        a=attrs
        if nm=='deshabilitado': a+=' disabled' if tag=='button' else ' aria-disabled="true"'
        cells.append(f'<div style="display:grid;gap:6px;justify-items:start"><{tag} class="{cls} {sc}" {a}>{inner}</{tag}><span class="m-lbl">{nm}</span></div>')
    cap=f'<div class="m-lbl" style="margin-top:6px">{label}</div>' if label else ''
    return f'<div class="d-row" style="gap:18px;align-items:flex-start;margin-bottom:18px">{"".join(cells)}</div>{cap}'
def demo(inner): return f'<div class="m-panel"><div class="didi m-demo">{inner}</div></div>'
def demos(*items): return '<div class="m-panel">'+''.join(f'<div class="didi m-demo">{i}</div>' for i in items)+'</div>'
