# Parte C · Componentes (secciones 13 a 18). Se ejecuta dentro de build_manual.py.
import calendar, math
out.append(part('Parte C · Componentes'))
I=lambda n,s=24: ic(n,s)
def H(t,sub=''): return f'<h3>{t}</h3>'+(f'<p class="m-lbl" style="max-width:84ch;font-size:.8125rem;margin:-2px 0 10px">{sub}</p>' if sub else '')
def P(inner): return f'<div class="m-panel"><div class="didi m-demo">{inner}</div></div>'
def R(*items,gap=18,top=False): return f'<div class="d-row" style="gap:{gap}px;align-items:{"flex-start" if top else "center"};margin-bottom:14px">{"".join(items)}</div>'
def L(t): return f'<div class="m-lbl" style="margin:2px 0 14px">{t}</div>'
def U(*rules): return '<ul style="margin:10px 0 4px">'+''.join(f'<li>{r}</li>' for r in rules)+'</ul>'
IMG1="url(img/v2-kol-escritorio.jpg)"; IMG2="url(img/v2-home-casos-escritorio.jpg)"; IMG3="url(img/v2-kol-celular.jpg)"

# ---------- 12 · catálogo ----------
CAT=[
 ('Barra superior','Navegación (celeste)','Barra: indicador recto','Todas las páginas: logo, Casos, Sobre mí, Contacto, idiomas y «Escribime»','sí'),
 ('Marcas (puntos y contadores)','Acción (rosa) / atención','Píldora chica','Contador en el menú, punto de «nuevo»','no'),
 ('Hoja inferior','Neutra','Esquinas superiores de 28 px','Hojas de becas, exposiciones y colaboraciones (en celular)','sí'),
 ('Grupo de botones','Acción (rosa)','Píldora con extremos','Filtro de categoría, idioma','no'),
 ('Botones','Acción (rosa)','Píldora; variante D','«Escribime» (tonal en la barra), cierre de cada caso (relleno), «Enviar mensaje»','sí'),
 ('Tarjetas','Neutras; el color del tipo en el borde y el punto','Esquinas de 12 px','Tarjetas de casos en la portada; baldosas de reconocimientos','sí'),
 ('Carrusel','Neutro','Ítems con esquinas suaves','Galerías de capturas de los casos','sí, como galería'),
 ('Casilla','Navegación (celeste)','Cuadrado, esquinas rectas','Consentimiento, filtros','no'),
 ('Fichas','Navegación (celeste); dato (azul)','Barra, radio 0','Fichas de datos de cada caso (año, rol, herramientas)','sí, las de dato'),
 ('Selector de fecha','Navegación (celeste)','Barra; contenedor en D','Fecha de una reunión','no'),
 ('Diálogos','Neutro','D grande','Hojas de reconocimientos (en computadora, tarjeta centrada)','sí'),
 ('Divisor','Neutro','Línea de 1 px','Entre secciones y entre filas de listas','sí'),
 ('Botón flotante extendido','Acción (rosa)','D grande','«Escribime» en celular y tableta','sí'),
 ('Menú del botón flotante','Acción (rosa)','D grande','Mail, LinkedIn','no'),
 ('Botón flotante','Acción (rosa)','D grande','Acción principal flotante','no'),
 ('Botones de ícono','Acción / neutro / celeste (activo)','Círculo','Ampliar, cerrar, anterior y siguiente en las galerías','sí'),
 ('Listas','Neutras; número en azul','Barra, filas rectas','Trabajos académicos y pasantías','sí'),
 ('Indicador de carga','Atención (amarillo)','Forma que cambia entre D, barra y píldora','Tarjetas de casos e imágenes de trabajos académicos, mientras la imagen llega','sí'),
 ('Menús','Neutro','Esquina de 4 px','Menú de navegación en celular','sí'),
 ('Barra de navegación inferior','Navegación (celeste)','Barra: indicador superior','Navegación inferior en celular','no'),
 ('Cajón de navegación','Navegación (celeste)','D grande (borde izquierdo recto)','Menú lateral en tableta','no'),
 ('Riel de navegación','Navegación (celeste); en los casos, el color del tipo','Barra a la izquierda','Índice de secciones de cada caso (desde 1100 px)','sí'),
 ('Indicadores de progreso','Atención (amarillo); en la lectura, el color del caso; azul en proporciones','Tramo activo en D acostada; circular = la D del logo','Barra de lectura de cada caso; envío del formulario (próximo)','sí, la barra de lectura'),
 ('Botón de opción','Navegación (celeste)','Círculo','Tipo de consulta','no'),
 ('Búsqueda','Dato (azul)','Barra con línea inferior','Buscar en los casos','no'),
 ('Botones segmentados','Navegación (celeste)','Barra segmentada','Vista lista, tabla o mosaico','no'),
 ('Hoja lateral','Neutro','D grande, borde derecho recto','Detalle de un caso desde el índice','no'),
 ('Deslizadores','Dato (azul)','Barra y manija recta','Rango de fechas','no'),
 ('Aviso breve','Atención (amarillo)','D chica','«Mail copiado», errores de envío','no'),
 ('Botón dividido','Acción (rosa)','D con mitad redonda','Una acción con variantes','no'),
 ('Interruptor','Navegación (celeste)','Píldora','Preferencia de movimiento reducido (si se ofrece)','no'),
 ('Pestañas','Navegación (celeste); en los casos, el color del tipo','Barra: indicador de 3 px','Pestañas del monitor en Kol Accesorios','sí'),
 ('Campos de texto','Dato (azul)','Barra: línea inferior','Formulario de contacto: nombre, mail y mensaje','sí'),
 ('Selector de hora','Navegación (celeste)','Barra; dial circular','Horario de una reunión','no'),
 ('Barras de herramientas','Neutro; acción (rosa)','D completa (flotante)','Acciones de la página de caso','no'),
 ('Ayudas emergentes','Neutro','Esquina de 4 px; la rica en D','Explicar un ícono','no')]
