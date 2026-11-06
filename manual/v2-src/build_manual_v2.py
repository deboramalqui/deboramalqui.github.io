"""Genera manual/manual-didi-v2.html a partir de marca/didi-ui.css + manual/manual-v2.css + este contenido.
Copia de tools/build_manual.py (la v1 queda como está). Uso: python3 manual/v2-src/build_manual_v2.py"""
import pathlib, sys, html as H
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from manual_lib import *
from manual_lib import _paths

SECS=[]   # (parte, id, num, titulo)
# --publico: la versión del sitio. Débora (2026): estas secciones quedan privadas, «aca entre nos».
PUBLICO='--publico' in sys.argv
PRIVADAS={'imagen','microcopy','no-hacer','tokens','abiertas'}
def part(t):
    if PUBLICO and t.startswith('Parte E'): return ''
    SECS.append(('PART',t,None,None)); return f'<div class="m-part">{t}</div>'
def sec(id_,titulo,lead,body):
    if PUBLICO and id_ in PRIVADAS: return ''
    n=sum(1 for s in SECS if s[0]!='PART')+1; SECS.append(('SEC',id_,n,titulo))
    return f'<section class="m-sec" id="{id_}"><div class="m-num">{n:02d}</div><h2>{titulo}</h2><p class="m-lead">{lead}</p>{body}</section>'
def note(t,k=''): return f'<div class="m-note {k}">{t}</div>'
def two(do,dont): return f'<div class="m-two"><div class="m-do"><b>Sí</b>{do}</div><div class="m-dont"><b>No</b>{dont}</div></div>'
def card(h,p): return f'<div class="m-card"><h5>{h}</h5><p>{p}</p></div>'
def fig(inner,cap): return f'<div class="m-fig">{inner}<div class="m-cap">{cap}</div></div>'
def table(head,rows,cls='m-t'):
    return f'<table class="{cls}"><tr>'+''.join(f'<th>{h}</th>' for h in head)+'</tr>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</table>'
A=lambda s: s  # alias de lectura
chk=ic('check',16); arr=ic('arrow',18)

# ============================== PARTE A ==============================
out=[]
out.append(f'''<header class="m-cover"><div class="m-kick">Manual de marca · versión 2 · 2026</div>
<div style="max-width:380px;margin:0 0 28px">{logo(w=380)}</div>
<h1>DiDí, el sistema</h1>
<p>Cómo se ve, se mueve y se construye el portfolio de Débora Malqui. Un color por función en la interfaz y un color por tipo de trabajo en los casos, tres formas sacadas del logo y una fuente propia con la D sin palo.</p>
<p>Este manual dice lo que hace hoy <a href="https://www.malquidebora.com/">www.malquidebora.com</a>. Las cifras de contraste y de verificación las calcula el generador; no están escritas a mano.</p>
{note('<b>Estado.</b> v2. Reemplaza a la v1, que queda guardada sin cambios. Lo que la v1 decía y el sitio ya no hace no se borró: está en cada sección, marcado en <b>rosa</b> con «Ya no se usa en el sitio», y reunido en la sección 1.','m-open')}
</header>''')

out.append(part('Antes de empezar'))
out.append(sec('cambios','Qué cambió desde la v1','El sistema creció mientras se construía el sitio: más color, más movimiento y una portada nueva. Esta es la lista corta; el detalle está en cada sección.',f'''
<h3>Lo nuevo</h3>
<ol>
<li><strong>Color por tipo de trabajo.</strong> Campañas en rosa, producto en celeste, UX en amarillo, automatización en verde y académicos en azul. Cada caso toma su color en los detalles; los enlaces y los botones no cambian (sección 4).</li>
<li><strong>Portada con la Campaign Suite.</strong> Una laptop que se abre al cargar, con tres cifras alrededor, que sigue al mouse en computadora y se inclina al bajar la página en celular (sección 20).</li>
<li><strong>Casos en dos tamaños.</strong> Campaign Suite y Medido en grande; los otros ocho en filas completas de 2 (celular y tableta) o 4 (computadora).</li>
<li><strong>Títulos de sección grandes</strong>, en DiDi Sans ExtraBold, con la cantidad al lado en DiDi Mono (sección 5).</li>
<li><strong>Movimiento de la vitrina:</strong> los casos y los títulos entran al bajar la página, el título de una tarjeta viaja hasta el título del caso al abrirlo, y la imagen de cada trabajo académico sigue al mouse (sección 10).</li>
<li><strong>Procesos que se ven:</strong> una barra de lectura del color del caso que avanza al bajar, y un indicador de carga amarillo mientras llegan las imágenes (secciones 10 y 18).</li>
<li><strong>Hojas de reconocimientos:</strong> becas, exposiciones y colaboraciones se abren en una hoja que sube desde abajo en celular y en una tarjeta centrada en computadora.</li>
<li><strong>Piezas para mostrar trabajo:</strong> monitor que se desplaza, cuaderno que pasa las hojas, prototipo que se puede tocar, mosaico de piezas y videos con miniatura (sección 21).</li>
<li><strong>Hebreo con su letra:</strong> la Heebo va incluida en el sitio, y el nombre aparece también en letras hebreas.</li>
<li><strong>Velocidad:</strong> 100 de 100 en Lighthouse, la medición de Google, en celular y en computadora (sección 12).</li>
</ol>
<h3>Lo que la v1 decía y ya no se hace</h3>
{table(['La v1 decía','Hoy'],[
 ['Un color, una función: rosa solo acción, verde solo verificado.','En los componentes sigue igual. En los casos, los cinco colores también marcan el tipo de trabajo.'],
 ['Etiquetas de confianza (verificado, reportado, inferido), «Lo que no salió», «Sin mejora medible todavía».','La web es una vitrina: tono seguro y concreto, sin notas de método. Las fuentes de cada cifra viven en la hoja de verdad y en las fichas.'],
 ['Cliente con nombre de fantasía: Nido Accesorios.','Se llama por su nombre real: Kol Accesorios. «Nido» no se usa más.'],
 ['Sin título ni frase hasta el posicionamiento; «Disponible desde [fecha]».','La portada tiene una frase fija, aprobada por Débora. No se muestra fecha de disponibilidad.'],
 ['Portada con «Ver los casos», «Descargar CV», cuatro cifras y pestañas por categoría.','Portada con la laptop y tres cifras; casos en tarjetas con portada; sin pestañas.'],
 ['Nada dura más de 400 ms, los títulos no se animan, no hay transición entre páginas, nada se mueve solo.','Los componentes siguen en 400 ms o menos. La vitrina tiene su propio movimiento, más largo. El logo sigue quieto y todo se apaga con «reducir movimiento».'],
 ['Tarjetas en D abierta, con el lado recto a la izquierda.','Las tarjetas de casos tienen las cuatro esquinas redondeadas (12 px).'],
 ['Barra de arriba de 64 px con el logo de 84 px; «Escribime» relleno.','Barra de 72 px con el logo de 88 px; «Escribime» tonal en D.'],
 ['Fechas con día y mes en todo el documento.','Fechas solo con año.']])}'''))

