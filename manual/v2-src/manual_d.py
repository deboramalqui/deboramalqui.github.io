# Parte D · Aplicación (secciones 20 a 23). Se ejecuta dentro de build_manual.py.
out.append(part('Parte D · Aplicación'))
out.append(sec('home','Portada','La portada presenta a Débora con una frase, muestra su propio producto funcionando y después los casos. Todo lo que se ve sale del sistema; la laptop es la única ilustración.',f'''
<div class="m-pair"><figure style="margin:0"><img class="m-shot" src="img/v2-home-escritorio.jpg" alt="Portada en computadora: nombre, presentación, frase corta con «Probalo» y la laptop abierta con la Campaign Suite, con tres cifras a los costados" loading="lazy"><figcaption class="m-lbl" style="margin-top:8px">Computadora, 1360 px</figcaption></figure><figure style="margin:0"><img class="m-shot" src="img/v2-home-celular.jpg" alt="Portada en celular: nombre, presentación y la laptop abierta debajo, con las cifras abajo" loading="lazy"><figcaption class="m-lbl" style="margin-top:8px">Celular, 390 px</figcaption></figure></div>
<div class="m-pair"><figure style="margin:0"><img class="m-shot" src="img/v2-home-casos-escritorio.jpg" alt="Sección Casos en computadora: título grande con la cantidad al lado y las dos tarjetas destacadas, Campaign Suite y Medido" loading="lazy"><figcaption class="m-lbl" style="margin-top:8px">Computadora, 1360 px</figcaption></figure><figure style="margin:0"><img class="m-shot" src="img/v2-home-casos-celular.jpg" alt="Sección Casos en celular: título grande y tarjetas en dos columnas" loading="lazy"><figcaption class="m-lbl" style="margin-top:8px">Celular, 390 px</figcaption></figure></div>
<p class="m-lbl">Capturas del sitio publicado, en español, a 2×.</p>
{table(['Bloque','Qué lleva','Regla'],[
 ['Barra de arriba','Logo, Casos, Sobre mí, Contacto, idiomas (EN, ES, עב) y «Escribime» tonal','Fija arriba. Debajo de 760 px la navegación pasa al menú y «Escribime» al botón flotante.'],
 ['Presentación','Nombre (h1), la frase fija de la portada y una frase corta en negrita con «Probalo», que abre la demo en otra ventana','Sin otra frase ni título inventado. En hebreo, el nombre en letras hebreas va chico debajo.'],
 ['La laptop','La Campaign Suite en su pestaña «Hoy», con tres cifras: +69 % visitas al sitio en 28 días, 505 postulaciones en 28 días, 410 → 82 leads con el error apagado','Entra entera en el primer pantallazo. Sin JavaScript se ve abierta y quieta. La imagen se precarga: es lo primero que mide la velocidad.'],
 ['Casos','Título grande «Casos» con la cantidad. Campaign Suite y Medido en grande; los otros ocho (Kol Accesorios entre ellos) en filas completas','Celular y tableta 2 columnas, computadora 4. Si cambia la cantidad, ninguna fila puede quedar incompleta. El orden de «Siguiente caso» no cambia.'],
 ['Tarjeta de caso','Portada, título, bajada, y en mono el año y el tipo con su punto de color','En celular la bajada no se muestra. Sin portada, la tarjeta dibuja barras.'],
 ['Reconocimientos y colaboraciones','Tres baldosas: becas, exposiciones con su trabajo, colaboraciones. Cada una abre su hoja','Premios: no se muestran hasta que haya pruebas y nombres. Una lista vacía deja la baldosa sin acción.'],
 ['Trabajos académicos y pasantías','Lista con número, título, año e imagen','En computadora la imagen aparece al pasar el mouse; en celular va chica al inicio de la fila.'],
 ['Pie','© 2026 Débora Malqui, mail, WhatsApp (+972 52-743-0122) y LinkedIn, y el logo apilado','Mismo pie en todas las páginas. El teléfono va solo acá, como enlace de WhatsApp, y en los datos estructurados (pedido de Débora, 2026).']])}
<h3>Las hojas de reconocimientos</h3>
<div class="m-pair"><figure style="margin:0"><img class="m-shot" src="img/v2-home-hoja-escritorio.jpg" alt="Hoja de becas abierta en computadora, como tarjeta centrada sobre un velo" loading="lazy"><figcaption class="m-lbl" style="margin-top:8px">Computadora, 1360 px</figcaption></figure><figure style="margin:0"><img class="m-shot" src="img/v2-home-hoja-celular.jpg" alt="Hoja de becas abierta en celular, subiendo desde abajo, con una barra de color y el año en color en cada beca" loading="lazy"><figcaption class="m-lbl" style="margin-top:8px">Celular, 390 px</figcaption></figure></div>
<ul><li>Celular: hoja que sube desde abajo, con una manija para arrastrarla. Computadora: tarjeta centrada.</li><li>Se cierra con «Listo» (rosa, la acción), con Esc, tocando el fondo o arrastrando hacia abajo más de 80 px.</li><li>Al abrir, el foco va al título de la hoja, no al botón «Listo».</li><li>Colaboraciones: arriba, la franja de países; después «Principales clientes», con subrayado de color y enlace a su web; después los años.</li></ul>
{note('<b>Ya no se usa en el sitio.</b> La portada de la v1 tenía la fecha de disponibilidad, cuatro cifras del caso Nido, «Ver los casos» relleno, «Descargar CV», un índice con pestañas por categoría (en inglés), un caso destacado con «Lo que la medición encontró» y una tarjeta de «Sin mejora medible todavía».','m-open')}'''))