_en=sum(1 for c in CAT if c[4].startswith('sí'))
out.append(sec('catalogo','Catálogo completo',f'Los 36 componentes de la base que se tomó, todos diseñados para DiDí. Hoy el sitio usa {_en}; el resto queda listo para cuando crezca.',f'''
{table(['Componente','Color / función','Forma','Dónde va','En el sitio hoy'],[[f'<strong>{a}</strong>',b,c,d,(f'<span class="m-pass">{e}</span>' if e.startswith('sí') else f'<span style="color:#AAB7C9">{e}</span>')] for a,b,c,d,e in CAT])}
<p class="m-lbl">«En el sitio hoy» se revisó en las páginas publicadas en español (portada, Sobre mí, Contacto y los casos). Las piezas propias del sitio (laptop, monitor, cuaderno, prototipo, mosaico) no están en esta lista: van en la sección 22.</p>
{note('<b>Cada componente sigue las mismas tres reglas</b>: su color es el de su función (sección 4), su forma es una de las del logo (sección 6) y sus estados son capas (sección 9). Lo que cambia entre componentes es la anatomía, no el lenguaje.','m-ok')}
{note('<b>Ya no se usa en el sitio.</b> En la v1 la columna «Dónde va» hablaba de pestañas por categoría (Campañas, Producto, UX, Automatización), de un botón «Descargar CV», de fecha de disponibilidad y de una barra inferior con «Contacto». Nada de eso está en el sitio de hoy; los componentes siguen diseñados.','m-open')}'''))

# ---------- 13 · acciones ----------
btn_var=R(f'<button class="d-btn d-st">Relleno</button>',f'<button class="d-btn d-btn--tonal d-st">Tonal</button>',f'<button class="d-btn d-btn--outlined d-st">Contorno</button>',f'<button class="d-btn d-btn--text d-st">Texto</button>',f'<button class="d-btn d-btn--d d-st">Variante D {I("arrow",18)}</button>',f'<button class="d-btn d-st">{I("download",18)} Con ícono</button>')
btn_sizes=R('<button class="d-btn d-st" style="min-height:32px;padding:0 16px">XS · 32</button>','<button class="d-btn d-st">S · 40</button>','<button class="d-btn d-btn--lg d-st">M · 56</button>','<button class="d-btn d-st" style="min-height:96px;padding:0 48px;font-size:1.5rem">L · 96</button>')
def ib(cls,icon,extra='',lbl=''): return f'<div style="display:grid;gap:6px;justify-items:center"><button class="d-iconbtn {cls} d-st {extra}" aria-label="{lbl or icon}">{I(icon)}</button><span class="m-lbl">{lbl}</span></div>'
ibs=''.join(R(ib(c,'plus','','normal'),ib(c,'plus','is-hover','hover'),ib(c,'plus','is-focus','foco'),ib(c,'plus','is-pressed','presionado'),ib(c,'plus','is-selected' if c!='d-iconbtn--filled' else 'is-unselected','alternado'),ib(c,'plus','is-disabled','deshabilitado')) for c in ('','d-iconbtn--filled','d-iconbtn--tonal','d-iconbtn--outlined'))
fabs=R(f'<button class="d-fab d-fab--sm d-st" aria-label="Contacto">{I("mail")}</button>',f'<button class="d-fab d-st" aria-label="Contacto">{I("mail")}</button>',f'<button class="d-fab d-fab--lg d-st" aria-label="Contacto">{I("mail")}</button>',f'<button class="d-fab d-fab--tonal d-st" aria-label="Contacto">{I("mail")}</button>')
efabs=R(f'<button class="d-fab d-fab--ext d-fab--sm d-st">{I("mail",18)} Contacto</button>',f'<button class="d-fab d-fab--ext d-st">{I("mail")} Contacto</button>',f'<button class="d-fab d-fab--ext d-fab--lg d-st">{I("mail",36)} Contacto</button>')
fabm=R(f'<div class="d-fabmenu"><button class="d-btn d-st">{I("mail",18)} Mail</button><button class="d-btn d-st">{I("external",18)} LinkedIn</button><button class="d-btn d-st">{I("external",18)} GitHub</button><button class="d-fab d-st" aria-label="Cerrar" aria-expanded="true">{I("close")}</button></div>',f'<div class="d-fabmenu"><button class="d-fab d-st" aria-label="Contacto" aria-expanded="false">{I("mail")}</button></div>',top=True)
split=R(f'<div class="d-split"><button class="d-btn d-st">Descargar CV</button><button class="d-btn d-st" aria-label="Elegir idioma" aria-haspopup="menu">{I("chev",18)}</button></div>',f'<div class="d-split"><button class="d-btn d-btn--tonal d-st">Descargar CV</button><button class="d-btn d-btn--tonal d-st" aria-label="Elegir idioma">{I("chev",18)}</button></div>',f'<div class="d-split"><button class="d-btn d-btn--outlined d-st">Descargar CV</button><button class="d-btn d-btn--outlined d-st" aria-label="Elegir idioma">{I("chev",18)}</button></div>')
bgrp=R('<div class="d-btngroup"><button class="d-btn d-btn--tonal d-st is-selected" data-sel>Campañas</button><button class="d-btn d-btn--tonal d-st" data-sel>Producto</button><button class="d-btn d-btn--tonal d-st" data-sel>UX</button><button class="d-btn d-btn--tonal d-st" data-sel>Automatización</button></div>','<div class="d-btngroup d-btngroup--gap"><button class="d-btn d-btn--outlined d-st">ES</button><button class="d-btn d-btn--outlined d-st">EN</button><button class="d-btn d-btn--outlined d-st">HE</button></div>')
seg=R(f'<div class="d-seg" role="radiogroup"><button class="d-seg-i d-st is-selected" data-seg>{chk} Lista</button><button class="d-seg-i d-st" data-seg>Tabla</button><button class="d-seg-i d-st" data-seg>Mosaico</button></div>',f'<div class="d-seg"><button class="d-seg-i d-st is-selected" data-multi>{chk} Campañas</button><button class="d-seg-i d-st is-selected" data-multi>{chk} Producto</button><button class="d-seg-i d-st" data-multi>UX</button></div>',f'<div class="d-seg"><button class="d-seg-i is-disabled" disabled>Lista</button><button class="d-seg-i is-disabled" disabled>Tabla</button></div>')
out.append(sec('acciones','Acciones','Todo lo que el visitante puede hacer. El rosa es acción y su forma es la D: un lado recto, uno redondo.',f'''
{H('Buttons','Relleno, tonal, contorno y texto. Una sola acción rellena por vista.')}{P(btn_var+L('Variantes')+btn_sizes+L('Tamaños: extrachico, chico, mediano y grande. El extragrande no se usa.')+states_row('button','d-btn d-btn--d',f'Escribime {I("arrow",18)}','',"Estados de la variante D"))}
{U('Texto en una línea, verbo en infinitivo o imperativo voseante: "Leer el caso", "Escribime".','Altura 40 px, 48 px en táctil. Ícono de 18 px a la izquierda del texto.','La variante D va en la acción principal del encabezado y en el cierre de cada caso.')}
{H('Icon buttons','Estándar, relleno, tonal y contorno; cada uno con estado alternado (toggle).')}{P(ibs+L('De arriba abajo: estándar, relleno, tonal, contorno. El estado alternado usa el celeste (qué está activo), salvo el relleno, que cambia de fondo.'))}
{H('Floating action button','Pequeño, regular, grande y tonal. Lado recto a la izquierda.')}{P(fabs)}
{H('Extended FAB','Pequeño, mediano y grande, con texto.')}{P(efabs)}
{H('FAB menu','Un FAB que abre las acciones de contacto.')}{P(fabm+L('Abierto (izquierda) y cerrado (derecha).'))}
{H('Split button','Una acción principal y un menú de variantes.')}{P(split)}
{H('Button groups','Conectado (filtro de categoría) y separado (idioma).')}{P(bgrp)}
{H('Segmented buttons','Selección única y múltiple. Barra recta; el seleccionado lleva una tilde y la línea celeste.')}{P(seg+L('Selección única · múltiple · deshabilitado.'))}
{U('Entre dos y cinco segmentos. El texto cabe en una línea.','Selección = celeste, no rosa: no es una acción, es un estado.')}'''))