out.append(part('Parte A · Identidad'))
out.append(sec('concepto','Concepto y voz','El portfolio es la prueba de lo que hace, no un catálogo de todo lo que hizo. La web es una vitrina: tono seguro y concreto, con cifras verdaderas.',f'''
<h3>Cuatro principios</h3>
<div class="m-grid">{card('1 · Cifras verdaderas, no adjetivos','Un resultado se muestra con la cifra y lo que mide. La cifra tiene que estar en la hoja de verdad o en una ficha; si no está, no se publica.')}{card('2 · Vitrina, no informe','Tono seguro y concreto. Sin disculpas, sin notas de método, sin etiquetas de confianza en la página.')}{card('3 · Un color por función, un color por tipo','En la interfaz, cada color del logo hace un trabajo. En los casos, también dice qué tipo de trabajo es.')}{card('4 · El sistema se explica solo','Cada regla tiene una frase. Si necesita dos párrafos para justificarse, se simplifica.')}</div>
{note('<b>Ya no se usa en el sitio.</b> La v1 tenía como principio 2 «Lo que no salió también se cuenta»: «Sin mejora medible todavía» con el mismo peso que un resultado bueno. Desde 2026 la web no lo muestra (regla de Débora: la web es una vitrina).','m-open')}
<h3>Voz</h3>
{table(['Regla','Cómo se aplica'],[
 ['Primera persona, verbo concreto','«Vengo del diseño de producto», «Hoy manejo campañas». No «soy experta en».'],
 ['Cifra + qué mide','«505 postulaciones en 28 días». La fuente queda en la ficha del caso, no en la página.'],
 ['Rol exacto','«Dirigí y validé el desarrollo hecho con asistentes de IA.» Nunca «programé» ni «desarrollé» si no es cierto.'],
 ['Sin adjetivos que no se puedan medir','Fuera: excelente, innovador, apasionada, resultados increíbles.'],
 ['La frase de la portada es fija','«Vengo del diseño de producto y del marketing clásico. Hoy manejo campañas de Google y Meta medidas en GA4, SEO, GEO y AEO, y automatizaciones con IA.» Lo mismo en Google, en los datos estructurados y en la imagen para compartir.'],
 ['Voseo en las llamadas a la acción','«Escribime», «Probalo». El resto del texto no habla de vos.']])}
{two('«410 → 82 leads, con el error apagado.»','«Detecté errores críticos y optimicé la medición con resultados excelentes.»')}
{two('«+69 % visitas al sitio en 28 días.»','«Mejoré mucho el tráfico de la marca.»')}
<h3>Nombre</h3>
<p>En el texto, el nombre es <strong>Débora Malqui</strong>; en los textos en hebreo, <strong lang="he">דבורה מלכי</strong>, en letras hebreas. <strong>DiDí</strong> es la marca gráfica: aparece como logo, firma y favicon, no como nombre propio en frases. Los clientes van con su nombre real (Kol Accesorios). Medido, su propio producto, tiene un caso en el sitio; quien lo usa se describe como «un negocio».</p>
{note('<b>Ya no se usa en el sitio.</b> La v1 decía que un cliente anonimizado se nombraba por su fantasía (Nido Accesorios), que no había frase de presentación hasta el posicionamiento y que ninguna pieza mencionaba Medido. Las tres cosas cambiaron: nombre real, frase fija y Medido con su caso.','m-open')}''') )

# ---- logo
def vp(inner,cap,bg=None):
    st=f"background:{bg};" if bg else ""
    return f'<div class="m-panel"><div class="didi m-demo" style="min-height:150px;display:flex;gap:18px;align-items:center;justify-content:center;{st}">{inner}</div><div class="m-lbl" style="padding:8px 14px;background:#0A1322;margin:0">{cap}</div></div>'
