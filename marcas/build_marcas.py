"""Genera marcas/index.html: la página de casos de marca (Medido, DiDí, Danzas Circulares y Ziconex).
Un solo archivo con los datos de los cinco casos. Las imágenes viven en img/ (capturas y recortes) y logos/ (archivos finales).
Las tipografías DiDi Sans y DiDi Mono van embebidas (base64) para que la página no dependa de ningún host.
Escribe también published-files.json con la lista exacta de archivos que usa la página."""
import base64, html, json, os, re

B = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(B), "fuentes")
USED = set()

def esc(s): return html.escape(s, quote=True)

def use_asset(path):
    USED.add(path); return path

def lum(hexc):
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ink_on(hexc): return "#0F1B2D" if lum(hexc) > 0.35 else "#FFFFFF"

# ---------------------------------------------------------------- piezas de HTML
def tile(src, caption, bg, alt=None, multi=None, wide=False, gif=None):
    """Una versión del logo sobre su superficie. multi: lista de (archivo, px) para mostrar tamaños reales."""
    if multi:
        inner = "".join(f'<img src="{use_asset(f)}" width="{px}" height="{px}" style="width:{px}px;height:{px}px" alt="">' for f, px in multi)
        cls = "tile tile--multi"
    elif gif:
        use_asset(src); use_asset(gif)
        inner = (f'<img class="gif-img" src="{src}" data-still="{src}" data-gif="{gif}" alt="{esc(alt or caption)}">'
                 f'<button type="button" class="play" aria-label="Reproducir el movimiento del logo">Reproducir</button>')
        cls = "tile tile--gif"
    else:
        inner = f'<img src="{use_asset(src)}" alt="{esc(alt or caption)}" loading="lazy">'
        cls = "tile"
    if wide: cls += " tile--wide"
    return f'<figure class="{cls}" style="--t:{bg}"><div class="surface">{inner}</div><figcaption>{esc(caption)}</figcaption></figure>'

def step(title, text, img=None, alt="", media=None):
    if media:
        return f'<li class="step step--wide"><div class="step-text"><h4>{esc(title)}</h4><p>{text}</p></div><div class="step-media">{media}</div></li>'
    media = ""
    if img:
        media = (f'<button type="button" class="shot" data-zoom="{use_asset(img)}" aria-label="Ampliar: {esc(title)}">'
                 f'<img src="{img}" alt="{esc(alt or title)}" loading="lazy"></button>')
    return f'<li class="step{"" if img else " step--text"}"><div class="step-text"><h4>{esc(title)}</h4><p>{text}</p></div>{media}</li>'

def usage(img, caption, alt="", portrait=False, square=False):
    cls = "use" + (" use--portrait" if portrait else "") + (" use--square" if square else "")
    return (f'<figure class="{cls}"><button type="button" class="shot" data-zoom="{use_asset(img)}" aria-label="Ampliar: {esc(caption)}">'
            f'<img src="{img}" alt="{esc(alt or caption)}" loading="lazy"></button><figcaption>{esc(caption)}</figcaption></figure>')

def swatches(items):
    out = []
    for name, hexc, note in items:
        out.append(f'<li><span class="chip" style="background:{hexc};color:{ink_on(hexc)}"></span>'
                   f'<span class="sw-text"><b>{esc(name)}</b><code>{esc(hexc)}</code>{f"<em>{esc(note)}</em>" if note else ""}</span></li>')
    return '<ul class="swatches">' + "".join(out) + "</ul>"

def spec(rows):
    return '<dl class="spec">' + "".join(f"<div><dt>{esc(k)}</dt><dd>{v}</dd></div>" for k, v in rows) + "</dl>"

def case(cid, name, year, kind, lede, stage_html, stage_bg, idea, facts, steps, tiles, uses, ficha, note="", tiles_cls=""):
    chips = "".join(f"<li>{esc(c)}</li>" for c in kind[1])
    return f'''<section class="case" id="{cid}" aria-labelledby="h-{cid}">
  <header class="case-head">
    <p class="kicker">{year} · {esc(kind[0])}</p>
    <h2 id="h-{cid}">{esc(name)}</h2>
    <p class="lede">{lede}</p>
    <ul class="chips" aria-label="Qué incluyó">{chips}</ul>
  </header>
  <div class="stage" style="--s:{stage_bg}">{stage_html}</div>
  <div class="idea-row">
    <div class="idea"><h3 class="label">La idea</h3>{idea}</div>
    {spec(facts)}
  </div>
  <h3 class="label">Camino</h3>
  <ol class="path">{"".join(steps)}</ol>
  {note}
  {f'<h3 class="label">Versiones</h3><div class="tiles{" " + tiles_cls if tiles_cls else ""}">{"".join(tiles)}</div>' if tiles else ""}
  {f'<h3 class="label">Usos</h3><div class="uses">{"".join(uses)}</div>' if uses else ""}
  <h3 class="label">Ficha técnica</h3>
  <div class="ficha">{ficha}</div>
</section>'''

def stage_logo(*srcs, alt, gap=False):
    return "".join(f'<img src="{use_asset(s)}" alt="{esc(alt)}">' for s in srcs)

CENTRO = json.load(open(os.path.join(B, "img/dcs-m-centro.json")))   # centro de la flor, lo calcula prep_dcs_morph.py
MORPH = (
    f'<figure class="morph" id="clavel" style="--cx:{CENTRO["cx"]}%;--cy:{CENTRO["cy"]}%">'
    '<div class="m-stage" role="img" aria-label="Animación: la foto de un clavel se simplifica en los colores de la marca, se dibuja la línea, aparece el color y el nombre en arco">'
    '<div class="m-turn"><img class="m-foto" src="' + use_asset("img/dcs-m-foto.webp") + '" alt=""><img class="m-poster" src="' + use_asset("img/dcs-m-poster.webp") + '" alt=""></div>'
    '<img class="m-lineas" src="' + use_asset("img/dcs-m-lineas.svg") + '" alt=""><img class="m-color" src="' + use_asset("img/dcs-m-color.svg") + '" alt="">'
    '<img class="m-texto" src="' + use_asset("img/dcs-m-texto.svg") + '" alt=""></div>'
    '<figcaption class="m-bar"><ol class="m-steps"><li>Foto</li><li>Síntesis</li><li>Línea</li><li>Color</li><li>Nombre</li></ol>'
    '<button type="button" class="m-replay">Ver de nuevo</button></figcaption></figure>')

use_asset("logos/didi-monograma-Di.svg")   # lo usa la tarjeta «Just for fun, brands» de Sobre mí
use_asset("logos/zic-avatar.webp")   # lo usa la tarjeta «Just for fun, brands» de Sobre mí

# ---------------------------------------------------------------- CASOS
cases = []