# ---------- 14 · navegación ----------
def nav_items(active=0,labels=('Casos','Sobre mí','Contacto')): return ''.join(f'<a class="d-navi d-st{" is-active" if i==active else ""}" href="#">{l}</a>' for i,l in enumerate(labels))
lg=logo(w=84)
ab_small=f'<div class="d-appbar" style="width:100%">{lg}<nav>{nav_items()}</nav><span class="d-grow" style="flex:1"></span><button class="d-btn d-btn--d d-st">Escribime {I("arrow",18)}</button></div>'
ab_center=f'<div class="d-appbar d-appbar--center" style="width:360px;border:1px solid #2B3A52"><button class="d-iconbtn d-st" aria-label="Menú">{I("menu")}</button><span class="d-appbar__t">Trabajos</span><button class="d-iconbtn d-st" aria-label="Buscar">{I("search")}</button></div>'
ab_md=f'<div class="d-appbar d-appbar--md" style="width:360px;border:1px solid #2B3A52"><button class="d-iconbtn d-st" aria-label="Atrás">{I("arrow")}</button><span></span><button class="d-iconbtn d-st" aria-label="Más">{I("plus")}</button><span class="d-appbar__t">Kol Accesorios</span></div>'
ab_lg=f'<div class="d-appbar d-appbar--lg" style="width:360px;border:1px solid #2B3A52"><button class="d-iconbtn d-st" aria-label="Atrás">{I("arrow")}</button><span></span><button class="d-iconbtn d-st" aria-label="Más">{I("plus")}</button><span class="d-appbar__t">Kol Accesorios</span></div>'
bb=f'<div class="d-bottombar" style="width:360px"><button class="d-iconbtn d-st" aria-label="Copiar">{I("copy")}</button><button class="d-iconbtn d-st" aria-label="Descargar">{I("download")}</button><button class="d-iconbtn d-st" aria-label="Mail">{I("mail")}</button><span class="d-grow"></span><button class="d-fab d-st" aria-label="Contacto">{I("mail")}</button></div>'
tb1=f'<div class="d-toolbar"><button class="d-iconbtn d-st" aria-label="Copiar">{I("copy")}</button><button class="d-iconbtn d-st" aria-label="Descargar">{I("download")}</button><button class="d-iconbtn d-st" aria-label="Compartir">{I("external")}</button><button class="d-btn d-btn--d d-st" style="margin-left:6px">Escribime</button></div>'
tb2=f'<div class="d-toolbar d-toolbar--docked" style="width:360px"><button class="d-iconbtn d-st" aria-label="Copiar">{I("copy")}</button><button class="d-iconbtn d-st" aria-label="Descargar">{I("download")}</button><span class="d-grow"></span><button class="d-btn d-btn--text d-st">Cerrar</button></div>'
navbar=f'<div class="d-navbar" style="width:360px">'+''.join(f'<button class="d-navbar__i{" is-active" if i==0 else ""}"><span class="d-badged">{I(ic_)}{"<span class=\"d-badge d-badge--dot\"></span>" if i==3 else ""}</span>{l}</button>' for i,(ic_,l) in enumerate((('plus','Trabajos'),('search','Método'),('copy','Sobre mí'),('mail','Contacto'))))+'</div>'
rail=f'<div class="d-rail"><button class="d-iconbtn d-st" aria-label="Menú">{I("menu")}</button><div class="d-raili is-active d-st">{I("plus")} Problema</div><div class="d-raili d-st">{I("search")} Qué hice</div><div class="d-raili d-st">{I("copy")} Medición</div><div class="d-raili d-st">{I("warn")} Lo que no salió</div></div>'
drawer=f'<div class="d-drawer"><h4>Trabajos</h4><div class="d-raili is-active d-st">{I("plus")} Kol Accesorios</div><div class="d-raili d-st">{I("search")} Sistemas de trading</div><div class="d-raili d-st">{I("copy")} Campaign Suite</div><hr class="d-divider"><h4>Sobre mí</h4><div class="d-raili d-st">{I("mail")} Contacto</div></div>'
drawer_m=f'<div class="d-drawer d-drawer--modal" style="width:260px"><h4>Menú</h4><div class="d-raili is-active d-st">{I("plus")} Trabajos</div><div class="d-raili d-st">{I("search")} Método</div><div class="d-raili d-st">{I("mail")} Contacto</div></div>'
tabs1=f'<div class="d-tabs" style="min-width:380px"><button class="d-tab is-active d-st" data-tab>Campañas</button><button class="d-tab d-st" data-tab>Producto</button><button class="d-tab d-st" data-tab>UX</button><button class="d-tab d-st" data-tab>Automatización</button></div>'
tabs2=f'<div class="d-tabs" style="min-width:380px"><button class="d-tab is-active d-st" data-tab>{I("plus",18)} Campañas</button><button class="d-tab d-st" data-tab>{I("search",18)} Producto</button><button class="d-tab d-st" data-tab>{I("copy",18)} UX</button></div>'
srch=f'<div class="d-search">{I("search")}<input placeholder="Buscar en los casos" aria-label="Buscar"><button class="d-iconbtn d-st" aria-label="Limpiar">{I("close")}</button></div>'
srchv=f'<div class="d-searchview"><div class="d-search">{I("arrow")}<input value="medición" aria-label="Buscar"><button class="d-iconbtn d-st" aria-label="Limpiar">{I("close")}</button></div><a class="d-item d-st" href="#"><span class="d-item__l">{I("search")}</span><span><b>medición de franquicia</b></span><span class="d-item__t">1 caso</span></a><a class="d-item d-st" href="#"><span class="d-item__l">{I("search")}</span><span><b>medición de campañas</b></span><span class="d-item__t">1 caso</span></a></div>'
out.append(sec('navegacion','Navegación','Dónde estás y a dónde podés ir. El celeste es navegación y su forma es la barra: un indicador recto, nunca una píldora.',f'''
{H('App bars','Barra superior pequeña (escritorio), centrada, mediana y grande (móvil); barra inferior con FAB.')}{P(ab_small+L('Pequeña, la de escritorio: logo, tres ítems, acción principal.')+R(ab_center,ab_md,top=True)+L('Centrada y mediana (colapsa a pequeña al desplazar).')+R(ab_lg,bb,top=True)+L('Grande y barra inferior con FAB. Con scroll, la barra pasa a <code>d-appbar--scrolled</code> (contenedor un nivel más claro, sin borde).'))}
{U('El logo mide siempre 84 px o más en la barra, y va quieto.','Un solo ítem activo: color de texto principal más la barra celeste de 3 px.','Altura 64 px; el indicador no toca los bordes laterales del ítem.')}
{H('Toolbars','Flotante (acciones de una página de caso) y acoplada.')}{P(R(tb1,tb2))}
{H('Navigation bar','Navegación inferior en móvil, con indicador superior y punto de aviso.')}{P(navbar)}
{H('Navigation rail','Índice de secciones de un caso largo, con el activo marcado por la barra izquierda.')}{P(R(rail,'<p style="max-width:40ch;color:#AAB7C9;font-size:.9375rem;margin:0">En pantallas anchas el riel acompaña la lectura de un caso: Problema, Qué hice, Medición y Lo que no salió. El ítem activo cambia al desplazarse.</p>',top=True))}
{H('Navigation drawer','Estándar (tablet) y modal (con velo). Borde izquierdo recto.')}{P(R(drawer,'<div style="background:rgba(5,10,20,.6);padding:20px 0 20px 0;display:flex">'+drawer_m+'<div style="width:90px"></div></div>',top=True))}
{H('Tabs','Primarias con ícono y secundarias solo con texto. Indicador recto de 3 px.')}{P(tabs1+'<div style="height:18px"></div>'+tabs2)}
{H('Search','Barra de búsqueda y vista de búsqueda con sugerencias.')}{P(R(srch,srchv,top=True))}
{U('La búsqueda es un campo de dato: línea inferior azul, no una píldora.','La vista ocupa la pantalla completa en móvil.')}'''))