favs='<img src="../marca/png/favicon-32.png" width="32" height="32" alt="favicon 32" style="image-rendering:pixelated"><img src="../marca/png/favicon-16.png" width="16" height="16" alt="favicon 16" style="image-rendering:pixelated"><img src="../marca/png/favicon-32.png" width="128" height="128" alt="favicon ampliado" style="image-rendering:pixelated">'
V=lambda ink: logo(mono(ink),w=170)
sizes=''.join(f'<div style="display:grid;gap:6px;justify-items:start">{logo(w=w)}<span class="m-lbl">{w} px</span></div>' for w in (240,160,120,96,64))
wrong=lambda t,svg: f'<div class="m-card" style="padding:12px">{svg}<p style="margin:10px 0 0;font-size:.8125rem;color:#AAB7C9">{t}</p></div>'
stretched=logo(w=170,extra='transform:scaleX(1.25);transform-origin:left;')
bad_one=logo({k:'#E890CC' for k in LOGO},w=170)
shadow=logo(w=170,extra='filter:drop-shadow(4px 6px 5px rgba(0,0,0,.6));')
outlinedlogo=f'<svg viewBox="0 0 380 193" width="170" style="height:auto;display:block">{_paths({k:"none" for k in LOGO}) if False else ""}<g fill="none" stroke="#E6ECF5" stroke-width="2">{_paths({k:"none" for k in LOGO}).replace("fill=\"none\"","")}</g></svg>'
closed=f'<svg viewBox="0 0 380 193" width="170" style="height:auto;display:block"><path fill="#E890CC" fill-rule="evenodd" d="M36 2 H67 A95 95 0 0 1 67 192 H36 V172 H67 A75 75 0 0 0 67 22 H36 Z"/>'+_paths(LOGO).split('<rect',1)[1].join(['<rect','']) if False else None
closed=f'<svg viewBox="0 0 380 193" width="170" style="height:auto;display:block"><path fill="#E890CC" fill-rule="evenodd" d="M36 2 H67 A95 95 0 0 1 67 192 H36 V172 H67 A75 75 0 0 0 67 22 H36 Z"/><rect fill="#80ECEC" x="169" y="97" width="20" height="95"/><path fill="#DCD060" fill-rule="evenodd" d="M210 2 H241 A95 95 0 0 1 241 192 H210 V172 H241 A75 75 0 0 0 241 22 H210 Z"/><rect fill="#70B4F4" x="343" y="97" width="20" height="95"/><rect fill="#ACEC84" x="338.36" y="55.04" width="46" height="20" rx="10" transform="rotate(-50 361.36 65.04)"/></svg>'
rot=logo(w=170,extra='transform:rotate(-8deg);')
onlight=f'<div style="background:#F6F3EE;padding:10px">{logo(w=150)}</div>'
out.append(sec('logo','Logo','El logo es la forma de todo el sistema: dos D abiertas sin asta, dos barras y un acento inclinado. La D rosa entra cortada por el borde izquierdo, a propósito.',f'''
{fig(f'<div class="m-panel">{logo_anatomy()}</div>','Construcción en unidades de dibujo (el logo mide 380×193). Trazo 20 en todas las líneas; las dos D, de diámetro 190, comparten eje y base; las barras llegan hasta el centro de la D (y 97).')}
{table(['Elemento','Medida (u)','Regla'],[
 ['Trazo','20','Único: D, barras y acento. No hay dos pesos.'],
 ['D rosa y D amarilla','Ø190 · radios 95 y 75','Mismo tamaño, centros en y 97. La rosa entra cortada en x 0; la amarilla tiene extremos planos en x 210.'],
 ['Barras celeste y azul','20×95 · y 97–192','El tope coincide con el centro de la D.'],
 ['Huecos','7 · 21 · 7','D→barra 7, barra→D 21: se lee "Di" y "Dí" como dos bloques.'],
 ['Acento verde','46×20 · −50° · radio 10','Despegado 12 u de la barra azul, con su cabeza inferior sobre el eje de la barra.'],
 ['Colores','#E890CC #80ECEC #DCD060 #70B4F4 #ACEC84','Exactos del archivo original. No se derivan ni se oscurecen.']])}
<h3>Versiones</h3>
<div class="m-grid m-g3">
{vp(logo(w=200),'Color · sobre azul noche')}
{vp(logo(mono('#161616'),w=200),'Una tinta oscura · sobre claro','#F6F3EE')}
{vp(logo(mono('#F2F2F2'),w=200),'Una tinta clara · sobre oscuro')}
{vp(logo_stacked(w=96),'Apilado · pie, firma, avatar')}
{vp(logo_di(w=96)+logo_di(w=48)+logo_di(w=32),'Monograma D + í · 96, 48 y 32 px')}
{vp(favs,'Favicon calzado al píxel · 32, 16 y ampliado')}
</div>
<h3>En la barra del sitio</h3>
<p>El logo va a la izquierda de la barra de arriba, a <strong>88 px</strong> de ancho, sobre azul noche y en sus colores. La barra mide 72 px de alto. En hebreo, la barra se espeja pero el logo no: es una imagen.</p>
<h3>Área de respeto y tamaño mínimo</h3>
<p>El área de respeto es <strong>x = 40 u</strong> (dos trazos, 21 % de la altura), medida desde el borde más saliente. A la izquierda el logo sangra contra el borde del contenedor, o guarda la misma x completa: nunca un margen intermedio, que haría parecer error al corte.</p>
<div class="m-panel"><div class="didi m-demo d-row" style="gap:36px;align-items:flex-end">{sizes}</div></div>
{table(['Uso','Mínimo','Por qué'],[['Logo completo, pantalla','96 px de ancho','Trazo de 5 px y hueco de 12 u de 3 px. Por debajo, el acento se funde con la barra.'],['Logo completo, impresión','25 mm','Misma proporción.'],['Debajo de 96 px','Monograma D + í','Es el recorte del mismo vector, con favicon calzado a 32 y 16 px.']])}
{note('Los mínimos salen de la proporción del dibujo, no de una prueba en pantalla real a 1×. Ver sección 28.','m-open')}
<h3>Sobre qué fondo</h3>
<p>Los colores del logo son pasteles pensados para fondos oscuros. Sobre azul noche pasan con 5,4:1 o más. <strong>Sobre fondo claro no pasan</strong> (celeste y verde quedan en 1,3:1 sobre hueso): ahí va la versión de una tinta oscura. No existe una versión "con colores oscurecidos": es el logo o es una tinta.</p>
<h3>Usos incorrectos</h3>
<div class="m-grid">
{wrong('Deformarlo: el trazo deja de ser único.',f'<div class="didi" style="padding:14px;overflow:hidden">{stretched}</div>')}
{wrong('Un solo color: pierde las funciones.',f'<div class="didi" style="padding:14px">{bad_one}</div>')}
{wrong('Sombra o efecto.',f'<div class="didi" style="padding:14px">{shadow}</div>')}
{wrong('Cerrar la D rosa con corte plano: se pierde "entra en cuadro".',f'<div class="didi" style="padding:14px">{closed}</div>')}
{wrong('Rotarlo o inclinarlo: el único ángulo es el del acento.',f'<div class="didi" style="padding:14px;overflow:hidden">{rot}</div>')}
{wrong('Los colores originales sobre claro: no pasan contraste.',onlight)}</div>
<h3>El logo no se anima</h3>
<p>Se probó una entrada animada de 1,3 segundos y se descartó en 2026. El logo aparece quieto, siempre: tampoco se mueve en la transición entre páginas, porque la barra de arriba queda fija mientras cambia la página (sección 10).</p>
<h3>Archivos</h3>
<p><code>marca/didi-logo.svg</code> (final) · <code>didi-logo-una-tinta-oscura.svg</code> · <code>didi-logo-una-tinta-clara.svg</code> · <code>didi-logo-apilado.svg</code> · <code>didi-monograma-Di.svg</code> · <code>didi-favicon-32.svg</code> · <code>didi-favicon-16.svg</code> · <code>favicon.ico</code> · PNG en <code>marca/png/</code>. Anteriores guardados: <code>didi-logo-fiel-v0.svg</code> (calco del PNG original) y <code>didi-logo-v1-seis-ajustes.svg</code>.</p>'''))

