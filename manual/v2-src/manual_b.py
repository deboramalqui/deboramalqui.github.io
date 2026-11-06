# Parte B · Sistema (secciones 6 a 11). Se ejecuta dentro de build_manual.py (usa out, sec, part, table, note, card, two, fig, ic, demo, demos, ...).
out.append(part('Parte B · Sistema'))

# ---------- 5 · forma ----------
RAD=[('none','0','Datos, barras, indicadores','--d-r-none'),('xs','4','Ayuda emergente, menú','--d-r-xs'),('sm','8','Imagen chica de los trabajos académicos','--d-r-sm'),('md','12','D chica: aviso. Tarjeta de caso (las cuatro esquinas)','--d-r-md'),('lg','16','D media: tarjeta de componente, lista destacada','--d-r-lg'),('xl','28','D grande: diálogo, botón flotante, hoja de reconocimientos (arriba)','--d-r-xl'),('full','9999','Píldora: botón, etiqueta verificado, interruptor, fichas de empresas, cifras de la portada','--d-r-full')]
radbox=''.join(f'<div style="display:grid;gap:8px;justify-items:start"><div style="width:84px;height:56px;background:#2A4665;border-radius:{("9999px" if r=="9999" else r+"px")}"></div><span class="m-lbl">{n} · {r}</span></div>' for n,r,_,_ in RAD)
def dshape(rad,w=110,h=56,c='#E890CC'): return f'<div style="display:grid;gap:8px;justify-items:start"><div style="width:{w}px;height:{h}px;background:{c};border-radius:{rad}"></div></div>'
out.append(sec('forma','Forma','Tres formas, todas sacadas del logo: la D abierta, la barra y la píldora. Cada forma pertenece a una función; el radio es la señal que el color refuerza.',f'''
<h3>Las tres formas</h3>
<div class="m-panel"><div class="didi m-demo" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:32px;align-items:end">
<div style="display:grid;gap:10px">{dshape("0 28px 28px 0",140,64)}<span class="m-lbl">D abierta · lado recto a la izquierda · acción y contenedores con jerarquía</span></div>
<div style="display:grid;gap:10px">{dshape("0",140,64,"#70B4F4")}<span class="m-lbl">Barra · radio 0 · navegación y dato</span></div>
<div style="display:grid;gap:10px">{dshape("9999px",140,40,"#ACEC84")}<span class="m-lbl">Píldora · radio completo · verificado</span></div></div></div>
{table(['Forma','Color','Componentes','Token'],[
 ['D abierta','Rosa (acción)','Botón con variante D («Escribime», cierre del caso), botón flotante, lista destacada, diálogo','<code>--d-r-d-sm / md / lg / full</code>'],
 ['D abierta, lado derecho abierto','Amarillo (atención)','Tarjeta de atención, marca de atención, aviso','<code>--d-r-d-*</code>'],
 ['Barra (radio 0)','Celeste (navegación) y azul (dato)','Indicadores, índice del caso, campos con línea inferior, baldosas de cifras, tablas, código','<code>--d-r-none</code>'],
 ['Píldora','Verde (verificado) y botones','Botón estándar, idioma elegido, interruptor, fichas de empresas, cifras flotantes de la portada','<code>--d-r-full</code>'],
 ['Esquinas parejas de 12 px','Neutra; el borde toma el color del tipo','Tarjetas de casos de la portada','<code>--d-r-md</code>']])}
<h3>Escala de radios</h3>
<div class="m-panel"><div class="didi m-demo d-row" style="gap:22px">{radbox}</div></div>
{table(['Token','Valor','Dónde'],[[f'<code>{t}</code>',f'{r} px',u] for n,r,u,t in RAD])}
<h3>Reglas</h3>
<ul><li>El <strong>lado recto de la D</strong> va siempre del lado de inicio de lectura (izquierda en español e inglés), como en el logo.</li><li>Nada mezcla dos formas: una baldosa de cifra nunca lleva una esquina redonda.</li><li>El radio de 4 px solo va en la ayuda emergente y el menú, que son superficies neutras.</li><li>Los puntos (de las tarjetas, de los subtítulos, de las galerías) son círculos: marcan el tipo o la posición, no una función.</li></ul>
{note('<b>Ya no se usa en el sitio.</b> La v1 decía que las tarjetas eran D abiertas (lado recto a la izquierda), que el radio de 12 px solo existía dentro de las D chicas y que una vista tenía como máximo tres formas. Las tarjetas de casos tienen hoy las cuatro esquinas de 12 px, y la portada junta tarjetas, píldoras, puntos y barras.','m-open')}
{note('<b>Hebreo (derecha a izquierda).</b> La web en hebreo se espeja con un bloque <code>[dir="rtl"]</code> al final de didi-ui.css: barras laterales, flechas, tablas, menús y anillos pasan de lado. Las formas con la D (radios) todavía no se espejan: la D de los botones y de las etiquetas conserva su lado recto a la izquierda. Pendiente: reemplazar los radios físicos por propiedades lógicas (<code>border-start-start-radius</code> y similares) si se quiere el espejo completo. El botón flotante pasa a la izquierda; las galerías y la captura ampliada siguen de izquierda a derecha, porque son imágenes; los títulos grandes entran desde la derecha.','m-open')}'''))