# ---------- 15 · selección y entrada ----------
def chip(txt,cls='',ic_=None,sel=False,extra=''): return f'<button class="d-chip {cls} d-st{" is-selected" if sel else ""} {extra}" {"data-chipsel" if "filter" in cls else ""}>{(I(ic_,18) if ic_ else "")}{txt}</button>'
chips=(R(chip('Campañas','d-chip--filter',chk and 'check',True),chip('Producto','d-chip--filter'),chip('UX','d-chip--filter'),chip('Automatización','d-chip--filter'),chip('Deshabilitado','','',False,'is-disabled'))+L('Filter: selección múltiple. El seleccionado lleva una tilde, fondo tonal celeste y la línea inferior.')
 +R(chip('Escribime','d-chip--assist','mail'),chip('Copiar mail','d-chip--assist','copy'))+L('Assist: acciones inteligentes en contexto (rosa).')
 +R(f'<button class="d-chip d-chip--input d-st">nombre@empresa.com <span class="d-iconbtn" style="width:24px;height:24px;margin:0">{I("close",16)}</span></button>',f'<button class="d-chip d-chip--input d-st">Kol Accesorios <span class="d-iconbtn" style="width:24px;height:24px;margin:0">{I("close",16)}</span></button>')+L('Input: valores que la persona ingresó y puede quitar.')
 +R(chip('¿Qué mediste?','d-chip--suggest'),chip('¿Con qué stack?','d-chip--suggest'),chip('¿Qué no salió?','d-chip--suggest'))+L('Suggestion: preguntas frecuentes sobre un caso.'))