# ---- color
def tipos_demo():
    T=[('Kol Accesorios','Campañas','#E890CC','2024–hoy · Campañas'),('Campaign Suite','Producto','#80ECEC','2025–hoy · Producto · Medición'),('Waycare','UX/UI','#DCD060','2019 · UX/UI'),('Sistemas de trading','Automatización','#ACEC84','2025–presente · Automatización'),('Adidas Pulse','Académico','#70B4F4','2026 · SEO · GEO')]
    return ''.join(f'<div style="background:var(--d-low);border:1px solid {c};border-radius:12px;overflow:hidden;box-shadow:0 22px 44px -26px {c}"><div style="aspect-ratio:4/3;background:linear-gradient(160deg,{c}33,var(--d-lowest) 70%)"></div><div style="padding:12px 14px 4px;font:700 1rem/1.3 var(--d-sans)">{t}</div><div style="padding:0 14px 12px;font:400 .6875rem/1.4 var(--d-mono);color:var(--d-on-var);letter-spacing:.04em"><i style="display:inline-block;width:7px;height:7px;border-radius:50%;background:{c};margin-right:7px;vertical-align:1px"></i>{m}</div></div>' for t,k,c,m in T)
out.append(sec('color','Color','Superficie azul noche y cinco colores del logo. Cada uno hace un trabajo en la interfaz y, en los casos, nombra un tipo de trabajo.',f'''
<h3>Un color por función</h3>
{func_table()}
<h3>Superficies</h3>
<p>El fondo es <strong>azul noche (#0F1B2D)</strong>, nunca negro puro. Los niveles de contenedor suben en claridad para marcar jerarquía; en un tema oscuro, el tono sustituye a la sombra.</p>
{surface_swatches()}
<h3>Contenedores tonales de función</h3>
<p>Cuando un color de función rellena una superficie (tarjeta de atención, chip seleccionado), se usa su versión tonal: el color al 28 % sobre la superficie, con el texto en el mismo color aclarado. Así el texto largo nunca va sobre el color pleno.</p>
{tonal_block()}
<h3>Matriz de contraste (calculada)</h3>
{contrast_matrix()}
<p class="m-lbl">Fórmula WCAG 2.x. "texto" ≥ 4,5:1 · "gráfico" ≥ 3:1 (bordes, íconos, logo). El contorno #6A809E se eligió para llegar a 3:1 en todas las superficies: el primero que probé (#4F6079) daba 2,7:1 y falló.</p>
<h3>Reglas</h3>
<ol><li><strong>Un elemento, una función.</strong> Si una tarjeta tiene acción y dato, el color va en el botón y el dato queda en un tile recto.</li>
<li><strong>Un solo botón relleno rosa por vista.</strong> Es la acción principal; las demás son tonales, con contorno o de texto.</li>
<li><strong>Texto sobre color pleno siempre #0F1B2D.</strong> En tonal, el color aclarado.</li>
<li><strong>El color nunca es el único portador de significado.</strong> Cada función lleva además forma, ícono o texto.</li>
<li><strong>Verde, como estado, solo con algo comprobado detrás.</strong> Como tipo de trabajo, marca automatización (ver abajo).</li>
<li><strong>No hay tema claro.</strong> Para impresión y CV: logo de una tinta sobre blanco, texto negro.</li></ol>
<h3>Color por tipo de trabajo</h3>
<p>Cada caso tiene un tipo, y cada tipo toma un color del logo. El color aparece en la tarjeta de la portada (un punto antes del año y un brillo al pasar el mouse) y en toda la página del caso, siempre en detalles: nunca en el fondo ni en el texto.</p>
<div class="m-panel"><div class="didi m-demo" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px">{tipos_demo()}</div></div>
{table(['Tipo','Color','Casos de hoy'],[
 ['Campañas','<span class="m-sw" style="background:#E890CC"></span>rosa <code>--d-accion</code>','Kol Accesorios, Communiqué'],
 ['Producto','<span class="m-sw" style="background:#80ECEC"></span>celeste <code>--d-nav</code>','Campaign Suite, Medido, Santo Tomé'],
 ['UX y UX/UI','<span class="m-sw" style="background:#DCD060"></span>amarillo <code>--d-atencion</code>','Waycare, Clash, Bplay, MAC'],
 ['Automatización','<span class="m-sw" style="background:#ACEC84"></span>verde <code>--d-ok</code>','Sistemas de trading'],
 ['Trabajos académicos y pasantías','<span class="m-sw" style="background:#70B4F4"></span>azul <code>--d-dato</code>','La sección «Trabajos académicos y pasantías»']])}
<p>Dentro del caso, el color del tipo (<code>--tone</code>) va en: la línea bajo el título, el punto de cada subtítulo, las viñetas, las cifras y su etiqueta, los encabezados de tabla, las fichas de datos, el ítem activo del índice, la pestaña elegida y los puntos de las galerías.</p>
<ul><li><strong>Los enlaces siguen celestes y los botones siguen rosas</strong>, en cualquier caso: son funciones, no decoración.</li>
<li>Un tipo nuevo cae en celeste hasta que se le asigne un color (<code>TONES</code> en el generador del sitio).</li>
<li>Si un caso tiene dos tipos (por ejemplo «Producto · Medición»), manda el primero.</li></ul>
<h3>Otras listas con color</h3>
<ul><li><strong>Becas y exposiciones:</strong> cada ítem lleva una barra a la izquierda y el año en color, alternando celeste, amarillo, verde y azul. Sin rosa: el rosa es del botón «Listo» de la hoja.</li>
<li><strong>Colaboraciones principales:</strong> cada empresa lleva un subrayado de color, en el orden rosa, celeste, amarillo, verde y azul, y enlaza a su web.</li></ul>
<h3>Etiquetas de confianza</h3>
<p>El método de los informes (verificado, reportado, inferido) se volvió componente, con color y forma propios:</p>
<div class="m-panel"><div class="didi m-demo d-row" style="gap:18px"><span class="d-tag d-tag--verified">{chk} Verificado</span><span class="d-tag d-tag--reported">Reportado</span><span class="d-tag d-tag--inferred">Inferido</span><span class="m-lbl">Verificado: visto en la fuente (verde, píldora) · Reportado: lo dice un tercero (azul, recto) · Inferido: conclusión propia a confirmar (amarillo, D abierta).</span></div></div>
{note('<b>Ya no se usa en el sitio.</b> Las etiquetas de confianza siguen en <code>didi-ui.css</code>, pero la web no las muestra desde 2026: es una vitrina, no un informe (regla 1 de Débora). La fuente de cada cifra está en la hoja de verdad y en las fichas.','m-open')}
{note('<b>Cambio respecto del tablero anterior.</b> En el primer tablero el interruptor encendido era verde. Pasó a celeste: la selección es «qué está activo» (navegación).','m-ok')}'''))