# ---------- 6 · espaciado ----------
SP=[('1','4'),('2','8'),('3','12'),('4','16'),('5','24'),('6','32'),('7','48'),('8','64'),('9','96')]
spbars=''.join(f'<tr><td class="n">--d-{k}</td><td class="n">{v} px</td><td><div style="height:12px;width:{v}px;background:#70B4F4"></div></td></tr>' for k,v in SP)
out.append(sec('espaciado','Espaciado y grilla','Base de 4 px, paso de 8. Un contenedor de 1160 px como máximo, y cortes de ancho según lo que cambia en cada pantalla.',f'''
<table class="m-t"><tr><th>Variable</th><th>Valor</th><th>Barra</th></tr>{spbars}</table>
<h3>Cortes de ancho del sitio</h3>
{table(['Ancho','Qué cambia'],[['Hasta 600 px (celular)','Casos en dos columnas compactas (portada, título y año; la bajada se ve al abrir el caso). Trabajos académicos con la imagen primero. Reconocimientos uno debajo del otro desde 560 px.'],['Hasta 759 px','La navegación se guarda en el menú; «Escribime» sale de la barra y queda el botón flotante.'],['Desde 760 px','Navegación completa en la barra.'],['Hasta 899 px (celular y tableta)','Botón flotante «Escribime» abajo a la derecha. Casos en dos columnas.'],['Desde 900 px (computadora)','Casos destacados de a dos y los demás de a cuatro. La laptop de la portada se mide para entrar entera en el primer pantallazo. Con mouse, la laptop lo sigue y la imagen de cada trabajo académico aparece al pasar.'],['Desde 1100 px','Página de caso con índice fijo a la izquierda (200 px) y texto de hasta 780 px.'],['Desde 1200 px','Las cifras de la portada salen a los costados de la laptop.'],['Más de 1160 px de contenido','El contenedor se centra; no se estira.']])}
{note('<b>Ya no se usa en el sitio.</b> La v1 seguía cinco clases de ventana estándar (de 0 a 599, de 600 a 839, de 840 a 1199, de 1200 a 1599 y de 1600 en adelante) con grilla de 4, 8 y 12 columnas. El sitio usa los cortes de arriba, elegidos por lo que cambia en cada pantalla.','m-open')}
<h3>Ritmo vertical</h3>
<ul><li>Entre secciones de página: de 40 a 80 px según el ancho, con una línea de 1 px entre una y otra.</li><li>Entre un título y su contenido: 16 px. Entre elementos de un grupo: 8 o 12 px. Entre grupos: 24 px.</li><li>Relleno interno: tarjetas 24 px, diálogo 24 px, campos 12 × 16 px.</li></ul>
<h3>Objetivos táctiles</h3>
<p>Todo lo que se toca mide <strong>48 × 48 px</strong> como mínimo, aunque lo visible sea más chico: el botón de ícono dibuja 40 px más 4 px de margen por lado; la casilla dibuja 18 px más 15 de margen. En pantallas táctiles (<code>pointer: coarse</code>) botones, fichas y campos suben a 48 px de alto. El índice del caso usa filas de 44 px: es el mínimo que mide la verificación. Entre objetivos, 8 px como mínimo.</p>'''))