def chk_(state,disabled=False,lbl=''):
    svg=I('check',14) if state!='mixed' else '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 12h12"/></svg>'
    return f'<label style="display:flex;align-items:center;gap:0;color:#E6ECF5;font:400 .875rem var(--d-sans)"><button class="d-check d-st{" is-disabled" if disabled else ""}" role="checkbox" aria-checked="{state}" {"disabled" if disabled else ""} data-check>{svg}</button>{lbl}</label>'
checks=R(chk_('false',False,'Sin marcar'),chk_('true',False,'Marcado'),chk_('mixed',False,'Indeterminado'),chk_('false',True,'Deshabilitado'),chk_('true',True,'Marcado, deshabilitado'))
def rad(state,lbl,dis=False): return f'<label style="display:flex;align-items:center;color:#E6ECF5;font:400 .875rem var(--d-sans)"><button class="d-radio d-st{" is-disabled" if dis else ""}" role="radio" aria-checked="{state}" {"disabled" if dis else ""} data-radio>{""}</button>{lbl}</label>'
radios=R(rad('true','Español'),rad('false','English'),rad('false','עברית'),rad('false','Deshabilitado',True))
def sw(state,lbl,cls='',dis=False): return f'<label style="display:flex;align-items:center;gap:12px;color:#E6ECF5;font:400 .875rem var(--d-sans)"><button class="d-switch {cls}" role="switch" aria-checked="{state}" {"disabled" if dis else ""} data-sw></button>{lbl}</label>'
switches=R(sw('false','Apagado'),sw('true','Encendido'),sw('true','Con ícono','d-switch--icon'),sw('true','Deshabilitado','',True),sw('false','Deshabilitado','',True))
def pos(i,r=100,c=128): a=math.radians(i*30-90); return c+r*math.cos(a),c+r*math.sin(a)
dial=''.join(f'<span class="d-tp__n{" is-selected" if i==9 else ""}" style="left:{pos(i)[0]:.1f}px;top:{pos(i)[1]:.1f}px">{i}</span>' for i in range(1,13))
dial_m=''.join(f'<span class="d-tp__n{" is-selected" if i==6 else ""}" style="left:{pos(i)[0]:.1f}px;top:{pos(i)[1]:.1f}px">{(i*5)%60:02d}</span>' for i in range(1,13))
tp=lambda d,sel_h,sel_m,ang: f'<div class="d-tp"><small>Elegir hora</small><div class="d-tp__h"><div class="d-tp__box{" is-selected" if sel_h else ""}">09</div><span style="font:600 3.5rem var(--d-sans)">:</span><div class="d-tp__box{" is-selected" if sel_m else ""}">30</div><div class="d-tp__ap"><button class="is-selected">AM</button><button>PM</button></div></div><div class="d-tp__dial">{d}<span class="d-tp__hand" style="width:100px;transform:rotate({ang}deg)"></span><span class="d-tp__dot"></span></div><div class="d-dp__f" style="justify-content:space-between"><button class="d-iconbtn d-st" aria-label="Teclado">{I("menu")}</button><div class="d-row" style="gap:8px"><button class="d-btn d-btn--text d-st">Cancelar</button><button class="d-btn d-btn--text d-st">Aceptar</button></div></div></div>'
cal=calendar.Calendar(0).monthdayscalendar(2026,10)
def dp(kind='modal'):
    cells=''.join(f'<span class="d-dp__w">{w}</span>' for w in 'LMXJVSD')
    for wk in cal:
        for d in wk:
            if d==0: cells+='<span class="d-dp__d is-out">·</span>'; continue
            cl='';
            if kind=='range' and 27<=d<=30: cl='is-range'
            if d==26: cl+=' is-today'
            if (kind!='range' and d==28) or (kind=='range' and d in (27,30)): cl+=' is-selected'
            cells+=f'<button class="d-dp__d {cl} d-st">{d}</button>'
    head='<small>Elegir fecha</small><b>mié 28 oct</b>' if kind!='range' else '<small>Elegir rango</small><b>27 – 30 oct</b>'
    cls='d-dp d-dp--docked' if kind=='docked' else 'd-dp'
    foot='' if kind=='docked' else '<div class="d-dp__f"><button class="d-btn d-btn--text d-st">Cancelar</button><button class="d-btn d-btn--text d-st">Aceptar</button></div>'
    top='' if kind=='docked' else f'<div class="d-dp__h">{head}</div>'
    return f'<div class="{cls}">{top}<div class="d-dp__m"><span>octubre 2026</span><span><button class="d-iconbtn d-st" aria-label="Mes anterior" style="transform:scaleX(-1)">{I("arrow")}</button><button class="d-iconbtn d-st" aria-label="Mes siguiente">{I("arrow")}</button></span></div><div class="d-dp__g">{cells}</div>{foot}</div>'