# ---- Medido ----
M = "logos/medido-"
cases.append(case(
    "medido", "Medido", "2026", ("Identidad completa", ["Logo", "Hebreo", "Paleta", "Tipografía", "Manual", "Sitio web"]),
    "Una segunda opinión sobre lo que un negocio paga en marketing, en Estados Unidos e Israel, en inglés y en hebreo. La marca tenía que sentirse como un instrumento de medir sin dibujar uno.",
    stage_logo(M + "logo-sobre-negro.svg", alt="Logo de Medido, marca blanca con la o final como anillo amarillo"), "#0E0F12",
    "<p>El nombre dice lo que hace. La o final es un anillo lleno al 66 %, en sentido horario: una medición que muestra lo que hay y lo que falta, que es la regla de toda la marca.</p>"
    "<p>El hueco del anillo es idéntico al hueco de la d. En hebreo, la vav final se llena igual, hasta el techo de la dalet. El amarillo solo existe sobre negro o como fondo detrás de negro.</p>",
    [("Rol", "Diseño de la marca, el manual y el sitio"), ("Entregables", "Logo en tres superficies y en hebreo, anillo, favicon, avatar, tablero de entrega, manual y web"), ("Estado", "Logo cerrado y entregado")],
    [step("Cuatro direcciones, nueve referencias", "Un tablero con cuatro mundos (cinta métrica, libro mayor, instrumento y topografía), armado con nueve sitios de referencia y los premios de diseño web del mes. Quedó la base de libro mayor, el informe que un contador firmaría, con la tipografía del instrumento.", "img/medido-1-tablero.webp", "Tablero de Medido, dirección A «Cinta métrica»: titular «Pagás marketing todos los meses. ¿Sabés qué recibís?», logo amarillo y negro, paleta y tarjeta de datos"),
     step("Seis paletas", "Sobre esa base armé seis paletas, cada una aplicada a un informe de muestra con su contraste calculado. Ninguna convenció todavía.", "img/medido-2b-paletas.webp", "Tablero de paletas de Medido: titular en español y hebreo, botón y estado de cuenta de muestra en dos paletas"),
     step("Lo obvio se descartó", "La regla y la cinta métrica quedaron afuera porque dicen construcción y no marketing. Después probé cinco símbolos de buscador: la o como lupa, el nombre dentro del buscador, el primer resultado, la respuesta y el clic. Tampoco.", "img/medido-2c-buscador.webp", "Tablero con cinco conceptos de símbolo para Medido: la o como lupa, buscador, primer resultado, globo y cursor."),
     step("Seis marcas hechas solo con letras", "Pasé a marcas sin ícono: el punto final, la M como gráfico, el resaltador, el bloque, la o que se completa y la pendiente. Quedó la quinta.", "img/medido-2-conceptos.webp", "Dos conceptos de logo para Medido: «Medido.» con punto azul y una M trazada como curva, sobre blanco y negro"),
     step("La o como anillo", "Medí el anillo sobre la o real de doce tipografías, con hebreo en todas, hasta que calzara con la palabra. Quedaron tres finalistas: Plus Jakarta Sans, Manrope y Schibsted Grotesk.", "img/medido-3-anillo.webp", "Logo Medido con la o anillo en tres tipografías finalistas, sobre blanco y negro, con versión en hebreo y favicons"),
     step("El logo real, en ocho paletas", "Con el anillo elegido, pasé el logo a contornos reales y lo probé en ocho paletas, con el favicon, el avatar y las etiquetas de confianza al lado.", "img/medido-4b-colores.webp", "Tablero con el logo Medido en seis de ocho paletas, sobre fondo claro y oscuro, con versión en hebreo, favicon y avatar"),
     step("Negro y amarillo, con el contraste calculado", "Probé siete amarillos. El cálculo mostró que el amarillo sobre blanco rinde entre 1,2 y 2,1, y sobre negro entre 8,9 y 16,6. De ahí la regla: el amarillo va sobre negro o detrás de negro, nunca como letra sobre claro.", "img/medido-4-color.webp", "Tablero de tres amarillos (Sol, Ámbar, Lima) con el logo Medido sobre negro, amarillo y blanco, y sus ratios de contraste"),
     step("Plus Jakarta contra Manrope", "Las dos finalistas, con el mismo amarillo, el mismo anillo y las mismas superficies, lado a lado. Ganó Manrope 800, con más identidad, y Assistant 800 para el hebreo.", "img/medido-4c-manrope.webp", "Comparación lado a lado de la marca Medido en Plus Jakarta Sans 800 y en Manrope 800, con el mismo amarillo, sobre negro, amarillo y blanco"),
     step("Ajustes de ojo entrenado", "El hueco de la o pasó a ser el de la d. El anillo quedó al 66 %. En hebreo, el corte de la vav coincide con una línea de la dalet.", "img/medido-5-hueco.webp", "Antes y ahora del logo Medido: el hueco de la «o» pasa a ser idéntico al de la «d», 251×328."),
     step("Entrega", "Versiones, anillo, favicon y avatar, espacio de respeto, tamaños mínimos y qué no hacer, todo en un tablero. Los archivos van en contornos, sin depender de la fuente. Después vinieron el manual y el sitio.", "img/medido-6-entrega.webp", "Tablero de versiones del logo de Medido: sobre negro, amarillo y blanco, en un color, y en hebreo con la vav llena.")],
    [tile(M + "logo-sobre-negro.svg", "Sobre negro (principal)", "#0E0F12", alt="Logo de Medido, versión sobre negro: nombre en blanco y una o final en forma de anillo amarillo lleno al 66 %."),
     tile(M + "logo-sobre-blanco.svg", "Sobre blanco, sin amarillo", "#FFFFFF", alt="Logo de Medido sobre blanco, sin amarillo: letras negras y la o final como anillo parcialmente lleno en gris"),
     tile("logos/medido-logo-sobre-amarillo.svg", "Sobre amarillo", "#FFD60A", alt="Logo de Medido en negro, con la o final como anillo parcialmente lleno en gris, versión sobre amarillo"),
     tile(M + "he-sobre-negro.svg", "Hebreo, sobre negro", "#0E0F12", alt="Logo de Medido en hebreo sobre negro, con la vav final llena en amarillo"),
     tile(M + "he-sobre-blanco.svg", "Hebreo, sobre blanco", "#FFFFFF", alt="Logo de Medido en hebreo, «מדידו», en negro, letras gruesas; la vav final es un anillo lleno"),
     tile(M + "logo-un-color-negro.svg", "Un color, negro", "#FFFFFF", alt="Logo de Medido en negro, de un solo color, con la o final como anillo parcialmente lleno."),
     tile(M + "logo-un-color-blanco.svg", "Un color, blanco", "#0E0F12", alt="Logo de Medido en versión de un color, blanco, sobre negro"),
     tile(M + "anillo-sobre-negro.svg", "Anillo solo", "#0E0F12", alt="Anillo amarillo de Medido, abierto a la izquierda, sobre negro: la o final del logo, llena al 66 %."),
     tile(M + "favicon.svg", "Favicon", "#2A2B30", multi=[(M + "favicon.svg", 64), (M + "favicon.svg", 32), (M + "favicon.svg", 16)]),
     tile(M + "avatar-lupa.svg", "Avatar de Lupa, el agente", "#2A2B30", alt="Avatar de Lupa, el agente: la o de Medido como anillo amarillo lleno al 66 % sobre un círculo negro")],
    [usage("img/medido-web-en.webp", "Sitio en inglés", "Inicio del sitio de Medido en inglés: titular «Before you renew your agency, read what you actually have.» y campo para pegar la web"),
     usage("img/medido-web-he.webp", "El mismo sistema en hebreo, de derecha a izquierda", "Sitio de Medido en hebreo, de derecha a izquierda: título, lista de lo que se recibe y campo para pegar la dirección web."),
     usage("img/medido-web-movil.webp", "En el celular", "Sitio de Medido en el celular: el título «Before you renew your agency, read what you actually have.» y un campo para pegar una web.", portrait=True)],
    swatches([("Negro", "#0E0F12", ""), ("Amarillo Sol", "#FFD60A", "13,6:1 sobre negro"), ("Blanco", "#FFFFFF", ""), ("Gris de apoyo", "#A7ADB8", "8,5:1 sobre negro")]) +
    spec([("Tipografía", "Manrope 800 para el logo y los títulos, Assistant 800 para el hebreo, JetBrains Mono para datos."),
          ("Espacio de respeto", "x es el alto de la o. Libre en los cuatro lados."),
          ("Tamaño mínimo", "72 px de ancho en pantalla (20 mm impreso), 64 px en hebreo. Debajo, solo el anillo."),
          ("Regla de color", "El amarillo solo sobre negro o como fondo detrás de negro. Nunca letra amarilla sobre claro.")])))