out.append(sec('caso','Página de caso','La estructura de todos los casos: migas, título, presentación, datos del caso, el trabajo contado por secciones con sus piezas, y una sola acción al final. Toda la página toma el color del tipo.',f'''
<div class="m-pair"><figure style="margin:0"><img class="m-shot" src="img/v2-kol-escritorio.jpg" alt="Caso Kol Accesorios en computadora: índice fijo a la izquierda, migas, título con la línea rosa debajo, presentación y datos del caso" loading="lazy"><figcaption class="m-lbl" style="margin-top:8px">Computadora, 1360 px</figcaption></figure><figure style="margin:0"><img class="m-shot" src="img/v2-kol-celular.jpg" alt="Caso Kol Accesorios en celular: migas, título con la línea rosa, presentación y datos del caso, con el botón flotante «Escribime»" loading="lazy"><figcaption class="m-lbl" style="margin-top:8px">Celular, 390 px</figcaption></figure></div>
{table(['Bloque','Obligatorio','Regla'],[
 ['Migas y título','Sí','Un solo h1: «Nombre: lo que se hizo». Debajo, una línea de 72 × 4 px del color del tipo.'],
 ['Presentación','Sí','Un párrafo más grande (19 px) que dice qué es el caso.'],
 ['Datos del caso','Sí','Etiquetas en mono del color del tipo (rol, año, herramientas) y fichas de dato. Rol exacto, nunca inflado.'],
 ['Barra de lectura','Sí','Una línea de 3 px del color del tipo, al pie de la barra de arriba, que avanza a medida que se lee.'],
 ['Índice','Desde 1100 px','A la izquierda, fijo al bajar; marca la sección que se está leyendo con una barra del color del tipo.'],
 ['Secciones','Sí','Cada subtítulo con un punto del color del tipo. Cifras en baldosas, tablas con encabezado del color del tipo, piezas reales del trabajo.'],
 ['Qué no se publica','No en pantalla','Vive en la ficha interna, no en la página.'],
 ['Cierre','Sí','«Escribime» relleno (la variante D, la única acción rellena de la página) y el siguiente caso como enlace.']])}
<h3>Piezas para mostrar el trabajo</h3>
{table(['Pieza','Qué hace','Dónde'],[
 ['Captura ampliable','Se toca para verla grande, con acercar, alejar y desplazar.','Casi todos los casos'],
 ['Galería','Pasa de una imagen a otra deslizando, con botones o con las flechas.','Santo Tomé, Waycare, Medido'],
 ['Monitor','Una web dentro de una pantalla que se desplaza, con pestañas para cambiar de página.','Kol Accesorios'],
 ['Mosaico','Todas las piezas juntas, enteras, con la misma calle entre ellas.','Kol Accesorios, Communiqué'],
 ['Cuaderno','Un manual de marca que se abre y pasa de hoja en 3D.','Sobre mí y la sección de marcas'],
 ['Prototipo que se puede tocar','Las pantallas finales con zonas activas, flechas y teclado.','Bplay, Clash'],
 ['Componentes incrustados','La sección de componentes de un caso, dentro de un marco que toma su alto real.','Bplay, MAC, Clash'],
 ['Videos','Video propio con controles, o miniatura que lleva a YouTube.','Communiqué (reels), Medido, trabajos académicos'],
 ['Infografías en HTML','Las láminas rehechas como página: el texto se traduce y el dibujo es solo línea.','Clash']])}
{note('<b>Ya no se usa en el sitio.</b> La v1 pedía en cada caso «El problema», «Qué se midió» con tabla de fuente y etiqueta de confianza, y una tarjeta de «Lo que no salió» con el mismo peso que los resultados. Hoy los casos cuentan el trabajo y sus resultados, sin notas de método (la web es una vitrina).','m-open')}'''))