dp_input=f'<div class="d-dp" style="width:328px"><div class="d-dp__h"><small>Elegir fecha</small><b>día/mes/año</b></div><div style="padding:16px 8px"><div class="d-field"><label>Fecha</label><input value="28/10/2026" placeholder="dd/mm/aaaa"><span class="d-help">Formato día/mes/año</span></div></div><div class="d-dp__f"><button class="d-btn d-btn--text d-st">Cancelar</button><button class="d-btn d-btn--text d-st">Aceptar</button></div></div>'
def slider(v=35): return f'<input type="range" class="d-range" min="0" max="100" value="{v}" style="--v:{v}%;width:300px" aria-label="Valor">'
sl_d=f'<div class="d-sl"><div class="d-sl__t"></div><div class="d-sl__a" style="left:0;width:40%"></div>'+''.join(f'<span class="d-sl__k{" is-off" if i*20>40 else ""}" style="left:{i*20}%"></span>' for i in range(6))+'<div class="d-sl__h" style="left:40%"></div><span class="d-sl__v" style="left:40%">40</span></div>'
sl_r=f'<div class="d-sl"><div class="d-sl__t"></div><div class="d-sl__a" style="left:25%;width:45%"></div><div class="d-sl__h" style="left:25%"></div><div class="d-sl__h" style="left:70%"></div><span class="d-sl__v" style="left:25%">2024</span><span class="d-sl__v" style="left:70%">2026</span></div>'
fields=(R('<div class="d-field"><label>Nombre</label><input placeholder="Cómo te llamás"><span class="d-help">Normal</span></div>','<div class="d-field is-focus"><label>Nombre</label><input value="Lucía" style="border-bottom-color:#70B4F4;background:#172744"><span class="d-help">Foco</span></div>','<div class="d-field"><label>Nombre</label><input value="Lucía"><span class="d-help">Con valor</span></div>',top=True)
 +R(f'<div class="d-field is-error"><label>Mail</label><input value="lucia@empresa" aria-invalid="true"><span class="d-help">{I("warn",16)} Falta el dominio. Probá con lucia@empresa.com</span></div>','<div class="d-field is-disabled"><label>Mail</label><input value="lucia@empresa.com" disabled><span class="d-help">Deshabilitado</span></div>','<div class="d-field d-field--outlined"><label>Empresa</label><input placeholder="Tu empresa"><span class="d-help">Contorno</span></div>',top=True)
 +R(f'<div class="d-field d-field--icon"><label>Buscar</label>{I("search")}<input placeholder="Buscar"><span class="d-help">Ícono al inicio</span></div>',f'<div class="d-field d-field--icon d-field--trail"><label>Mail</label>{I("mail")}<input placeholder="nombre@empresa.com"><span class="d-help">Ícono al final</span></div>',f'<div class="d-field d-select"><label>Tipo de consulta</label><select><option>Una colaboración</option><option>Una pregunta</option></select>{I("chev")}<span class="d-help">Selector</span></div>',top=True)
 +R('<div class="d-field" style="max-width:420px"><label>Mensaje</label><textarea placeholder="Contame qué estás buscando"></textarea><span class="d-count">0 / 500</span></div>',top=True))
out.append(sec('seleccion','Selección y entrada','Lo que la persona elige o escribe. La selección es celeste (qué está activo); lo que se escribe es un campo de dato, con línea azul abajo.',f'''
{H('Chips','Assist, filter, input y suggestion.')}{P(chips)}
{H('Checkbox')}{P(checks)}
{H('Radio button')}{P(radios)}
{H('Switch','Apagado, encendido, con ícono y deshabilitado. El encendido es celeste, no verde.')}{P(switches)}
{H('Sliders','Continuo (interactivo), discreto con marcas y valor, y de rango.')}{P(R(slider(35),sl_d,sl_r,'<input type="range" class="d-range" value="60" style="--v:60%;width:300px" disabled aria-label="Deshabilitado">',top=True)+L('Manija recta de 4 × 36 px, pista de 4 px, valor en una etiqueta mono sobre la manija. El primero es interactivo.'))}
{H('Text fields','Estados, error, contorno, íconos, selector y área de texto.')}{P(fields)}
{U('Etiqueta siempre visible (no desaparece al escribir). Ayuda debajo, en mono.','El error dice qué pasó y cómo arreglarlo, con ícono y en amarillo. Nunca solo cambia el color.')}
{H('Date pickers','Modal, acoplado, de rango y por teclado. Semana desde el lunes.')}{P(R(dp('modal'),dp('docked'),dp('range'),dp_input,top=True))}
{H('Time pickers','Reloj de horas, reloj de minutos.')}{P(R(tp(dial,True,False,180),tp(dial_m,False,True,90),top=True))}'''))