# ---- tipografía
tscale=[('display-l','d-display-l','57 / 64','700','−0,25 px','No se usa: demasiado grande para el portfolio.'),('display-m','d-display-m','45 / 52','700','0','Títulos grandes de los componentes (escritorio).'),('display-s','d-display-s','36 / 44','700','0','Títulos grandes de los componentes (celular); cifras grandes.'),
 ('headline-l','d-headline-l','32 / 40','600','0','Título de sección.'),('headline-m','d-headline-m','28 / 36','600','0','Título de caso.'),('headline-s','d-headline-s','24 / 32','600','0','Subtítulo, título de diálogo.'),
 ('title-l','d-title-l','22 / 28','600','0','Título de tarjeta.'),('title-m','d-title-m','16 / 24','600','+0,15 px','Título de lista, ítem destacado.'),('title-s','d-title-s','14 / 20','600','+0,1 px','Encabezado de tabla de texto.'),
 ('body-l','d-body-l','16 / 24','400','+0,5 px','Texto de lectura.'),('body-m','d-body-m','14 / 20','400','+0,25 px','Texto secundario.'),('body-s','d-body-s','12 / 16','400','+0,4 px','Pie de foto, nota.'),
 ('label-l','d-label-l','14 / 20 · mono','500','+0,1 px','Etiqueta de tile, enlace de navegación mono.'),('label-m','d-label-m','12 / 16 · mono','500','+0,5 px','Metadatos, chips de dato.'),('label-s','d-label-s','11 / 16 · mono','400','+0,5 px','Micro-etiqueta, ayuda de campo.')]