# ---------- 7 · superficies y elevación ----------
out.append(sec('superficies','Superficies y elevación','En un tema oscuro la jerarquía la da el tono, no la sombra. Cada nivel de contenedor es un paso más claro.',f'''
{surface_swatches()}
{table(['Nivel','Qué va encima'],[['<code>--d-surface</code>','Fondo de la página, barra superior.'],['<code>--d-dim</code>','Fondo del documento y pie: más profundo que la página.'],['<code>--d-lowest</code>','Bloques de código y pozos.'],['<code>--d-low</code>','Tarjeta de caso, tarjeta rellena, baldosas de cifras, campos en reposo.'],['<code>--d-container</code>','Tarjeta elevada, campo con foco, ítem de riel activo.'],['<code>--d-high</code>','Diálogo, hoja de reconocimientos.'],['<code>--d-highest</code>','Pista del interruptor y de la barra de progreso.']])}
<h3>Sombra</h3>
<p>Tres sombras suaves, solo donde una superficie flota sobre otra: tarjeta elevada y cifras de la portada (e2); botón flotante, diálogo y hoja (e3). Nunca sombra en un elemento que está pegado al fondo.</p>
<p><strong>Sombra de color.</strong> Al pasar el mouse, una tarjeta de caso sube 3 px y proyecta una sombra larga del color de su tipo (al 70 %). La laptop de la portada tiene su propia luz y su sombra sobre la mesa: es una ilustración, no una superficie de la interfaz.</p>
<div class="m-panel"><div class="didi m-demo d-row" style="gap:28px"><div class="d-card d-card--outlined" style="width:180px"><h3 style="font-size:1rem;margin:0">Sin elevación</h3></div><div class="d-card" style="width:180px"><h3 style="font-size:1rem;margin:0">Rellena</h3></div><div class="d-card d-card--elevated" style="width:180px"><h3 style="font-size:1rem;margin:0">Elevada (e2)</h3></div><div class="d-dialog" style="width:180px;padding:16px"><h3 style="font-size:1rem;margin:0">Diálogo (e3)</h3></div></div></div>
<ul><li>Máximo tres niveles de superficie visibles en una misma vista.</li><li>El diálogo se apoya en un velo oscuro (<code>.d-scrim</code>) y bloquea el foco dentro de sí.</li></ul>'''))

# ---------- 8 · estados ----------
out.append(sec('estados','Estados','Los estados son capas sobre el color del componente, no colores nuevos.',f'''
{table(['Estado','Capa','Cómo se ve'],[['Al pasar el mouse','8 %','Capa del color del texto sobre el componente. En las tarjetas de casos: sube 3 px, el borde y la sombra toman el color del tipo y la imagen crece al 103 %.'],['Foco','12 % + anillo','Anillo celeste de 2 px, separado 2 px de la superficie, más la capa. El foco siempre se ve.'],['Presionado','12 %','Misma capa, un paso más.'],['Arrastrado','16 %','Solo en controles que se arrastran.'],['Deshabilitado','texto 38 %, contenedor 12 %','Sin capa y sin interacción. No se usa para ocultar información importante.'],['Seleccionado','tonal celeste + barra de 3 px','Dónde estás o qué está activo (sección 4).'],['Error','amarillo + ícono + texto','Nunca solo color. El mensaje dice qué pasó y qué hacer.'],['Cargando','indicador de carga o de progreso, amarillo','Menos de 200 ms: nada. De 200 ms a 5 s: indicador de carga. Más de 5 s: indicador de progreso (sección de retroalimentación).']])}
<p class="m-lbl">Valores: al pasar el mouse 0,08, foco 0,12, presionado 0,12, arrastre 0,16 (variables <code>--d-s-*</code>).</p>
<h3>Los cinco estados, en vivo</h3>
{demos(states_row('button','d-btn',f'Ver el caso {ic("arrow",18)}'),states_row('button','d-btn d-btn--tonal','Descargar CV'),states_row('button','d-btn d-btn--outlined','Ver todos'),states_row('button','d-btn d-btn--text','Más'))}
<h3>Estados vacío, error y cargando</h3>
<div class="m-panel"><div class="didi m-demo d-row" style="align-items:flex-start;gap:28px">
<div class="d-card d-card--outlined" style="width:260px"><h3>Todavía no hay casos acá</h3><p>Esta categoría se llena cuando haya un caso publicado.</p><button class="d-btn d-btn--tonal d-st">Ver todos los casos</button></div>
<div class="d-field is-error" style="width:260px"><label>Tu mail</label><input value="nombre@empresa" aria-invalid="true"><span class="d-help">{ic("warn",16)} Falta el dominio. Probá con nombre@empresa.com</span></div>
<div style="display:grid;gap:18px;width:260px"><div class="d-lin" style="--p:62" role="progressbar" aria-label="Cargando el caso" aria-valuemin="0" aria-valuemax="100" aria-valuenow="62"><div class="d-lin__track"></div><div class="d-lin__fill"></div><i class="d-lin__stop"></i></div><div class="d-lin d-lin--ind" role="progressbar" aria-label="Cargando"><div class="d-lin__track"></div><div class="d-lin__fill"></div></div><span class="m-lbl">Determinado e indeterminado. Amarillo = en curso.</span></div></div></div>'''))