# ---------- 16 · contenedores ----------
cards=R(f'<div class="d-card"><h3>Kol Accesorios</h3><p>Campañas de Meta y Google que traen candidatos y visitas.</p><div class="d-row" style="gap:8px"><span class="d-chip-data">2024–hoy</span><span class="d-tag d-tag--verified">{chk} En vivo</span></div></div>',f'<div class="d-card d-card--elevated"><h3>Sistemas de trading</h3><p>Tres sistemas en Python que vigilan mercados, avisan por mail y se auditan solos.</p><div class="d-row" style="gap:8px"><span class="d-chip-data">10.380 líneas</span><span class="d-badge-attn">SIMULACIÓN</span></div></div>','<div class="d-card d-card--outlined"><h3>Campaign Suite</h3><p>El tablero para que todo el equipo vea qué trae cada campaña.</p><button class="d-btn d-btn--text d-st" style="margin-left:-12px">Abrir demo</button></div>',top=True)
cards2=R(f'<div class="d-card d-card--media d-card--elevated" style="width:340px"><div class="d-media" style="background-image:{IMG1}"></div><div class="d-body"><h3>Hub de franquicias</h3><p>Una página que explica el modelo, la inversión y los pasos, en vivo.</p><div class="d-actions"><button class="d-btn d-btn--tonal d-st">Leer el caso</button></div></div></div>',f'<div class="d-card d-card--row d-card--outlined"><div class="d-media" style="background-image:{IMG3}"></div><div class="d-body"><h3 style="font-size:1rem;line-height:1.5rem">Versión celular</h3><p style="margin:0">375 px, una columna.</p></div></div>',f'<div class="d-card d-card--attn" style="width:300px"><span class="d-badge-attn" style="background:#DCD060">SIN MEJORA MEDIBLE TODAVÍA</span><p style="margin:12px 0 0">Citas en IA antes y después del rediseño: ChatGPT 3→4, Claude 10→8, Perplexity 5→7 de 30. Se publica así.</p></div>',top=True)
def item(cls,lead,head,sup='',trail='',sel=False): return f'<a class="d-item {cls} d-st{" is-selected" if sel else ""}" href="#">{lead}<span><b>{head}</b>{f"<small>{sup}</small>" if sup else ""}</span>{f"<span class=\"d-item__t\">{trail}</span>" if trail else "<span></span>"}</a>'
lists=R(f'<div class="d-list" style="width:380px">{item("","<span class=\"d-item__l\">01</span>","Kol Accesorios","","2024–hoy")}{item("","<span class=\"d-item__l\">02</span>","Sistemas de trading","","2026",True)}{item("","<span class=\"d-item__l\">03</span>","Campaign Suite","","2026")}</div>',f'<div class="d-list" style="width:380px">{item("d-item--2","<span class=\"d-item__l\">"+I("search")+"</span>","Medición de punta a punta","GA4, Clarity, Search Console","2024–hoy")}{item("d-item--2","<span class=\"d-item__l\">"+I("copy")+"</span>","Batería de prompts de IA","1.520 respuestas analizadas","2026")}</div>',f'<div class="d-list" style="width:420px">{item("d-item--3","<span class=\"d-item__img\" style=\"background-image:"+IMG2+"\"></span>","Página de ciudades","Tarjetas con locales abiertos y ciudades disponibles. Quince ciudades nuevas, cada una con su análisis.","")}</div>',top=True)
car=f'<div class="d-carousel"><figure class="d-ci d-ci--l" style="background-image:{IMG1}"><figcaption>Hub</figcaption></figure><figure class="d-ci d-ci--l" style="background-image:{IMG2}"><figcaption>Ciudades</figcaption></figure><figure class="d-ci d-ci--m" style="background-image:{IMG3}"></figure><figure class="d-ci d-ci--s" style="background-image:{IMG1}"></figure></div>'
car_h=f'<div class="d-carousel" style="height:180px"><figure class="d-ci d-ci--xl" style="background-image:{IMG1}"><figcaption>Una captura a la vez</figcaption></figure><figure class="d-ci d-ci--s" style="background-image:{IMG2}"></figure></div>'
dlg=f'<div class="d-dialog"><div class="d-dialog__icon">{I("download")}</div><h3>¿Descargar el CV?</h3><p>PDF de una página, en inglés, con las fechas de esta web.</p><div class="d-actions"><button class="d-btn d-btn--text d-st">Cancelar</button><button class="d-btn d-st">Descargar</button></div></div>'
dlg_i=f'<div class="d-dialog"><div class="d-dialog__icon">{I("warn")}</div><h3>No se pudo enviar</h3><p>El mensaje no salió. Probá de nuevo o escribime a malquidebora@gmail.com.</p><div class="d-actions"><button class="d-btn d-btn--text d-st">Cerrar</button><button class="d-btn d-st">Reintentar</button></div></div>'
dlg_f=f'<div class="d-dialog d-dialog--full" style="width:360px"><div class="d-dialog__bar"><button class="d-iconbtn d-st" aria-label="Cerrar">{I("close")}</button><h3>Escribime</h3><button class="d-btn d-btn--text d-st">Enviar</button></div><div class="d-body"><div class="d-field" style="margin-bottom:14px"><label>Mail</label><input placeholder="nombre@empresa.com"></div><div class="d-field"><label>Mensaje</label><textarea></textarea></div></div></div>'
sheet_b=f'<div style="background:rgba(5,10,20,.6);width:360px;height:300px;display:flex;align-items:flex-end"><div class="d-sheet" style="width:100%"><div class="d-menu" style="background:none;box-shadow:none;padding:0"><a href="#">{I("plus")} Trabajos</a><a href="#" class="is-selected">{I("search")} Método</a><a href="#">{I("mail")} Contacto</a></div></div></div>'
sheet_s=f'<div style="background:#0F1B2D;box-shadow:inset 0 0 0 1px #2B3A52;width:360px;height:300px;display:flex;align-items:flex-end"><div class="d-sheet" style="width:100%;box-shadow:none;background:#172744"><p style="margin:0;color:#AAB7C9">Hoja estándar: convive con el contenido y no lleva velo.</p></div></div>'
side=f'<div style="background:rgba(5,10,20,.6);width:480px;height:340px;display:flex;justify-content:flex-end"><div class="d-sidesheet" style="height:100%"><header><h3>Kol Accesorios</h3><button class="d-iconbtn d-st" aria-label="Cerrar">{I("close")}</button></header><p style="color:#AAB7C9;margin:0 0 12px">Campañas · Producto · 2024–hoy</p><div class="d-row" style="gap:8px"><span class="d-tag d-tag--verified">{chk} Verificado</span><span class="d-chip-data">27 páginas</span></div></div></div>'
menu=f'<div class="d-menu" style="max-width:280px"><a href="#" class="d-st">{I("copy")} Copiar mail<span class="d-kbd">⌘C</span></a><a href="#" class="d-st is-selected">{I("check")} Español</a><a href="#" class="d-st">{I("plus")} English</a><hr><a href="#" class="d-st" aria-disabled="true">{I("download")} Descargar CV</a></div>'
out.append(sec('contenedores','Contenedores','Superficies que agrupan contenido. Son neutras: el color entra por la función de lo que contienen.',f'''
{H('Cards','Rellena, elevada, con contorno, con imagen, horizontal y de atención. Siempre con el lado recto a la izquierda.')}{P(cards+cards2)}
{H('Lists','Una, dos y tres líneas; con número, ícono o imagen a la izquierda y dato a la derecha. El ítem seleccionado lleva barra celeste.')}{P(lists)}
{H('Carousel','Multi-browse y hero, con ítems en D.')}{P(car+'<div style="height:14px"></div>'+car_h)}
{H('Divider')}{P('<div style="max-width:420px"><hr class="d-divider"><hr class="d-divider d-divider--inset"><div class="d-row" style="gap:14px;height:40px"><span>Uno</span><span class="d-vdivider"></span><span>Dos</span><span class="d-vdivider"></span><span>Tres</span></div></div>'+L('Completo, con sangría y vertical.'))}
{H('Dialogs','Básico, con ícono de alerta y de pantalla completa (móvil).')}{P(R(dlg,dlg_i,dlg_f,top=True))}
{H('Bottom sheets','Modal (con velo) y estándar.')}{P(R(sheet_b,sheet_s,top=True))}
{H('Side sheets','Modal en escritorio, borde derecho recto.')}{P(side)}
{H('Menus','Con íconos, atajo, seleccionado, divisor y deshabilitado.')}{P(menu)}
{H('Tooltips','Simple y rico.')}{P(R('<span class="d-tooltip">Copiar mail</span>',f'<div class="d-tooltip--rich"><b>Inferido</b>Conclusión propia, a confirmar con la fuente. <div class="d-actions"><button class="d-btn d-btn--text d-st" style="min-height:32px">Más info</button></div></div>',top=True))}'''))