scale_html=''.join(f'<tr><td class="n">{n}</td><td><span class="didi {c}" style="background:none;display:block">Débora Malqui · Dirigí</span></td><td class="n">{sz}</td><td class="n">{w}</td><td class="n">{tr}</td><td>{u}</td></tr>' for n,c,sz,w,tr,u in tscale)
stem_rows=''.join(f'<tr><td class="n">{n}</td><td class="n">{w}</td><td class="n">{s}</td><td><span style="font-family:\'DiDi Sans\';font-weight:{w};font-size:2.25rem;line-height:1">DiDí</span></td></tr>' for n,w,s in (('Regular',400,84),('Medium',500,99),('SemiBold',600,116),('Bold',700,137),('ExtraBold',800,161)))
out.append(sec('tipografia','Tipografía','Una fuente propia derivada de Figtree y DM Mono, con una sola modificación: todas las D mayúsculas son sin palo, como la del logo.',f'''
<h3>DiDi Sans y DiDi Mono</h3>
<div class="m-panel"><div class="didi m-demo"><div class="d-display-m" style="font-weight:800">DiDí Diseño</div><div class="d-headline-s" style="margin-top:14px">Datos · Dirección · Diagnóstico · Demo · Disponible</div><div class="d-label-l d-caps" style="margin-top:14px;color:#80ECEC">Datos · DNS · DDMMYY · ADD · Diagnóstico</div><p class="d-body-l" style="margin:14px 0 0;max-width:64ch">Dos años con una cadena de accesorios sin equipo de marketing: 27 páginas en vivo y un protocolo que encontró 1.531 postulaciones de 3 personas. Dirigí el desarrollo, definí cada dato y lo validé contra la fuente.</p></div></div>
<p><strong>DiDi Sans</strong> (cuerpo, títulos, botones) parte de Figtree, de diseño geométrico y redondeado, afín a las curvas del logo. <strong>DiDi Mono</strong> (etiquetas, cifras, metadatos, código) parte de DM Mono. Las dos son OFL: se pueden modificar y redistribuir conservando la licencia (archivos en <code>fuentes/</code>). Se renombraron para no usar los nombres originales.</p>
<h3>La D sin palo</h3>
<p>La D del logo no tiene asta vertical: línea de arriba, semicírculo, línea de abajo. En la fuente, la D mayúscula se dibujó igual, con el trazo del peso correspondiente (el ancho del palo de la "I" de cada peso). Es una sola modificación: el resto de las letras es la fuente original. La d minúscula no se toca: sin palo dejaría de ser una d.</p>
{table(['Peso','CSS','Trazo de la D (u de 1000)','Muestra'],[[*r.split('|')] for r in []]) if False else f'<table class="m-t"><tr><th>Peso</th><th>CSS</th><th>Trazo (1000 u/em)</th><th>Muestra</th></tr>{stem_rows}</table>'}
<div class="m-panel"><div class="didi m-demo d-row" style="gap:48px;align-items:flex-end"><div><div style="font:400 300px/.8 var(--d-sans);color:#E6ECF5;height:210px">D</div><span class="m-lbl">DiDi Sans 400, D de 300 px</span></div><div class="d-headline-l" style="font-weight:700">DA DO DE DV<br>AD OD ED VD<br>DÓNDE DIDÍ</div></div></div>
<h3>El costo de lectura, y la reserva</h3>
{note('<b>Lo que hay que saber.</b> En texto corrido chico, una D sin palo se parece a una C al revés: "Dirigí" a 16 px se lee casi como "ɔirigí". En el nombre, los títulos y las etiquetas se resuelve por contexto y por tamaño. En párrafos largos tiene un costo de lectura. Es una observación propia, no una prueba con personas.','m-open')}
<p>Por eso las dos fuentes traen la D clásica como característica OpenType <strong>ss20</strong>, apagada por defecto. Si se decide usarla en los párrafos de lectura, es una línea: <code>.d-prose {{ font-feature-settings: "ss20"; }}</code>.</p>
<div class="m-two"><div class="m-panel"><div class="didi m-demo"><div class="m-lbl" style="margin:0 0 8px">Todas sin palo (por defecto)</div><p class="d-body-l" style="margin:0">Dos años con una cadena de accesorios. Dirigí el desarrollo, definí cada dato y lo validé. Del diagnóstico al dashboard, nada se da por sentado: ni el DNS ni el dominio.</p></div></div><div class="m-panel"><div class="didi m-demo"><div class="m-lbl" style="margin:0 0 8px">Con ss20 (D clásica en el párrafo)</div><p class="d-body-l d-prose" style="margin:0">Dos años con una cadena de accesorios. Dirigí el desarrollo, definí cada dato y lo validé. Del diagnóstico al dashboard, nada se da por sentado: ni el DNS ni el dominio.</p></div></div></div>
{note('<b>Decisión pendiente.</b> Mientras no se decida, la regla es: sin palo en todo. Propuesta a considerar: clásica solo en párrafos de lectura de más de dos líneas a 16 px o menos.','m-open')}
<h3>Escala de la interfaz</h3>
<table class="m-t"><tr><th>Rol</th><th>Muestra</th><th>Tamaño / interlineado (px)</th><th>Peso</th><th>Espacio entre letras</th><th>Uso</th></tr>{scale_html}</table>
<p class="m-lbl">Tamaños e interlineados de la escala estándar que se tomó como base para los componentes; los pesos son decisión propia. Las etiquetas van en DiDi Mono. La primera columna es el nombre de la clase en <code>didi-ui.css</code>.</p>
<h3>Escala del sitio</h3>
<p>Las páginas del sitio usan tamaños propios, que crecen con el ancho de la pantalla (entre un mínimo en celular y un máximo en computadora):</p>
{table(['Dónde','Tamaño','Peso','Detalle'],[
 ['Nombre en la portada','de 40 a 64 px','Bold 700','Interlineado 1,02; espacio entre letras −0,02 em.'],
 ['Títulos de sección grandes («Casos», «Trabajos académicos y pasantías»)','de 40 a 88 px','ExtraBold 800','Interlineado 0,98; espacio entre letras −0,035 em; como máximo 16 caracteres por línea.'],
 ['Cantidad junto al título','de 14 a 18 px','DiDi Mono 500','Celeste; azul en trabajos académicos. Va arriba, al lado del título.'],
 ['Presentación de la portada','de 17 a 20 px','Regular 400','Interlineado 1,6; hasta 58 caracteres por línea.'],
 ['Frase corta de la portada','la misma','SemiBold 600','Presenta lo que se ve en la laptop; «Probalo» enlaza a la demo.'],
 ['Título de un caso','de 30 a 44 px','Bold 700','Con una línea de 72 × 4 px del color del tipo debajo.'],
 ['Subtítulo dentro de un caso','28 px','SemiBold 600','Con un punto de 10 px del color del tipo adelante.'],
 ['Párrafo de un caso','17 px','Regular 400','Interlineado 1,65; hasta 66 caracteres por línea.'],
 ['Título de tarjeta de caso','16 px (destacadas: de 20 a 26 px)','Bold 700','Debajo, la bajada en 14 px y el año y el tipo en DiDi Mono de 11 px.'],
 ['Idiomas de la barra','13 px','SemiBold 600','En DiDi Sans y no en la mono, para que la barra no se mueva al cargar. «עב» con la letra hebrea del sistema.']])}
<h3>Reglas de texto</h3>
<ul><li>Párrafos de lectura: 60 a 72 caracteres por línea. Interlineado 1,5.</li><li>Un solo H1 por página. Los títulos no saltan de nivel.</li><li>Mayúsculas sostenidas solo en etiquetas mono (con espaciado de 0,08 em), nunca en cuerpo.</li><li>Cifras: tabulares (<code>font-variant-numeric: tabular-nums</code>) en tiles y tablas. Separador de miles según idioma: 1.520 en español, 1,520 en inglés.</li><li>El mono no se usa para párrafos.</li><li>Letra de reserva: <code>system-ui</code>, con <code>font-display: swap</code>.</li><li>Carga en dos tandas. Con la página: DiDi Sans Regular, SemiBold y Bold (precargadas). Después del primer pantallazo: Medium, ExtraBold y las dos DiDi Mono. Así el sitio llega a 100 en velocidad.</li></ul>
{note('<b>Tres idiomas.</b> DiDi Sans y DiDi Mono cubren el latín, no el hebreo. En las páginas en hebreo se usa la <strong>Heebo</strong> (licencia OFL), incluida en el sitio: solo el bloque hebreo, 20 KB, precargada y con <code>font-display: block</code> para que la portada no se corra al llegar la letra. El hebreo no tiene D, así que la regla de la D sin palo no cambia, y los nombres en latín conservan DiDi Sans. Sin espacio entre letras ni mayúsculas en hebreo.','m-ok')}'''))

