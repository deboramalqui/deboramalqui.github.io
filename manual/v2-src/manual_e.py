# Parte E · Referencia (secciones 25 y 25) + script de las demos.
out.append(part('Parte E · Referencia'))
out.append(sec('tokens','Variables y archivos','El sistema vive en una hoja de estilos; el sitio suma la suya encima. En cada página publicada, las dos van adentro, recortadas a lo que esa página usa.',f'''
<h3>Cómo se usa</h3>
<div class="m-pre">&lt;link rel="stylesheet" href="marca/didi-ui.css"&gt;
&lt;body class="didi"&gt;
  &lt;a class="d-btn d-btn--d d-st"&gt;Escribime&lt;/a&gt;
  &lt;span class="d-chip-data"&gt;2026&lt;/span&gt;
&lt;/body&gt;

/* Color del tipo de un caso: lo pone el generador del sitio en .s-case */
.s-case {{ --tone: var(--d-accion); }}   /* Campañas */

/* D clásica de reserva en los párrafos de lectura (decisión pendiente): */
.d-prose {{ font-feature-settings: "ss20"; }}</div>
<h3>Variables</h3>
<div class="m-pre">{tokens_pre()}</div>
<h3>Archivos</h3>
{table(['Qué','Dónde'],[
 ['Variables y componentes del sistema','<code>marca/didi-ui.css</code> · gestos en <code>marca/didi-gestos.js</code>'],
 ['Estilos y movimiento del sitio (portada, casos, color por tipo, transición entre páginas)','<code>sitio-src/site.css</code> · <code>sitio-src/site.js</code>'],
 ['Colores por tipo y casos destacados','<code>TONES</code>, <code>TONOS_D</code> y <code>FEATURED</code> en <code>tools/build_sitio.py</code>'],
 ['Recorte de estilos por página','<code>tools/css_purga.py</code>'],
 ['Logo, favicon y PNG','<code>marca/</code> y <code>marca/png/</code>'],
 ['Fuentes y licencias','<code>fuentes/</code> · <code>OFL-figtree.txt</code> · <code>OFL-dmmono.txt</code> · <code>OFL-heebo.txt</code>'],
 ['Generador de las fuentes','<code>tools/build_fuente_didi.py</code>'],
 ['Verificación del sitio','<code>tools/verificar_sitio.py</code> → <code>sitio-src/verificacion.json</code>'],
 ['Este manual','<code>manual/manual-didi-v2.html</code> · generado con <code>manual/v2-src/build_manual_v2.py</code>'],
 ['El manual anterior','<code>manual/manual-didi-v1.html</code> y su PDF, sin cambios'],
 ['Hoja de verdad y fichas de proyecto','<code>hoja-de-verdad.md</code> · <code>fichas/</code>'],
 ['Cómo mantener el sitio','<code>MANTENIMIENTO.md</code>']])}'''))