exec(compile((pathlib.Path(__file__).resolve().parent/'manual_gestos.py').read_text(),'manual_gestos','exec'),globals())

# ---------- imagen ----------
out.append(sec('imagen','Imagen y capturas','La prueba de un caso es el trabajo real: capturas, piezas y pantallas finales. Se muestran sin marco de dispositivo, salvo la laptop de la portada y el monitor, que son piezas del sitio.',f'''
{table(['Regla','Valor'],[
 ['Fuente','Captura del sitio o de la pieza real; las pantallas y los componentes de los casos de diseño, tal como se entregaron.'],
 ['Formato','WebP. Toda imagen de más de 1000 px tiene copias de 480 y 720 px, y el navegador elige la que corresponde al ancho.'],
 ['Carga','La imagen principal de la portada se precarga. Las que están debajo del primer pantallazo llegan cuando se acercan a la pantalla.'],
 ['Caja','Nunca más alta que la imagen: sin franjas oscuras. Borde de 1 px (<code>--d-outline-var</code>).'],
 ['Pie de foto','Una línea en mono: qué muestra.'],
 ['Texto alternativo','Qué muestra y qué importa de eso. Nunca «captura de pantalla». Las portadas de las tarjetas son decorativas: alternativo vacío.'],
 ['Clientes','Con su nombre real. Los importes en pesos de las campañas que funcionaron se muestran como figuran en las plataformas.'],
 ['Datos de personas','Mail, fecha de nacimiento y teléfonos de terceros, tapados.'],
 ['Personas','Sin fotos de personas sin permiso. Sin fotos grupales de los trabajos del MA.'],
 ['Imagen para compartir','1200 × 630, una por caso y una general con la frase de la portada.'],
 ['Celular y computadora','Al cambiar una imagen o una portada, se revisan las dos versiones (y sus copias de 480 y 720 px).']])}
{note('<b>Ya no se usa en el sitio.</b> La v1 pedía anonimizar el cliente (logo, nombre y dominio reemplazados por script, montos tapados) y capturas en JPG de hasta 200 KB a 16:10. Hoy Kol Accesorios va con su nombre y las imágenes van en WebP con copias por ancho.','m-open')}'''))