# ---------- 17 · retroalimentación ----------
fb=(R('<div class="d-snackbar">Se copió el mail.</div>','<div class="d-snackbar">Mail copiado <button>Deshacer</button></div>',f'<div class="d-snackbar d-snackbar--2"><span style="flex:1">No se pudo enviar el mensaje. Probá de nuevo en un rato.</span><button>Reintentar</button><button class="d-iconbtn d-st" style="color:#0F1B2D;margin:0" aria-label="Cerrar">{I("close",20)}</button></div>',top=True))
exec(compile((pathlib.Path(__file__).resolve().parent/'manual_progreso.py').read_text(),'manual_progreso','exec'),globals())
badges=R(f'<span class="d-badged"><button class="d-iconbtn d-st" aria-label="Avisos">{I("mail")}</button><span class="d-badge d-badge--dot"></span></span>',f'<span class="d-badged"><button class="d-iconbtn d-st" aria-label="Avisos">{I("mail")}</button><span class="d-badge">3</span></span>',f'<span class="d-badged"><button class="d-iconbtn d-st" aria-label="Avisos">{I("mail")}</button><span class="d-badge" style="min-width:28px">99+</span></span>','<span class="d-badge-attn">NUEVO</span>')+L('Punto, contador chico, contador grande y etiqueta de atención.')
out.append(sec('retroalimentacion','Retroalimentación','Lo que el sistema le dice a la persona: qué pasó, qué está pasando, qué hay de nuevo. Amarillo = atención.',f'''
{H('Snackbar')}{P(fb)}
{PROGRESS}
{H('Badges')}{P(badges)}
{U('Un aviso breve dura de 4 a 10 segundos y no tapa la acción principal.','Nunca se anuncia solo con color: el amarillo siempre lleva texto o ícono.')}'''))

# ---------- 18 · datos propios ----------
dato=(R('<div class="d-tile"><div class="d-v">27</div><div class="d-l">páginas en vivo</div></div>','<div class="d-tile"><div class="d-v">1.520</div><div class="d-l">respuestas de IA</div></div>','<div class="d-tile"><div class="d-v">3 de 4</div><div class="d-l">con un dato mal</div></div>','<div class="d-tile d-tile--lg"><div class="d-v">10.380</div><div class="d-l">líneas de Python</div></div>',top=True)
 +R('<span class="d-chip-data">2024–2026</span>','<span class="d-chip-data">WordPress REST</span>','<span class="d-chip-data">Python</span>','<span class="d-chip-data">GA4</span>','<span class="d-chip-data">llms.txt</span>')
 +'<table class="d-table" style="max-width:640px"><thead><tr><th>#</th><th>Proyecto</th><th>Año</th><th>Qué se midió</th></tr></thead><tbody><tr><td class="d-n">01</td><td>Kol Accesorios</td><td class="d-n">2024–hoy</td><td>27 páginas en vivo</td></tr><tr><td class="d-n">02</td><td>Sistemas de trading</td><td class="d-n">2026</td><td>0 hallazgos refutados</td></tr></tbody></table><div style="height:16px"></div>'
 +'<pre class="d-code" style="max-width:480px">lead_franquicia  → GA4 · conversión\nclick_whatsapp   → GA4 · secundaria\nutm_source       → google | meta | ig</pre>'
 +'<div style="height:16px"></div>'+R(f'<span class="d-tag d-tag--verified">{chk} Verificado</span>','<span class="d-tag d-tag--reported">Reportado</span>','<span class="d-tag d-tag--inferred">Inferido</span>','<span class="d-avail">Disponible desde [fecha]</span>'))
out.append(sec('datos-propios','Datos (propios)','Componentes propios para mostrar cifras y datos de cada caso. La base que se tomó no los tiene.',f'''
{P(dato)}
{table(['Componente','Para qué','Regla'],[['Baldosa de cifra','Una cifra y lo que mide','Etiqueta en mono bajo la cifra, línea superior del color del tipo del caso, radio 0. En Kol, Campaign Suite, Santo Tomé y Medido, mantenerla presionada muestra de dónde sale (sección 22).'],['Ficha de dato','Año, rol, herramientas','Rectangular, con una línea inferior del color del tipo del caso. No es interactiva.'],['Tabla','Resultados y comparaciones','Encabezado en mono con mayúsculas, del color del tipo; números tabulares; filas rectas. En celular se desplaza de costado dentro de su marco.'],['Bloque de código','Evento, comando o salida','Mono, línea izquierda azul, fondo hundido.'],['Baldosa de reconocimiento','Becas, exposiciones, colaboraciones','Cifra grande, etiqueta en mono y una flecha: abre la hoja con la lista.']])}
{note('<b>Ya no se usa en el sitio.</b> La etiqueta de confianza (verificado, reportado, inferido: «cada cifra publicada lleva una») y la etiqueta de disponibilidad («Disponible desde…») siguen dibujadas en <code>didi-ui.css</code>, pero el sitio no las muestra. La fuente de cada cifra vive en la hoja de verdad y en las fichas.','m-open')}'''))