for _f in ('manual_b','manual_c','manual_d','manual_e'):
    _p=pathlib.Path(__file__).resolve().parent/f'{_f}.py'
    if _p.exists(): exec(compile(_p.read_text(),str(_p),'exec'),globals())

# ============================== ARMADO ==============================
import re as _re
# Débora pidió todo en español: los nombres en inglés que vienen de la v1 se pasan al español solo en el texto visible
# (no en clases, atributos, estilos, scripts ni código).
_ES=[('Extended FAB','Botón flotante extendido'),('FAB menu','Menú del botón flotante'),('FABs','botones flotantes'),('FAB','botón flotante'),
 ('Icon buttons','Botones de ícono'),('Buttons','Botones'),('Button groups','Grupos de botones'),('Segmented buttons','Botones segmentados'),('Split button','Botón dividido'),
 ('Floating action button','Botón flotante'),('App bars','Barras superiores'),('Toolbars','Barras de herramientas'),('Navigation bar','Barra de navegación inferior'),
 ('Navigation rail','Riel de navegación'),('Navigation drawer','Cajón de navegación'),('Tabs','Pestañas'),('Search','Búsqueda'),('Chips','Fichas'),('Checkbox','Casilla'),
 ('Radio button','Botón de opción'),('Switch','Interruptor'),('Sliders','Deslizadores'),('Text fields','Campos de texto'),('Date pickers','Selectores de fecha'),('Time pickers','Selectores de hora'),
 ('Cards','Tarjetas'),('Lists','Listas'),('Carousel','Carrusel'),('Divider','Divisor'),('Dialogs','Diálogos'),('Bottom sheets','Hojas inferiores'),('Side sheets','Hojas laterales'),
 ('Menus','Menús'),('Tooltips','Ayudas emergentes'),('Snackbar','Aviso breve'),('Progress indicators','Indicadores de progreso'),('Loading indicator','Indicador de carga'),('Badges','Marcas'),
 ('Assist','De ayuda'),('Filter','Filtro'),('Input','Ingresados'),('Suggestion','Sugerencia'),('multi-browse','varias a la vez'),('Multi-browse','Varias a la vez'),('hero','principal'),
 ('hover','al pasar el mouse'),('Hover','Al pasar el mouse'),('tooltip','ayuda emergente'),('snackbar','aviso breve'),('chips','fichas'),('chip','ficha'),('tiles','baldosas'),('tile','baldosa'),
 ('badge','marca'),('toggle','alternado'),('stack','herramientas'),('STACK','HERRAMIENTAS'),('Tracking','Espacio entre letras'),('tracking','espacio entre letras'),('tokens','variables'),('token','variable'),('Tokens','Variables'),
 ('scroll','desplazamiento'),('mockup','maqueta'),('dashboard','tablero'),('Dashboard','Tablero'),('checkbox','casilla'),('reflow','reacomodo'),('compact','celular'),('XS','extrachico'),('Compact','Celular'),('Medium','Mediano'),('Expanded','Ampliado')]
_ES.sort(key=lambda kv:-len(kv[0]))
_PAT=_re.compile(r'(?<![-\w])('+'|'.join(_re.escape(k) for k,_ in _ES)+r')(?![-\w])')
_MAP=dict(_ES)
def espanol(doc):
    keep=[]
    def _hold(m): keep.append(m.group(0)); return f'\x00{len(keep)-1}\x00'
    doc=_re.sub(r'<div class="m-pre">.*?</div>',_hold,doc,flags=_re.S)
    out=[];skip=0
    for tok in _re.split(r'(<[^>]+>)',doc):
        if tok.startswith('<'):
            t=tok.lower()
            if _re.match(r'<(style|script|code)\b',t): skip+=1
            elif _re.match(r'</(style|script|code)>',t): skip=max(0,skip-1)
            out.append(tok)
        else:
            out.append(tok if skip else _PAT.sub(lambda m:_MAP[m.group(1)],tok))
    return _re.sub('\x00(\\d+)\x00',lambda m:keep[int(m.group(1))],''.join(out))