# ---------- microcopy ----------
out.append(sec('microcopy','Voz y textos de la interfaz','Cómo suenan los textos de la interfaz en los tres idiomas: español rioplatense con voseo, inglés estadounidense llano y hebreo moderno, en primera persona. Las traducciones viven en i18n/ y un chequeo avisa de lo que quedó sin traducir.',f'''
{table(['Elemento','Español','Inglés','עברית'],[
 ['Acción principal','Escribime','Get in touch','<span lang="he" dir="rtl">כתבו לי</span>'],
 ['Navegación','Casos · Sobre mí · Contacto','Cases · About me · Contact','<span lang="he" dir="rtl">מקרי בוחן · עליי · יצירת קשר</span>'],
 ['Saltar','Saltar al contenido','Skip to content','<span lang="he" dir="rtl">דלגו לתוכן</span>'],
 ['Siguiente','Siguiente caso: Sistemas de trading','Next case: Trading systems','<span lang="he" dir="rtl">המקרה הבא: מערכות טריידינג</span>'],
 ['Cerrar una hoja','Listo','Done','<span lang="he" dir="rtl">סיום</span>'],
 ['Campos','Tu nombre · Tu mail · Mensaje','Your name · Your email · Message','<span lang="he" dir="rtl">השם שלכם · המייל שלכם · הודעה</span>'],
 ['Enviar','Enviar mensaje · Enviando…','Send message · Sending…','<span lang="he" dir="rtl">שליחת הודעה · שולח…</span>'],
 ['Envío correcto','Me llegó tu mensaje. Te voy a responder en 24 horas hábiles.','Got your message. I will reply within 24 business hours.','<span lang="he" dir="rtl">ההודעה שלכם התקבלה אצלי. אחזור אליכם בתוך 24 שעות עסקים.</span>'],
 ['Privacidad','Tus datos se usan solo para responderte. El envío pasa por FormSubmit y no se guarda en ningún otro lado.','Your details are used only to reply to you. The message goes through FormSubmit and isn’t stored anywhere else.','<span lang="he" dir="rtl">הפרטים שלך משמשים רק כדי לענות לך. ההודעה עוברת דרך FormSubmit ולא נשמרת בשום מקום אחר.</span>'],
 ['Reconocimientos','becas · exposiciones con mi trabajo · colaboraciones','scholarships · exhibitions featuring my work · collaborations','<span lang="he" dir="rtl">מלגות · תערוכות שהציגו את העבודות שלי · שיתופי פעולה</span>'],
 ['Fecha','Solo el año: 2026','2026','2026'],
 ['Miles','1.520','1,520','1,520']])}
<ul><li>Sin signos de exclamación. Sin «¡Hola!». El tono es el de una nota amable y segura.</li><li>El error explica qué pasó y qué hacer; nunca culpa a la persona.</li><li>Los botones son verbos; las etiquetas, sustantivos.</li><li>Hay palabras que no van en el sitio: la lista está en la regla 3 de <code>MANTENIMIENTO.md</code>. Se dice «componentes», «sistema de diseño» y «pantallas finales». Única excepción: la nota de Figma en Bplay y MAC.</li></ul>
{note('<b>Para revisar en el hebreo.</b> Los textos de la interfaz le hablan a la persona en plural («השם שלכם»), pero el aviso de privacidad usa el singular («הפרטים שלך»). Conviene que lo mire una persona nativa.','m-open')}'''))

# ---------- qué no hacer ----------
out.append(sec('no-hacer','Qué no hacer y control antes de publicar','Los errores más probables, y la lista de chequeo para cada página.',f'''
<div class="m-two"><div class="m-dont"><b>No</b><ul style="margin:0;padding-left:18px"><li>Dos botones rellenos en una vista, o el rosa en algo que no sea acción o el tipo Campañas.</li><li>El color del tipo en un enlace, un botón, un fondo o un texto largo.</li><li>Poner texto largo sobre un color pleno.</li><li>Dar radio a un dato, o poner una barra a una acción.</li><li>Animar el logo, o cambiar la opacidad del texto al moverse.</li><li>Movimiento que no se apague con «reducir movimiento».</li><li>Fondo negro #000 o blanco #fff planos; ningún tema claro.</li><li>Una cifra que no esté en la hoja de verdad o en una ficha.</li><li>Notas de método, disculpas o etiquetas de confianza en la página.</li><li>Fechas con día o mes.</li><li>Inventar una frase de portada, un título o una fecha de disponibilidad.</li><li>Una hoja de estilos externa o una imagen sin carga diferida debajo de la portada: la velocidad baja de 100.</li></ul></div><div class="m-do"><b>Antes de publicar una página</b><ol style="margin:0;padding-left:18px"><li>Un solo botón relleno rosa.</li><li>Cada cifra está en la hoja de verdad o en una ficha.</li><li>Ningún color es el único portador de significado.</li><li>El foco se ve en cada elemento, con teclado.</li><li>Contraste revisado al pasar el mouse, con foco y deshabilitado.</li><li>Cada imagen tiene texto alternativo útil.</li><li>Sin nombres de compañeros ni datos de terceros.</li><li>Revisada en celular y en computadora, también las imágenes de 480 y 720 px.</li><li>Ninguna fila de tarjetas incompleta.</li><li>Nada se mueve con <code>prefers-reduced-motion</code>.</li><li>Verificación en verde y Lighthouse en 100.</li></ol></div></div>'''))