# ---- DiDí ----
D = "logos/didi-"
cases.append(case(
    "didi", "DiDí", "2026", ("Marca personal", ["Logo vectorial", "Una tinta", "Favicon", "Movimiento", "Tipografía propia"]),
    "El logo de mi propio portfolio. Existía solo como una imagen de 380 × 193 px. Lo reconstruí en vector midiendo cada forma, lo ajusté y lo convertí en sistema.",
    stage_logo(D + "logo.svg", alt="Logo de DiDí, dos D abiertas rosa y amarilla con barras celeste y azul y un acento verde"), "#0F1B2D",
    "<p><span class=\"is-didi\">DiDí</span> se lee sin tipografía: dos D abiertas, sin asta, y dos barras cortas, con un acento inclinado a −50° que es la única diagonal y tuerce todo lo demás. La D rosa entra cortada desde el borde: ese corte es el movimiento del logo.</p>"
    "<p>Cinco pasteles de luminosidad parecida, que se leen como una familia. Di, Dí: dos tiempos, el segundo con acento, como se dice el nombre.</p>",
    [("Rol", "Reconstrucción, ajuste y sistema de la marca"), ("Entregables", "Logo vectorial, una tinta clara y oscura, apilado, monograma, favicon, movimiento y dos tipografías"), ("Estado", "En uso en este sitio")],
    [step("Un PNG como único archivo", "El logo solo existía como una imagen recortada de 380 × 193 px, sin vector ni archivo de diseño. Antes de mejorar nada había que reconstruirlo.", "img/didi-1-original.webp", "Logo DiDí: PNG original y vector lado a lado, mapa de diferencias y tabla de coincidencia, 95.4 % en total"),
     step("Medir en vez de redibujar", "Medí cada forma por color (centros, radios, grosores y el ángulo del acento) hasta que el vector coincidió en un 95,4 % con el original. Es el máximo posible: el resto es el borde suavizado de un píxel.", None),
     step("Seis ajustes chicos", "Corregí lo que un ojo entrenado ve como ruido de construcción: tres grosores, dos tamaños de D, tres líneas de base, un hueco distinto en cada sílaba y un acento cortado. No toqué lo que hace que sea este logo: el ángulo, el corte y los cinco colores.", "img/didi-2-ajustes.webp", "Ajustes 1 y 2 del logo DiDí: trazo único de 20 u y dos D del mismo tamaño, con antes, después y superpuesto"),
     step("Fondos y contraste", "Probé cinco fondos con el contraste calculado. Los pasteles pasan 7:1 sobre carbón, grafito y azul noche. Sobre claro hay una versión de la misma familia con más tinta, y una versión de una sola tinta para firmas y sellos.", "img/didi-3-fondos.webp", "Logo DiDí original junto a su reconstrucción, y debajo el logo sobre fondos oscuros con el contraste de cada color"),
     step("Una D sin palo, también en la letra", "Redibujé la D mayúscula de las tipografías del sitio sin asta, con la misma construcción del logo. Nacieron DiDi Sans, sobre Figtree, y DiDi Mono, sobre DM Mono, ambas de licencia abierta. Esta página está escrita con ellas.", "img/didi-4-tipografia.webp", "Comparación de «Débora Malqui» y un párrafo en Figtree 700 y en DiDi Sans, con la D mayúscula sin palo")],
    [],
    [],
    swatches([("Rosa", "#E890CC", "acción"), ("Celeste", "#80ECEC", "navegación"), ("Amarillo", "#DCD060", "atención"), ("Azul", "#70B4F4", "dato"), ("Verde", "#ACEC84", "correcto"), ("Azul noche", "#0F1B2D", "superficie")]) +
    spec([("Tipografía", "DiDi Sans para títulos y texto, DiDi Mono para etiquetas y datos."),
          ("Espacio de respeto", "x = 40 unidades, dos trazos, 0,21 de la altura. La D cortada puede sangrar contra el borde o guardar la misma x, nunca un margen intermedio."),
          ("Tamaño mínimo", "120 px de ancho en pantalla (30 mm impreso). Entre 64 y 120 px solo en barras de navegación sobre carbón. Debajo de 64 px, el monograma Di."),
          ("Una tinta", "Clara (#F2F2F2) sobre carbón, u oscura sobre claro.")])))