# Versión pública: sin scripts, comandos, rutas ni archivos internos, y en primera persona (Débora, 2026: «se dice que hago yo»)
PUB_TXT=[
 ('el portfolio de Débora Malqui','mi portfolio'),
 ('Las cifras de contraste y de verificación las calcula el generador; no están escritas a mano.','Las cifras de contraste y de verificación se calculan; no están escritas a mano.'),
 ('Las fuentes de cada cifra viven en la hoja de verdad y en las fichas.','Cada cifra tiene su fuente documentada, aunque no se muestre en la página.'),
 ('aprobada por Débora','que elegí'),
 ('La cifra tiene que estar en la hoja de verdad o en una ficha; si no está, no se publica.','Cada cifra tiene su fuente documentada; si no la tiene, no se publica.'),
 (' (regla de Débora: la web es una vitrina)',' (la web es una vitrina)'),
 ('La fuente queda en la ficha del caso, no en la página.','La fuente queda documentada, no en la página.'),
 ('Un tipo nuevo cae en celeste hasta que se le asigne un color (<code>TONES</code> en el generador del sitio).','Un tipo nuevo va en celeste hasta que tenga su color.'),
 ('Las etiquetas de confianza siguen en <code>didi-ui.css</code>, pero la web no las muestra desde 2026: es una vitrina, no un informe (regla 1 de Débora). La fuente de cada cifra está en la hoja de verdad y en las fichas.','Las etiquetas de confianza siguen en el sistema, pero la web no las muestra desde 2026: es una vitrina, no un informe. Cada cifra tiene su fuente documentada.'),
 ('La primera columna es el nombre de la clase en <code>didi-ui.css</code>.','La primera columna es el nombre de cada tamaño en el sistema.'),
 ('verificado por script','verificado en cada publicación'),
 (' (archivos en <code>fuentes/</code>)',''),
 ('no de una prueba en pantalla real a 1×. Ver sección 28.','no de una prueba en pantalla real a 1×.'),
 ('siguen dibujadas en <code>didi-ui.css</code>, pero el sitio no las muestra. La fuente de cada cifra vive en la hoja de verdad y en las fichas.','siguen en el sistema, pero el sitio no las muestra. Cada cifra tiene su fuente documentada.'),
 ('La portada presenta a Débora con una frase, muestra su propio producto funcionando','La portada me presenta con una frase, muestra mi propio producto funcionando'),
 (' (pedido de Débora, 2026)',''),
 ('Vive en la ficha interna, no en la página.','Queda en mis notas internas, no en la página.'),
 ('el componente sigue en <code>didi-gestos.js</code>.','el componente sigue en el sistema.'),
 ('<b>Cómo se verificó.</b> Un script abre cada gesto en un navegador real y comprueba el resultado','<b>Cómo lo verifico.</b> Antes de publicar, pruebo cada gesto en un navegador real y compruebo el resultado'),
 ('Lo automático se corre con un script; lo que no se puede automatizar se prueba con personas.','Lo medible lo controlo en cada publicación, página por página; lo que no se puede medir así, lo pruebo con personas.'),
]
PUB_RE=[
 (r'<p class="[^"]*m-privado[^"]*">.*?</p>',''),
 (r'<h3>Archivos</h3>\s*<p><code>marca/didi-logo\.svg</code>.*?</p>',''),
 (r'Dentro del caso, el color del tipo \(<code>--tone</code>\) va en:','Dentro del caso, el color del tipo va en:'),
 (r'se espeja con un bloque <code>\[dir="rtl"\]</code> al final de didi-ui\.css:','se espeja:'),
 (r'\s*Se mide con <code>npx lighthouse[^<]*</code>[^.]*?<code>[^<]*</code>\.',''),
 (r'<tr>(?:(?!</tr>).)*prototipos/(?:(?!</tr>).)*</tr>',''),
]
def publico(doc):
    for a,b in PUB_TXT: doc=doc.replace(a,b)
    for a,b in PUB_RE: doc=_re.sub(a,b,doc,flags=_re.S)
    return doc
def build():
    toc=['<a class="m-brand" href="#top">'+logo(w=120)+'</a><p class="m-ver">Manual · v2 · 2026</p><p style="margin:-12px 0 22px"><a href="manual-didi-v2.pdf" download style="color:#80ECEC;font:500 .8125rem/1.25rem var(--d-sans)">Descargar en PDF</a></p>']
    # el índice va dentro de un <details>: abierto en computadora; en celular se pliega (script de abajo) para que primero se vea la tapa
    toc.append(f'<details class="m-tocd" open><summary>Índice · {sum(1 for x in SECS if x[0]!="PART")} secciones</summary><nav aria-label="Índice">')
    for kind,a,b,c in SECS:
        if kind=='PART': toc.append(f'<h4>{a}</h4>')
        else: toc.append(f'<a href="#{a}">{b:02d} · {c}</a>')
    toc.append('</nav></details><script>(function(){var d=document.querySelector(".m-tocd"),m=matchMedia("(max-width:900px)");function f(){if(m.matches)d.removeAttribute("open");else d.setAttribute("open","")}f();m.addEventListener("change",f);d.addEventListener("click",function(e){if(e.target.closest("a")&&m.matches)d.removeAttribute("open")})})();</script>')
    doc=('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
         '<title>DiDí · manual de marca v2</title><style>'+_re.sub(r'/\*.*?\*/','',UI_CSS,flags=_re.S)+(ROOT/'manual'/'manual-v2.css').read_text()+'</style></head>'
         '<body class="didi" id="top"><div class="m-shell"><aside class="m-toc">'+''.join(toc)+'</aside><main class="m">'+espanol(''.join(out))+'</main></div></body></html>')
    if PUBLICO: doc=publico(doc)
    p=ROOT/'manual'/('manual-didi-v2-publico.html' if PUBLICO else 'manual-didi-v2.html'); p.write_text(doc); return p,len(doc)
if __name__=='__main__': print(build())