out.append(sec('abiertas','Decisiones abiertas y qué no se verificó','Lo que falta decidir y lo que este manual afirma sin haberlo probado.',f'''
<h3>Decisiones abiertas</h3>
{table(['#','Decisión','Qué cambia','Propuesta'],[
 ['1','Hebreo: revisión por una persona nativa y espejo completo de las formas con la D','Hoy el hebreo está traducido por IA con una guía; la D de botones y etiquetas no se espeja; el plural y el singular se mezclan','Una revisión antes de la próxima publicación grande; propiedades lógicas para los radios'],
 ['2','D clásica (ss20) en párrafos de lectura','Legibilidad de textos largos','Clásica solo en párrafos de más de dos líneas a 17 px o menos; sin palo en todo lo demás'],
 ['3','Set de íconos: propio o el estándar de Google','Consistencia y mantenimiento','El estándar si se necesitan más de 15 íconos'],
 ['4','Error: amarillo con ícono, o un sexto color','Un color más en el sistema','Amarillo con ícono y texto; el único error es el del formulario'],
 ['5','Orden de los trabajos académicos','La lista de la portada','Por año, cuando Débora pase los años'],
 ['6','Peso de las páginas con muchas imágenes','Cinco páginas pasan de 1,5 MB en computadora (Kol, Communiqué, i24NEWS, Skyline, Relaciones afectivas)','Cargar más imágenes en diferido o achicarlas'],
 ['7','Premios en reconocimientos','La baldosa y la hoja','No se muestran hasta tener pruebas y nombres']])}
<h3>Decisiones que la v1 dejó abiertas y ya se cerraron</h3>
{table(['Decisión','Cómo se cerró'],[
 ['Heebo empaquetada','Incluida en el sitio (bloque hebreo, 20 KB).'],
 ['Línea de presentación y título','Frase fija de la portada, aprobada por Débora.'],
 ['Botón flotante de contacto en celular','Sí: «Escribime», extendido, en celular y tableta.'],
 ['Fecha de disponibilidad','No se publica.'],
 ['Casos en la portada y su orden','Campaign Suite y Medido destacados; los demás (Kol Accesorios entre ellos) en el orden del generador.'],
 ['Nombre del cliente anonimizado','Kol Accesorios con su nombre real.'],
 ['Teléfono','Va solo en el pie, como enlace de WhatsApp, y en los datos estructurados (pedido de Débora, 2026).']])}
<h3>Lo que este manual no verificó</h3>
{table(['Qué','Estado'],[
 ['Contrastes','Calculados con la fórmula WCAG 2.x por el generador. Lighthouse revisa el contraste del texto en cada página; no se pasaron por APCA.'],
 ['Fuentes DiDi Sans y DiDi Mono','Sin ajuste manual para pantallas de baja resolución: en Windows y a tamaños chicos pueden verse distintas. Sin prueba propia en Safari ni Firefox.'],
 ['La D sin palo en texto corrido','Observación propia (se parece a una C al revés), sin prueba de lectura con personas.'],
 ['Mínimos del logo (96 px, 25 mm)','Calculados por proporción; no probados en pantallas reales a 1×.'],
 ['Íconos propios','Sin revisión óptica a 18 y 24 px en pantallas de baja densidad.'],
 ['Componentes que el sitio no usa','Maquetas en este manual, con interacción mínima. Sin lector de pantalla ni modo de contraste forzado.'],
 ['Movimiento de la vitrina','Revisado en Chromium. El movimiento al bajar y la transición entre páginas dependen del navegador: donde no existen, la página funciona sin ellos.'],
 ['Hebreo y escritura de derecha a izquierda','Construido y verificado por script (idioma, dirección, desborde, gestos); sin revisión de una persona nativa ni prueba en lector de pantalla en hebreo.'],
 ['Personas','Nada de este manual se probó con personas. Es un sistema coherente, calculado y verificado por script, no uno validado con visitantes.']])}'''))

out.append('''<script>
(function(){
  var q=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  q('[data-sw]').forEach(function(b){b.addEventListener('click',function(){if(b.disabled)return;b.setAttribute('aria-checked',b.getAttribute('aria-checked')==='true'?'false':'true')})});
  q('[data-check]').forEach(function(b){b.addEventListener('click',function(){if(b.disabled)return;b.setAttribute('aria-checked',b.getAttribute('aria-checked')==='true'?'false':'true')})});
  q('[data-radio]').forEach(function(b){b.addEventListener('click',function(){if(b.disabled)return;var g=b.closest('.d-row');q('[data-radio]',g).forEach(function(x){x.setAttribute('aria-checked','false')});b.setAttribute('aria-checked','true')})});
  q('[data-chipsel]').forEach(function(b){b.addEventListener('click',function(){b.classList.toggle('is-selected')})});
  q('[data-tab]').forEach(function(b){b.addEventListener('click',function(){q('[data-tab]',b.parentNode).forEach(function(x){x.classList.remove('is-active')});b.classList.add('is-active')})});
  q('[data-seg]').forEach(function(b){b.addEventListener('click',function(){q('[data-seg]',b.parentNode).forEach(function(x){x.classList.remove('is-selected')});b.classList.add('is-selected')})});
  q('[data-multi]').forEach(function(b){b.addEventListener('click',function(){b.classList.toggle('is-selected')})});
  q('[data-sel]').forEach(function(b){b.addEventListener('click',function(){q('[data-sel]',b.parentNode).forEach(function(x){x.classList.remove('is-selected')});b.classList.add('is-selected')})});
  q('.d-range').forEach(function(r){var f=function(){var p=(r.value-r.min)/(r.max-r.min)*100;r.style.setProperty('--v',p+'%')};r.addEventListener('input',f);f()});
  var links=q('.m-toc a[href^="#"]');var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('is-on',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-20% 0px -70% 0px'});
  q('section.m-sec').forEach(function(s){io.observe(s)});
})();
</script>''')