# ---- Red Española de Danzas Circulares ----
R = "logos/dcs-"
cases.append(case(
    "danzas-circulares", "Red Española de Danzas Circulares", "2024", ("Logo y marca de un festival", ["Símbolo", "Logotipo del festival", "Folleto", "Mail", "Redes", "Remera"]),
    "La red que reúne a quienes bailan danzas circulares en España, y su primer festival, «Directo al corazón», en Sant Feliu de Llobregat, Barcelona, en 2024.",
    stage_logo(R + "color.webp", alt="Logo de la Red Española de Danzas Circulares, una flor roja y naranja con centro en espiral y el nombre en arco"), "#E9E2B6",
    "<p>Las danzas circulares se bailan en círculo, y la marca lo cuenta: pétalos que giran hasta un centro en espiral, como un círculo de bailarines. La flor es el clavel, la que se asocia con España, y el nombre la rodea en arco para cerrar el círculo.</p>"
    "<p>El festival habla más directo. «Directo al corazón» está escrito con una letra artística a pincel, en rojo, y la o de corazón se vuelve un corazón dibujado de un trazo. Es el mismo grupo con dos voces: la Red, serena, en azul marino y espiral; el festival, directo, en rojo.</p>",
    [("Rol", "Logo de la Red, logotipo del festival y piezas"), ("Entregables", "Símbolo en color y lineal, logotipo del festival, folleto, mail de inscripción, redes y remera"), ("Festival", "2024, Sant Feliu de Llobregat, Barcelona")],
    [step("Empezar por lo evidente", "Primero dibujé una ronda de figuras que giran y un molinete de pétalos. Decían danza, pero no decían España.", "img/dcs-exploracion.webp", "Dos exploraciones del símbolo de la Red Española de Danzas Circulares: una ronda de figuras y un molinete de pétalos"),
     step("Del clavel al símbolo", "Cambié las personas por una flor, el clavel, asociado a España. La animación muestra el camino: la foto, la síntesis en los colores de la marca, la línea que se dibuja girando como una ronda, el color que se abre desde la espiral y el nombre.", media=MORPH),
     step("Círculo y espiral", "Los pétalos giran hacia un centro en espiral: la danza. Quedó en color y en una versión lineal de una tinta. El nombre rodea la flor en arco, en una serifa caligráfica, para que el conjunto sea otro círculo.", None),
     step("El festival, más directo", "Para «Directo al corazón» hice un logotipo propio, con letra artística a pincel y la o convertida en corazón. Empezó en azul y terminó en el rojo de la flor. Una línea chica lo acompaña: «Festival de danzas circulares, primera edición».", None),
     step("El sistema en uso", "Una paleta de cinco colores llevó la marca a un folleto, un mail de invitación con la inscripción, publicaciones para redes, una remera y un mockup de teléfono. Todo se ve abajo, en Usos.", None)],
    [tile(R + "color.webp", "Símbolo y nombre, en color", "#E9E2B6", alt="Logo de la Red Española de Danzas Circulares: un clavel de pétalos rojos y naranjas con centro en espiral y el nombre en arco"),
     tile(R + "lineal.webp", "Versión lineal, una tinta", "#FFFFFF"),
     tile(R + "festival.webp", "Logotipo del festival", "#E9E2B6", wide=True, alt="Logotipo «DIRECTO AL CORAZÓN» en letra artística a pincel roja, con la o final dibujada como un corazón"),
     tile(R + "festival-linea.webp", "Línea del festival", "#E9E2B6", wide=True, alt="Línea del festival: «Festival de danzas circulares, primera edición», en letra artística a pincel azul marino")],
    [usage("img/dcs-sistema.webp", "Folleto, paleta y banner", "Folleto crema con «Red Española de Danzas Circulares» y «Directo al corazón», tarjetas azul y ocre, y paleta de cinco colores"),
     usage("img/dcs-remera.webp", "Remera", "Remera color crema con la marca de la Red Española de Danzas Circulares: flor de clavel roja y naranja con el nombre en arco"),
     usage("img/dcs-redes.webp", "Publicación para redes", "Publicación para redes del primer festival de danzas circulares de España, «Directo al corazón», 2024, Sant Feliu de Llobregat", square=True)],
    swatches([("Azul marino", "#002F49", "contorno y nombre"), ("Rojo", "#D62729", "flor y festival"), ("Naranja", "#F77F00", ""), ("Ámbar", "#FDBF4A", "centro"), ("Crema", "#E9E2B6", "fondo")]) +
    spec([("Tipografía", "Serifa caligráfica en arco para la Red. Letra artística a pincel, con la o corazón, para el festival."),
          ("Colores", "Valores tomados del archivo entregado.")]), tiles_cls="tiles--fila"))   # 6/11, Débora: «que entre en el ancho las 4 cosas»