# ---------- 9 · movimiento ----------
DUR=[('short1','50 ms','Casi instantáneo: foco de ícono'),('short2','100 ms','Capas de estado (hover, presionado)'),('short3','150 ms','Interruptor, chip, cambio de color'),('short4','200 ms','Ítem de menú, tooltip'),('medium1','250 ms','Despliegue de menú'),('medium2','300 ms','Diálogo, hoja inferior: entra'),('medium3','350 ms','—'),('medium4','400 ms','Máximo de este sistema')]
EAS=[('standard','cubic-bezier(.2, 0, 0, 1)','Todo lo que cambia de estado en pantalla.'),('emphasized-decelerate','cubic-bezier(.05, .7, .1, 1)','Lo que entra: diálogo, hoja, menú.'),('emphasized-accelerate','cubic-bezier(.3, 0, .8, .15)','Lo que sale.'),('standard-accelerate','cubic-bezier(.3, 0, 1, 1)','Salida corta.'),('standard-decelerate','cubic-bezier(0, 0, 0, 1)','Entrada corta.')]
mv=''.join(f'<div style="display:grid;gap:6px"><div class="m-move" style="--e:{e}"><i></i></div><span class="m-lbl">{n}</span></div>' for n,e,_ in EAS)
out.append(sec('movimiento','Movimiento','Dos niveles. En los componentes, el movimiento explica un cambio de estado y dura 400 ms o menos. En la vitrina (la portada, los casos, el paso de una página a otra) el movimiento presenta el trabajo y puede durar más. En los dos, el logo queda quieto y todo se apaga con «reducir movimiento».',f'''
<style>.m-move{{width:260px;height:14px;background:#13213A;position:relative}}.m-move i{{position:absolute;left:0;top:0;width:14px;height:14px;background:#80ECEC;transition:transform 700ms var(--e)}}.m-move:hover i{{transform:translateX(246px)}}</style>
<h3>Componentes</h3>
<div class="m-panel"><div class="didi m-demo d-row" style="gap:22px;align-items:flex-start">{mv}<span class="m-lbl">Pasá el mouse sobre cada pista: mismo recorrido, misma duración (700 ms para que se vea la diferencia), distintas curvas.</span></div></div>
{table(['Duración','Valor','Uso'],[[f'<code>{n}</code>',v,u] for n,v,u in DUR])}
{table(['Curva','Valores','Uso'],[[f'<code>{n}</code>',f'<code>{e}</code>',u] for n,e,u in EAS])}
<ul><li>Se anima: capas de estado, interruptor, fichas, entrada y salida de diálogo, hoja y menú, progreso.</li><li>En los componentes nada dura más de 400 ms.</li></ul>
<h3>La vitrina</h3>
{table(['Qué','Cómo se mueve','Tiempo'],[
 ['Laptop de la portada, al cargar','La tapa arranca cerrada y se abre; después aparecen las tres cifras, una tras otra, y quedan flotando.','Tapa 1 s (curva de entrada enfatizada); cifras 0,45 s cada una, separadas 0,12 s, desde 0,95 s; flotan en un ciclo de 6 s'],
 ['Laptop en computadora (con mouse)','Sigue al mouse con suavidad (±5° de costado, ±3° de arriba abajo) y, si nadie la toca, respira. El brillo, la sombra y las cifras se corren al revés para dar profundidad. Al bajar la página, la tapa se inclina hacia atrás.','Continuo, solo mientras se ve y con la pestaña al frente'],
 ['Laptop en celular','Un reflejo cruza la pantalla cada tanto, y la laptop se inclina con el desplazamiento (hasta ±9°).','Reflejo de 0,8 s a los 3,5 s y después cada 9 s, pausado con la pestaña oculta'],
 ['Al bajar la página','La laptop se aleja al salir (se achica al 90 % y baja su opacidad); las tarjetas de casos suben 72 px y crecen del 94 % al 100 %; los títulos grandes entran desde el costado (desde la derecha en hebreo); las filas de trabajos académicos suben 28 px.','Atado al desplazamiento, no al reloj (solo CSS)'],
 ['Barra de lectura (en cada caso)','Una línea de 3 px del color del caso, al pie de la barra de arriba, que se llena de izquierda a derecha a medida que se baja (de derecha a izquierda en hebreo).','Atada al desplazamiento, no al reloj (solo CSS)'],
 ['Indicador de carga','Mientras una imagen que llega después todavía no está, en el centro de la tarjeta o de la imagen flotante aparece la forma de DiDí que pasa de D a barra y a píldora, en amarillo («en curso»).','Aparece a los 0,2 s, para no parpadear si la imagen llega rápido; ciclo de 2,4 s hasta que la imagen termina de cargar'],
 ['De una página a otra','La página que se va sube 16 px y se apaga; la que llega sube desde 28 px. El título de la tarjeta viaja hasta el título del caso, y al volver hace el camino inverso. La barra de arriba no se mueve.','Salida 0,28 s; llegada 0,5 s con 0,05 s de espera; el título 0,5 s'],
 ['Tarjeta de caso, al pasar el mouse','Sube 3 px; el borde y la sombra toman el color del tipo; la imagen crece al 103 %.','Tarjeta 0,3 s; imagen 0,6 s'],
 ['Imagen de un trabajo académico (computadora)','Aparece junto al mouse, inclinada, y lo sigue mientras recorre la fila.','Aparece en 0,25 s; se endereza en 0,35 s'],
 ['Hojas de reconocimientos','En celular suben desde abajo y se cierran arrastrando hacia abajo; en computadora aparecen desde 16 px más abajo.','0,24 s'],
 ['Cuaderno (manuales de marca)','Las hojas giran en 3D al tocarlas o con las flechas.','0,9 s por hoja'],
 ['Prototipo que se puede tocar','Algunas pantallas avanzan solas, con una barra que muestra la espera.','Según la pantalla']])}
<h3>Reglas</h3>
<ul><li><strong>El logo no se anima,</strong> ni al cargar ni al cambiar de página.</li>
<li><strong>El texto no cambia de opacidad al moverse.</strong> A medio camino quedaría con poco contraste. Solo se mueve; lo que se desvanece es la laptop o la página entera.</li>
<li><strong>Sin desplazamiento forzado:</strong> la página nunca se mueve sola ni retiene la rueda del mouse.</li>
<li><strong>Lo continuo se pausa</strong> cuando la laptop sale de la pantalla o la pestaña queda oculta.</li>
<li>Con <code>prefers-reduced-motion: reduce</code> («reducir movimiento» en el sistema) se apaga todo: la laptop aparece abierta y quieta, con las cifras; no hay movimiento al bajar ni transición entre páginas; las hojas y las galerías cambian sin recorrido; el prototipo no avanza solo.</li>
<li>Donde el navegador no sabe hacer el movimiento al bajar o la transición entre páginas, la página se ve y se navega como siempre.</li></ul>
{note('<b>Ya no se usa en el sitio.</b> La v1 decía: «nada dura más de 400 ms; si dura más, es decoración», «no se animan los títulos al cargar», «no hay transición entre páginas» y «no hay contenido que se reproduzca solo». Hoy esas reglas valen para los componentes; la vitrina tiene las suyas, arriba.','m-open')}
{note('<b>Decisión registrada.</b> Se probó una animación de entrada del logo de 1,3 segundos y se descartó en 2026. Si alguna vez se vuelve a considerar, parte de cero.','m-ok')}'''))