# ---- Ziconex (sistema de marca a partir de un logo recibido) ----
Z = "logos/zic-"
cases.append(case(
    "ziconex", "Ziconex", "2023", ("Sistema de marca", ["Color", "Ilustración", "Redes", "Afiches", "Lanzamiento", "Landing"]),
    "Terapia online en español para quienes viven fuera de su país. El logo me llegó hecho; a partir de él armé la marca: el color, la ilustración y cada pieza, de las redes y los afiches al lanzamiento y la landing.",
    stage_logo(Z + "logo.webp", alt="Logo de Ziconex: un ícono verde con dos triángulos de reproducción que forman una Z, y el nombre en minúsculas redondeadas"), "#FFFFFF",
    "<p>Una marca de salud mental tiene que sentirse calma antes de decir nada. Sobre el verde del logo sumé un menta suave, nubes y personajes planos de formas simples, que muestran gente real hablando por video sin caer en la foto de banco de imágenes.</p>"
    "<p>El mismo sistema lleva todo: el feed explica la terapia de a un post por vez, los afiches hablan de lo que pasa adentro de cada uno y los avisos repiten la calma del rostro sobre las nubes.</p>",
    [("Rol", "Sistema de marca a partir de un logo recibido"), ("Entregables", "Espacio de respeto del logo, avatares, redes, afiches, avisos del lanzamiento y la landing con el seteo de medición"), ("Cliente", "Ziconex, Inc., terapia online en español (EE. UU., remoto)")],
    [step("El punto de partida", "El logo llegó hecho: dos triángulos de reproducción, como los de una videollamada, que juntos forman la Z. No es diseño mío. Mi trabajo empezó ahí: convertirlo en una marca que se sintiera un lugar seguro.", "img/zic-logo-recibido.webp", "Presentación del logo de Ziconex: el ícono de videollamada más la letra Z dan el símbolo, en verde menta"),
     step("Calma antes que nada", "Al verde del logo le sumé un menta suave y nubes blancas. Un rostro con los ojos cerrados, flotando sobre las nubes, se volvió la imagen de los avisos.", "img/zic-aviso.webp", "Aviso de Ziconex: un rostro ilustrado con los ojos cerrados sobre nubes, fondo menta y el logo con «Terapia online en tu idioma»"),
     step("Un estilo de ilustración", "Personas planas, de formas simples y colores vivos, el estilo que en 2023 se volvió más cálido. Sirve para terapia: muestra gente real en videollamada sin la frialdad de una foto de banco de imágenes.", "img/zic-ilustraciones.webp", "Cuatro ventanas de videollamada con personas ilustradas que saludan, sobre fondos menta y amarillo"),
     step("Explicar la terapia, un post por vez", "En redes, la marca enseña: qué es el psicoanálisis, cómo es una primera sesión, el recorrido terapéutico. Carruseles, posts sueltos y un feed con el mismo verde.", "img/zic-carrusel.webp", "Carrusel «Psicoanálisis explicado» de Ziconex: la portada verde en un monitor y las láminas de colores flotando alrededor"),
     step("El lanzamiento: una frase en todos los tamaños", "Para salir al aire, una sola frase, «Terapia online en tu idioma», y un solo botón, «Conocer más». El rostro sobre las nubes y la frase se adaptaron a cada formato de aviso, del banner al rascacielos, y todos llevaban a la landing.", "img/zic-avisos.webp", "Avisos gráficos de Ziconex en varios tamaños: vertical, apaisado, rascacielos, cuadrado y franja, todos con el rostro sobre nubes y «Terapia online en tu idioma»"),
     step("El seteo de la medición", "La landing repetía la promesa, «Es acá. Psicoterapia online en español», y pedía un solo dato, el correo, para reservar un lugar, arriba y otra vez al final. Dejé armado el recorrido completo (aviso, landing, correo, lista de espera), con Google Tag Manager en la página para registrar cada paso, y las pruebas A/B listas: seis títulos (uno de ellos, «No cualquier psicólogo. Tu terapeuta a la medida»), el texto, el tamaño y el lugar del botón, y un formulario de uno o de dos campos.", "img/zic-landing.webp", "La parte de arriba de la página de Ziconex: el logo, «Es acá. Psicoterapia online en español», un campo de correo y el botón «Reserva tu lugar»")],
    [tile(Z + "logo.webp", "Logo horizontal", "#FFFFFF", wide=True, alt="Logo horizontal de Ziconex sobre blanco"),
     tile(Z + "icono.webp", "Ícono", "#FFFFFF", alt="Ícono de Ziconex en un círculo verde, con los dos triángulos que forman la Z"),
     tile(Z + "avatar.webp", "Avatar para redes", "#13AA65", alt="Avatar de Ziconex: los dos triángulos blancos sobre verde")],
    [usage("img/zic-afiche-mar.webp", "Afiche: «Al igual que el mar, dentro de mí hay profundidades por explorar»", "Afiche ilustrado de Ziconex en un marco sobre un escritorio: una mujer en el mar al atardecer"),
     usage("img/zic-afiche-desierto.webp", "Afiche en marco", "Afiche de Ziconex en un marco apoyado sobre una mesa: un desierto de noche con la luna"),
     usage("img/zic-feed.webp", "Feed de Instagram", "Perfil de Instagram de Ziconex en un celular y sus publicaciones en cuadrícula: «Recorrido terapéutico», «Psicoterapia explicada» e ilustraciones"),
     usage("img/zic-facebook.webp", "Facebook", "La página de Facebook de Ziconex en una computadora portátil y sus publicaciones alrededor, sobre verde"),
     usage("img/zic-lectura.webp", "Post de redes", "Ilustración de un hombre sentado sobre una pila de libros, leyendo, sobre fondo menta"),
     usage("img/zic-historias.webp", "Historias de Instagram", "Cinco historias de Instagram de Ziconex en durazno y verde: videollamada integrada, espacio terapéutico, desarrollo personal, inclusión y empatía, psicólogos expertos")],
    swatches([("Verde", "#13AA65", "logo"), ("Menta", "#ACEACC", "fondos"), ("Verde profundo", "#005607", "carruseles"), ("Negro", "#000000", "nombre")]) +
    spec([("Logo", "Recibido hecho, con su verde. Sumé el espacio de respeto y las versiones para redes."),
          ("Colores", "Valores tomados de los archivos entregados.")])))

# ---------------------------------------------------------------- índice
INDEX = [("medido", "Medido", "2026", "Identidad completa", "logos/medido-logo-sobre-negro.svg", "#0E0F12"),
         ("didi", "DiDí", "2026", "Marca personal", "logos/didi-logo.svg", "#0F1B2D"),
         ("danzas-circulares", "Red Española de Danzas Circulares", "2024", "Logo y marca de un festival", "logos/dcs-color.webp", "#E9E2B6"),
         ("ziconex", "Ziconex", "2023", "Sistema de marca", "img/zic-lectura.webp", "#BCE9CE")]   # 6/11, Débora: la foto del chico leyendo sobre los libros, no el logo
index_html = "".join(
    f'<li><a href="#{i}"><span class="ix-surface" style="--s:{bg}"><img src="{use_asset(src)}" alt="" loading="lazy"></span>'
    f'<span class="ix-meta"><b{" class=\"is-didi\"" if i == "didi" else ""}>{esc(n)}</b><small>{y} · {esc(k)}</small></span></a></li>' for i, n, y, k, src, bg in INDEX)
nav_html = "".join(f'<a href="#{i}"{" class=\"is-didi\"" if i == "didi" else ""}>{esc(short)}</a>' for i, short in (("medido", "Medido"), ("didi", "DiDí"), ("danzas-circulares", "Danzas Circulares"), ("ziconex", "Ziconex")))

# ---------------------------------------------------------------- CSS
def font_face(file, family, weight):
    b64 = base64.b64encode(open(os.path.join(FONTS, file), "rb").read()).decode()
    return f'@font-face{{font-family:"{family}";src:url(data:font/woff2;base64,{b64}) format("woff2");font-weight:{weight};font-display:swap}}'
FONT_CSS = "".join([font_face("DiDiSans-Regular.woff2", "DiDi Sans", 400), font_face("DiDiSans-Medium.woff2", "DiDi Sans", 500),
                    font_face("DiDiSans-Bold.woff2", "DiDi Sans", 700), font_face("DiDiSans-ExtraBold.woff2", "DiDi Sans", 800),
                    font_face("DiDiMono-Regular.woff2", "DiDi Mono", 400)])

CSS = r"""
/* Concepto: un capítulo de portfolio. La página es neutra (azul noche, como el sitio) y cada marca trae su propia superficie. */
:root{
  --bg:#0F1B2D; --bg-2:#0B1424; --panel:#13213A; --panel-2:#172744; --line:#2B3A52;
  --fg:#E6ECF5; --muted:#AAB7C9; --accent:#70B4F4; --accent-ink:#0F1B2D; --shot-line:#35465F;
  --sans:"DiDi Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; --mono:"DiDi Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  color-scheme:dark;
}
@media (prefers-color-scheme: light){ :root:not([data-theme="dark"]){
  --bg:#F3F5F9; --bg-2:#E8ECF3; --panel:#FFFFFF; --panel-2:#EEF1F7; --line:#D3DAE6;
  --fg:#0F1B2D; --muted:#4A5A70; --accent:#1F5FA8; --accent-ink:#FFFFFF; --shot-line:#C5CEDC; color-scheme:light } }
:root[data-theme="light"]{
  --bg:#F3F5F9; --bg-2:#E8ECF3; --panel:#FFFFFF; --panel-2:#EEF1F7; --line:#D3DAE6;
  --fg:#0F1B2D; --muted:#4A5A70; --accent:#1F5FA8; --accent-ink:#FFFFFF; --shot-line:#C5CEDC; color-scheme:light }
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:400 1.0625rem/1.55 var(--sans);-webkit-font-smoothing:antialiased;font-feature-settings:"ss20" 1}
/* Regla del sistema DiDí: la D sin palo es para el nombre y el logo; en texto de lectura va la D clásica (ss20). */
*{font-feature-settings:"ss20" 1 !important}
#h-didi,.is-didi{font-feature-settings:normal !important}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);background:var(--bg);z-index:30}
img{display:block;max-width:100%}
a{color:inherit}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.only-light{display:none}
@media (prefers-color-scheme: light){ :root:not([data-theme="dark"]) .only-light{display:block} :root:not([data-theme="dark"]) .only-dark{display:none} }
:root[data-theme="light"] .only-light{display:block} :root[data-theme="light"] .only-dark{display:none}
.wrap{width:100%;max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}

/* barra */
.bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--bg);border-bottom:1px solid var(--line)}
.bar .wrap{display:flex;align-items:center;gap:20px;min-height:56px}
.bar .brand img{height:26px;width:auto}
.bar nav{display:flex;gap:4px;overflow-x:auto;min-width:0;scrollbar-width:none;margin-left:auto}
.bar nav::-webkit-scrollbar{display:none}
.bar nav a{white-space:nowrap;text-decoration:none;color:var(--muted);font:500 .9375rem/1 var(--sans);padding:12px 12px;border-radius:999px}
.bar nav a:hover{color:var(--fg);background:var(--panel)}

/* apertura */
.hero{padding-block:clamp(40px,8vw,88px) 32px}
.eyebrow,.label,.kicker{font:400 .75rem/1.2 var(--mono);letter-spacing:.09em;text-transform:uppercase;color:var(--muted)}
.hero h1{font:800 clamp(2.4rem,7vw,4.5rem)/1.02 var(--sans);letter-spacing:-.025em;margin:14px 0 20px;text-wrap:balance;max-width:16ch}
.hero p.intro{max-width:60ch;color:var(--muted);font-size:1.1875rem;margin:0}
.index{list-style:none;margin:36px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
@media (max-width:900px){ .index{grid-template-columns:repeat(2,1fr)} }

.index a{display:flex;flex-direction:column;height:100%;text-decoration:none;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--panel)}
.index a:hover{border-color:var(--accent)}
.ix-surface{display:flex;align-items:center;justify-content:center;aspect-ratio:3/2;background:var(--s);padding:14px;overflow:hidden;min-height:0}
.ix-surface img{height:100%;width:auto;max-width:88%;min-height:0;object-fit:contain}
.ix-meta{display:flex;flex-direction:column;gap:2px;padding:12px 14px 14px;min-width:0}
.ix-meta b{font-weight:700;font-size:1rem;line-height:1.25}
.ix-meta small{color:var(--muted);font-size:.8125rem;line-height:1.35}

/* caso */
.case{padding-block:clamp(48px,8vw,96px) 8px;border-top:1px solid var(--line);margin-top:clamp(40px,7vw,80px);scroll-margin-top:60px}
.case-head{display:grid;gap:10px;max-width:70ch}
.case-head h2{font:800 clamp(2rem,5.4vw,3.5rem)/1.04 var(--sans);letter-spacing:-.02em;margin:0;text-wrap:balance}
.lede{font-size:1.1875rem;line-height:1.5;margin:6px 0 0;max-width:62ch}
.chips{list-style:none;margin:10px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.chips li{font:400 .75rem/1 var(--mono);letter-spacing:.04em;padding:8px 11px;border:1px solid var(--line);border-radius:999px;color:var(--muted)}
.stage{margin-top:28px;background:var(--s);border-radius:20px;min-height:clamp(220px,34vw,360px);display:flex;align-items:center;justify-content:center;gap:clamp(16px,4vw,48px);padding:clamp(24px,5vw,56px);flex-wrap:wrap}
.stage img{max-width:min(100%,560px);max-height:220px;width:auto;height:auto;object-fit:contain;flex:0 1 auto}
.stage img + img{max-width:min(100%,520px)}
.idea-row{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:clamp(24px,5vw,64px);margin-top:36px;align-items:start}
@media (max-width:820px){ .idea-row{grid-template-columns:minmax(0,1fr)} }
.idea p{margin:12px 0 0;max-width:60ch}
.idea p:first-of-type{margin-top:14px}
.label{margin:48px 0 14px;display:block}
.idea .label{margin:0}
.spec{margin:0;display:grid;gap:0;border-top:1px solid var(--line)}
.spec>div{display:grid;grid-template-columns:minmax(96px,150px) minmax(0,1fr);gap:16px;padding:12px 0;border-bottom:1px solid var(--line)}
.spec dt{font:400 .75rem/1.5 var(--mono);letter-spacing:.07em;text-transform:uppercase;color:var(--muted);padding-top:3px}
.spec dd{margin:0;font-size:.96875rem;line-height:1.5}
.idea-row .spec{margin-top:0}

/* camino */
.path{list-style:none;margin:0;padding:0;counter-reset:s;display:grid;gap:0;border-top:1px solid var(--line)}
.step{counter-increment:s;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,380px);gap:clamp(16px,4vw,48px);padding:24px 0;border-bottom:1px solid var(--line);align-items:center}
.step--text{grid-template-columns:minmax(0,1fr)}
.step-text{position:relative;padding-left:44px;min-width:0}
.step-text::before{content:counter(s);position:absolute;left:0;top:2px;font:400 .8125rem/1.6 var(--mono);color:var(--accent)}
.step h4{font:700 1.125rem/1.3 var(--sans);margin:0 0 6px;text-wrap:balance}
.step p{margin:0;max-width:58ch;color:var(--muted);font-size:1rem}
@media (max-width:760px){ .step{grid-template-columns:minmax(0,1fr)} }
.shot{display:block;width:100%;padding:0;border:1px solid var(--shot-line);border-radius:12px;overflow:hidden;background:var(--bg-2);cursor:zoom-in}
.shot img{width:100%;height:auto;max-height:440px;object-fit:contain;background:#F4F5F7}
.shot:hover{border-color:var(--accent)}

/* versiones */
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px}
.tile{margin:0;min-width:0}
.tile .surface{background:var(--t);border-radius:14px;aspect-ratio:4/3;display:flex;align-items:center;justify-content:center;gap:14px;padding:18px;border:1px solid rgba(127,140,160,.28);position:relative}
.tile .surface>img:not(.gif-img){max-width:100%;max-height:100%;object-fit:contain}
.tile--wide{grid-column:span 2}
.tile--wide .surface{aspect-ratio:8/3}
@media (max-width:520px){ .tile--wide{grid-column:span 2} .tile--wide .surface{aspect-ratio:2/1} .tiles{grid-template-columns:repeat(2,minmax(0,1fr))} }
.tile--multi .surface img{flex:none;max-width:none;max-height:none}
/* cuatro versiones en una fila: dos normales y dos anchas, con la misma altura (4/3 en 1 parte y 8/3 en 2 partes) */
@media (min-width:761px){ .tiles.tiles--fila{grid-template-columns:1fr 1fr 2fr 2fr} .tiles--fila .tile--wide{grid-column:auto} }
.tile--gif .gif-img{max-width:100%;max-height:100%;object-fit:contain}
.tile .play{position:absolute;right:10px;bottom:10px;font:400 .75rem/1 var(--mono);letter-spacing:.05em;background:var(--accent);color:var(--accent-ink);border:0;border-radius:999px;padding:9px 12px;cursor:pointer}
.tile figcaption,.use figcaption{font-size:.875rem;color:var(--muted);margin-top:8px;line-height:1.4}

/* usos */
.uses{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,320px),1fr));gap:16px;align-items:start}
.use{margin:0;min-width:0}
.use:only-child{grid-column:span 2}
@media (max-width:700px){ .use:only-child{grid-column:auto} }
.use .shot img{aspect-ratio:3/2;object-fit:cover;object-position:top center;max-height:none}
.use--portrait{max-width:300px}
.use--portrait .shot img{aspect-ratio:390/844;object-position:top}
.use--square .shot img{aspect-ratio:1/1;object-position:center}

/* ficha */
.ficha{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:clamp(20px,5vw,56px);align-items:start}
@media (max-width:820px){ .ficha{grid-template-columns:minmax(0,1fr)} }
.swatches{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.swatches li{display:flex;gap:12px;align-items:center}
.chip{width:44px;height:44px;border-radius:10px;flex:none;border:1px solid rgba(127,140,160,.35)}
.sw-text{display:flex;flex-direction:column;gap:1px;min-width:0}
.sw-text b{font-weight:700;font-size:.9375rem;line-height:1.3}
.sw-text code{font:400 .8125rem/1.3 var(--mono);color:var(--muted)}
.sw-text em{font-style:normal;font-size:.8125rem;color:var(--muted);line-height:1.3}

footer{margin-top:clamp(56px,9vw,112px);border-top:1px solid var(--line);padding-block:28px 56px;color:var(--muted);font-size:.875rem}
footer .wrap{display:flex;gap:12px 32px;flex-wrap:wrap;justify-content:space-between}

/* ampliar */
dialog.zoom{border:0;padding:0;background:transparent;max-width:min(96vw,1400px);max-height:94vh;width:auto;overflow:auto;border-radius:10px}
dialog.zoom::backdrop{background:rgba(5,9,16,.86)}
dialog.zoom img{display:block;max-width:min(96vw,1200px);height:auto;border-radius:10px;background:#fff;cursor:zoom-out}
@media (prefers-reduced-motion: reduce){ html{scroll-behavior:auto} }
/* paso ancho (animación) */
.step--wide{grid-template-columns:minmax(0,1fr)}
.step--wide .step-media{padding-left:44px;min-width:0}
@media (max-width:760px){ .step--wide .step-media{padding-left:0} }
/* del clavel al símbolo: capas alineadas en el mismo lienzo */
@property --sw{syntax:'<angle>';inherits:false;initial-value:0deg}
@property --rr{syntax:'<percentage>';inherits:false;initial-value:0%}
.morph{margin:6px 0 0;max-width:620px}
.m-stage{position:relative;aspect-ratio:1/1;border-radius:22px;overflow:hidden;background:radial-gradient(110% 95% at 50% 45%,#F4EECD 0%,#E9E2B6 55%,#DCD2A0 100%);box-shadow:0 30px 60px -30px rgba(0,0,0,.6),inset 0 0 0 1px rgba(0,0,0,.05)}
.m-stage img,.m-turn{position:absolute;inset:0;width:100%;height:100%}
.m-turn{transform-origin:var(--cx) var(--cy)}
.m-foto,.m-poster,.m-lineas{opacity:0}
.morph.is-play .m-turn{animation:m-turn 7.2s cubic-bezier(.3,0,.15,1) both}
.morph.is-play .m-foto{animation:m-foto 4.6s ease both}
.morph.is-play .m-poster{animation:m-poster 7.4s ease both}
.morph.is-play .m-lineas{opacity:1;-webkit-mask:conic-gradient(from 0deg at var(--cx) var(--cy),#000 var(--sw),transparent 0);mask:conic-gradient(from 0deg at var(--cx) var(--cy),#000 var(--sw),transparent 0);animation:m-sweep 2.3s cubic-bezier(.45,0,.2,1) 3.7s both}
.morph.is-play .m-color{-webkit-mask:radial-gradient(circle at var(--cx) var(--cy),#000 var(--rr),transparent calc(var(--rr) + 1.5%));mask:radial-gradient(circle at var(--cx) var(--cy),#000 var(--rr),transparent calc(var(--rr) + 1.5%));animation:m-bloom 1.7s cubic-bezier(.3,0,.2,1) 6.1s both}
.morph.is-play .m-texto{-webkit-mask:conic-gradient(from 238deg at var(--cx) var(--cy),#000 var(--sw),transparent 0);mask:conic-gradient(from 238deg at var(--cx) var(--cy),#000 var(--sw),transparent 0);animation:m-sweep-t 1.7s cubic-bezier(.4,0,.2,1) 7.8s both}
@keyframes m-turn{from{transform:rotate(-40deg) scale(1.05)}to{transform:rotate(0deg) scale(1)}}
@keyframes m-foto{0%{opacity:0}16%{opacity:1}62%{opacity:1}100%{opacity:0}}
@keyframes m-poster{0%,28%{opacity:0}46%{opacity:1}80%{opacity:1}100%{opacity:0}}
@keyframes m-sweep{from{--sw:0deg}to{--sw:360deg}}
@keyframes m-bloom{from{--rr:0%}to{--rr:72%}}
@keyframes m-sweep-t{from{--sw:0deg}to{--sw:250deg}}
.m-bar{display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap;margin-top:12px}
.m-steps{list-style:none;margin:0;padding:0;display:flex;gap:6px;flex-wrap:wrap}
.m-steps li{font:400 .75rem/1 var(--mono);letter-spacing:.06em;text-transform:uppercase;padding:8px 10px;border-radius:999px;border:1px solid var(--line);color:var(--muted);transition:background .3s,color .3s,border-color .3s}
.m-steps li.is-on{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.m-replay{font:600 .875rem/1 var(--sans);padding:10px 14px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--fg);cursor:pointer}
.m-replay:hover{border-color:var(--accent)}
@media (prefers-reduced-motion: reduce){ .morph.is-play *{animation:none!important} .morph.is-play .m-lineas{opacity:0} }

"""