# ---------- 10 · íconos ----------
ICON_ES={'arrow':'flecha','check':'tilde','close':'cerrar','menu':'menú','mail':'mail','download':'descargar','external':'afuera','warn':'aviso','plus':'más','search':'buscar','copy':'copiar','chev':'desplegar'}
icg=''.join(f'<div style="display:grid;gap:8px;justify-items:center;width:92px"><div style="color:#E6ECF5;display:flex;gap:10px;align-items:center">{ic(k,24)}{ic(k,18)}</div><span class="m-lbl" style="text-align:center">{ICON_ES.get(k,k)}</span></div>' for k in ICONS)

out.append(sec('iconos','Íconos','Un set propio mínimo, dibujado con la lógica del logo: trazo 2, terminales rectos, ángulos limpios.',f'''
<div class="m-panel"><div class="didi m-demo d-row" style="gap:18px">{icg}</div></div>
{table(['Regla','Valor'],[['Rejilla','24 × 24 px, zona segura de 20 px'],['Trazo','2 px, terminales rectos (no redondeados), uniones en inglete'],['Tamaños','24 px solos; 18 px dentro de botones, chips y etiquetas'],['Color','Hereda el color de la función del componente (<code>currentColor</code>)'],['Texto','Siempre acompañado de texto o <code>aria-label</code>; los decorativos llevan <code>aria-hidden</code>'],['Relleno','No hay íconos rellenos: el estado activo lo da el color y la barra, no el relleno']])}
{note('<b>Decisión abierta.</b> Este set son 12 íconos dibujados a mano para la maqueta, sin revisión óptica a 1×. La alternativa es el set de íconos estándar de Google (de contorno, peso 400, tamaño óptico 24), que ya trae todo el catálogo y se carga como fuente. Si el sitio necesita más de 15 íconos, conviene cambiar.','m-open')}'''))