JS = r"""

(function(){
  var RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.morph').forEach(function(m){
    var lis=m.querySelectorAll('.m-steps li'), T=[0,1800,3700,6100,7800], timers=[];
    function play(){
      timers.forEach(clearTimeout); timers=[]; m.classList.remove('is-play'); void m.offsetWidth; m.classList.add('is-play');
      lis.forEach(function(l){l.classList.remove('is-on')});
      T.forEach(function(t,i){ timers.push(setTimeout(function(){ lis.forEach(function(l,j){l.classList.toggle('is-on',j===i)}); }, t)); });
      timers.push(setTimeout(function(){ lis.forEach(function(l){l.classList.remove('is-on')}); }, 10400));
    }
    m.querySelector('.m-replay').addEventListener('click',play);
    // 6/11, Débora: «que arranque solo en loop». Se repite mientras está a la vista y se frena al salir; con movimiento reducido no arranca solo.
    var loop=null;
    function vuelta(){ play(); loop=setTimeout(vuelta, 12000); }
    if(!RM && 'IntersectionObserver' in window){
      new IntersectionObserver(function(es){ es.forEach(function(e){
        if(e.isIntersecting){ if(!loop) vuelta(); } else { clearTimeout(loop); loop=null; }
      }); },{threshold:.45}).observe(m);
    }
  });
})();
(function(){
  var dlg=document.getElementById('zoom'), big=dlg&&dlg.querySelector('img');
  document.addEventListener('click',function(e){
    var s=e.target.closest('[data-zoom]');
    if(s&&dlg&&dlg.showModal){ big.src=s.getAttribute('data-zoom'); big.alt=(s.querySelector('img')||{}).alt||''; dlg.showModal(); return; }
    var p=e.target.closest('.play');
    if(p){ var img=p.parentNode.querySelector('.gif-img'); var g=img.getAttribute('data-gif'); img.src=''; img.src=g+'?t='+Date.now(); p.hidden=true; setTimeout(function(){img.src=img.getAttribute('data-still'); p.hidden=false;},2200); }
  });
  if(dlg) dlg.addEventListener('click',function(){dlg.close();});
})();
"""

HTML = f'''<title>Marcas de Débora Malqui</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Cuatro marcas: logo, versiones, usos, la idea y el camino hasta llegar.">
<style>{FONT_CSS}{CSS}</style>

<header class="bar"><div class="wrap">
  <a class="brand" href="#top" aria-label="DiDí, inicio de la página"><img class="only-dark" src="{use_asset("logos/didi-logo.svg")}" alt="DiDí"><img class="only-light" src="{use_asset("logos/didi-logo-una-tinta-oscura.svg")}" alt="DiDí"></a>
  <nav aria-label="Casos">{nav_html}</nav>
</div></header>

<main id="top">
<div class="wrap">
  <section class="hero">
    <p class="eyebrow">Débora Malqui · Diseño de marca</p>
    <h1>Cuatro marcas, de la primera idea al uso real.</h1>
    <p class="intro">Cada caso muestra el logo final con sus versiones y usos, la idea que lo sostiene y el camino que llevó hasta ahí, con las pruebas de cada paso. Están ordenados del más reciente al más antiguo.</p>
    <ol class="index" aria-label="Índice de casos" style="list-style:none">{index_html}</ol>
  </section>
  {"".join(cases)}
</div>
</main>

<footer><div class="wrap">
  <span>Marcas de Débora Malqui. Los años son los del trabajo.</span>
  <span>Escrita con DiDi Sans y DiDi Mono, las tipografías del caso DiDí.</span>
</div></footer>

<dialog class="zoom" id="zoom" aria-label="Imagen ampliada"><img alt=""></dialog>
<script>{JS}</script>
'''
def to_artifact(h):
    """Vista previa privada: el mismo encabezado que el sitio; el menú lleva al sitio publicado y las pestañas a las vistas previas."""
    import re as _re, sys as _sys
    _sys.path.insert(0, B); from comun import header_html, HEADER_CSS, LIVE, ARTIFACT_GUIDES
    h = _re.sub(r'<header class="bar">.*?</header>', lambda m: header_html(False, "logos", main_base=LIVE + "es/", logos_href="#top", guides_href=ARTIFACT_GUIDES or "guidelines.html"), h, count=1, flags=_re.S)
    return h.replace("</style>", HEADER_CSS + "</style>", 1)
open(os.path.join(B, "index.html"), "w").write(to_artifact(HTML))
files = sorted(USED)
json.dump(files, open(os.path.join(B, "published-files.json"), "w"), indent=1)
print("ok", len(HTML) // 1024, "KB de HTML,", len(files), "archivos")
missing = [f for f in files if not os.path.exists(os.path.join(B, f))]
print("faltan:", missing)

# ---------------------------------------------------------------- versión para el sitio (se copia tal cual a sitio/marcas/)
import sys
def to_site(h):
    i = h.index('<header class="bar">'); head, body = h[:i], h[i:]
    head = head.replace("<title>Marcas de Débora Malqui</title>", "<title>Marcas · Débora Malqui</title>").replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
    import re as _re
    sys.path.insert(0, B); from comun import header_html, HEADER_CSS, meta_site
    body = _re.sub(r'<header class="bar">.*?</header>', lambda m: header_html(True, "logos"), body, count=1, flags=_re.S)
    head = head.replace("</style>", HEADER_CSS + "</style>", 1)
    head = _re.sub(r'@media \(prefers-color-scheme: light\)\{.*?\} \}', '', head, flags=_re.S)   # el sitio es siempre oscuro
    head = head.replace("<title>", '<meta name="color-scheme" content="dark"><title>', 1)
    body = body.replace("<span>Marcas de Débora Malqui. Los años son los del trabajo.</span>", '<span>Marcas de Débora Malqui. Los años son los del trabajo. <a href="../es/sobre-mi.html">Volver a Sobre mí</a></span>')
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0F1B2D">'
            + meta_site("index.html", "Marcas · Débora Malqui", "Cuatro marcas: logo, versiones, usos, la idea y el camino hasta llegar.") +
            '<link rel="icon" href="../assets/favicon.ico" sizes="any"><link rel="icon" type="image/svg+xml" href="../assets/favicon-32.svg"><link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">'
            + head + "</head><body>" + body + "</body></html>")

import sys, shutil
if "--site" in sys.argv:
    dest = os.path.join(os.path.dirname(B), "sitio-src", "extra", "marcas")
    if os.path.exists(dest): shutil.rmtree(dest)
    os.makedirs(dest)
    open(os.path.join(dest, "index.html"), "w").write(to_site(HTML))
    for f in files:
        t = os.path.join(dest, f); os.makedirs(os.path.dirname(t), exist_ok=True); shutil.copyfile(os.path.join(B, f), t)
    print("sitio-src/extra/marcas:", len(files) + 1, "archivos")