# ---------- 11 · accesibilidad ----------
mn=lambda col,keys: min(ratio(col,SURF_HEX[k]) for k in keys)
allk=[k for k,_ in SURFS]
minpleno=min(ratio(c,SURF_HEX[k]) for c in LOGO.values() for k in allk)
minton=min(ratio(css_var(f'd-on-{k}-cont'),css_var(f'd-{k}-cont')) for _,k,_,_ in FUNC)
out.append(sec('accesibilidad','Accesibilidad','Lo que el sistema garantiza por construcción y lo que todavía no se verificó.',f'''
{table(['Criterio','Cómo se cumple','Estado'],[
 ['Contraste de texto (4,5:1)',f'Texto principal {ratio("#E6ECF5",SURF):.1f}:1; secundario desde {mn("#AAB7C9",allk):.1f}:1; textos tonales desde {minton:.1f}:1','<span class="m-pass">calculado</span>'],
 ['Contraste de gráficos y bordes (3:1)',f'Colores de función desde {minpleno:.1f}:1; contorno {mn(css_var("d-outline"),allk):.2f}:1 sobre el peor nivel','<span class="m-pass">calculado</span>'],
 ['Color no es el único portador','Cada función suma forma, ícono o texto; el error lleva ícono y mensaje','<span class="m-pass">por diseño</span>'],
 ['Foco visible','Anillo celeste 2 px con separación; contraste del anillo 12,5:1','<span class="m-pass">por diseño</span>'],
 ['Objetivos de 48 px','Margen interno en íconos, checkbox y radio; 48 px en táctil','<span class="m-pass">por diseño</span>'],
 ['Movimiento reducido','Sin transiciones ni animaciones con <code>prefers-reduced-motion</code>, también en la portada y entre páginas','<span class="m-pass">verificado por script</span>'],
 ['Teclado','El primer Tab llega a «Saltar al contenido»; el foco se ve en todo; las hojas atrapan el foco, lo ponen en su título al abrir y se cierran con Esc','<span class="m-pass">verificado por script</span>'],
 ['Lector de pantalla','Roles ARIA indicados en interruptor, checkbox, radio, pestañas y diálogo','<span class="m-fail">sin auditar</span>'],
 ['Zoom 200 % y texto a 320 px','Sin desborde horizontal a 390 px; 320 px y zoom al 200 % todavía sin probar','<span class="m-fail">sin probar</span>'],
 ['Velocidad','100 de 100 en Lighthouse, en celular y en computadora: estilos dentro de cada página, recortados a lo que usa; fuentes e imágenes de abajo llegan después','<span class="m-pass">medido</span>'],
 ['Modo de contraste forzado','No se contempló','<span class="m-fail">pendiente</span>']])}
<h3>Pautas</h3>
<ul><li>Cada página: un <code>h1</code>, <code>main</code>, <code>nav</code> y <code>footer</code>; <code>lang</code> en el <code>html</code> y en cada tramo de otro idioma.</li><li>Las imágenes llevan texto alternativo que dice qué muestran y qué importa de eso, no «captura de pantalla». Las portadas de las tarjetas y los logos chicos son decorativos: texto alternativo vacío.</li><li>Los enlaces dicen adónde van («Siguiente caso: Sistemas de trading»), nunca «clic acá».</li><li>Los campos tienen etiqueta visible y los errores se anuncian con texto, no solo con color.</li><li>La D sin palo se lee distinto: el nombre y los títulos llevan el texto completo en el marcado, sin fragmentarlo ni reemplazarlo por imágenes.</li></ul>
{note('<b>Lo calculado no es lo auditado.</b> Los ratios salen de la fórmula WCAG 2.x. No se pasaron por una herramienta externa ni por APCA, y nada se probó con lector de pantalla ni con personas.','m-open')}'''))
