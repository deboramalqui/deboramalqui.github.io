# Secciones "Gestos" y "Usabilidad" (se ejecutan dentro de build_manual, después de "caso")
import json as _json
_VER=_json.loads((ROOT/'sitio-src'/'verificacion.json').read_text()) if (ROOT/'sitio-src'/'verificacion.json').exists() else []

out.append(sec('gestos','Gestos','Los gestos sirven para mostrar el trabajo: recorrer capturas, ampliarlas, ver de dónde sale una cifra y cerrar una hoja. La regla: el gesto acelera, nunca esconde. Todo lo que se hace con un gesto también se hace con un botón o con una tecla.',f'''
{table(['Gesto','Qué hace en el sitio','Alternativa sin gesto','Dónde'],[
['Tocar','Abre la captura ampliada','Botón de lupa visible sobre cada captura, 48 px de zona','Capturas de los casos'],
['Doble toque','Acerca y aleja dentro de la captura ampliada','Botón de lupa en la barra, tecla + o −','Captura ampliada'],
['Pellizcar','Acerca la captura ampliada con dos dedos','Doble toque, lupa o teclas','Captura ampliada (celular)'],
['Mantener presionado (600 ms)','Muestra de dónde sale una cifra, con un anillo en forma de D que se llena mientras se sostiene','Enter o espacio sostenidos','Baldosas de cifras en Kol Accesorios, Campaign Suite, Santo Tomé y Medido'],
['Deslizar','Pasa de una imagen a la siguiente en una galería','Botones anterior y siguiente, flechas del teclado, puntos de posición','Galerías de Santo Tomé, Waycare y Medido'],
['Desplazar','Recorre una web larga dentro de la pantalla del monitor, sin perder el lugar de la página','Teclado: Tab a la pantalla y flechas; pestañas para cambiar de página','Monitor de Kol Accesorios'],
['Arrastrar hacia abajo','Cierra la hoja de reconocimientos','«Listo», Esc o tocar el fondo','Hojas de becas, exposiciones y colaboraciones (celular)'],
['Tocar la hoja','Pasa la hoja del cuaderno','Flechas en pantalla y del teclado','Cuadernos de manuales de marca'],
['Atrás','Cierra lo ampliado sin salir de la página','Esc o botón cerrar','Captura ampliada']])}
{note('<b>Ya no se usa en el sitio.</b> La v1 tenía «Arrastrar la manija del antes y después» para comparar las tres IA en el caso Nido. Esa comparación no está en el sitio de hoy; el componente sigue en <code>didi-gestos.js</code>.','m-open')}
<h3>Reglas</h3>
<ul><li><b>Nada obligatorio.</b> Ninguna información vive solo detrás de un gesto. Los gestos aceleran o profundizan.</li>
<li><b>Descubrible.</b> Cada página con gestos dice cuáles hay en una línea, arriba del primer elemento que los usa («Desplazate dentro de la pantalla para recorrer la página»).</li>
<li><b>Sin conflicto con el sistema.</b> Los gestos de borde de pantalla (volver, cerrar app) no se usan; el deslizar de las galerías empieza adentro de la imagen.</li>
<li><b>Movimiento reducido.</b> Con esa preferencia activa, las galerías saltan sin animar y el anillo se muestra lleno sin recorrido.</li>
<li><b>Zona de toque de 48 px.</b> Los botones se ven de 40 px y se tocan en 48: la zona extra es invisible y no cambia el dibujo.</li></ul>
{note('<b>Cómo se verificó.</b> Un script abre cada gesto en un navegador real y comprueba el resultado (la galería avanza, la captura abre y cierra con Esc y con Atrás, el anillo y la fuente aparecen). No reemplaza probar con un dedo real en un celular.','')}
'''))

def _agg(page_prefix=None):
    asp=['Eficiencia','Errores','Aprender','Recordar','Satisfacción']
    rows=[]
    pages=[]
    for r in _VER:
        base=r['pagina'].split(' · ')[0]
        if base not in pages and base not in ('Gestos','Todo el sitio'): pages.append(base)
    for pg in pages+['Gestos','Todo el sitio']:
        rs=[r for r in _VER if r['pagina'].split(' · ')[0]==pg]
        cells=[]
        for a in asp:
            ra=[r for r in rs if r['aspecto']==a]
            if not ra: cells.append('—'); continue
            ok=sum(1 for r in ra if r['estado']=='ok'); cells.append(f'{ok} de {len(ra)}')
        rows.append([pg]+cells+[f"{sum(1 for r in rs if r['estado']=='ok')} de {len(rs)}"])
    return asp,rows
_asp,_rows=_agg()
_ids={}
for r in _VER: _ids.setdefault(r['id'],(r['aspecto'],r['chequeo']))
_lista=[[i,a,c] for i,(a,c) in sorted(_ids.items(),key=lambda kv:(['Eficiencia','Errores','Aprender','Recordar','Satisfacción'].index(kv[1][0]),kv[0]))]
_tot=len(_VER); _ok=sum(1 for r in _VER if r['estado']=='ok')

_paginas={r['pagina'].split(' · ')[0] for r in _VER}
if len(_paginas)<20:
    # la última corrida fue parcial: se muestra la última corrida completa, guardada al generar el manual
    _n=sum(1 for x in SECS if x[0]!='PART')+1; SECS.append(('SEC','usabilidad',_n,'Usabilidad'))
    _h=(ROOT/'manual'/'v2-src'/'usabilidad-ultima-completa.html').read_text()
    out.append(_h.replace('<h3>Resultado por página</h3>',note('<b>Última corrida completa.</b> La verificación más reciente revisó solo algunas páginas; esta tabla es la última que recorrió todo el sitio, en los tres idiomas. Se actualiza sola cuando se vuelva a correr completa.','')+'<h3>Resultado por página</h3>',1))
else:
  out.append(sec('usabilidad','Usabilidad','Cada trabajo que se muestra se verifica antes de publicarse con cinco aspectos de usabilidad: eficiencia, errores, facilidad de aprender, facilidad de recordar y satisfacción. Lo automático se corre con un script; lo que no se puede automatizar se prueba con personas.',f'''
<div class="m-two"><div>{card('Eficiencia','Se llega a lo importante rápido: el título a la vista, una sola acción principal por pantalla, contacto a un toque.')}{card('Errores','Nada se rompe: sin desborde, sin imágenes rotas, sin fallos de código, y todo gesto se puede deshacer (Esc, Atrás).')}{card('Facilidad de aprender','Estructura previsible: un solo H1, títulos sin saltos, objetivos de 48 px, líneas de lectura cortas, foco visible.')}</div><div>{card('Facilidad de recordar','La navegación es idéntica en todas las páginas: el que vuelve encuentra todo donde lo dejó.')}{card('Satisfacción','Contraste suficiente, carga liviana, movimiento sobrio y respeto por la preferencia de movimiento reducido.')}</div></div>
<h3>Resultado por página</h3>
<p>Resultado de la última corrida: <b>{_ok} de {_tot}</b> chequeos en verde. Cada página se mide en español, inglés y hebreo, en computadora (1360 px) y en celular (390 px). Los avisos son de peso: páginas con muchas imágenes que, en computadora, pasan de 1,5 MB en la carga inicial.</p>
<p><strong>Velocidad:</strong> 100 de 100 en Lighthouse, en celular y en computadora. Se mide con <code>npx lighthouse@12.6.1 &lt;dirección&gt;</code> (celular) y con <code>--preset=desktop</code>.</p>
{table(['Página']+_asp+['Total'],_rows)}
<h3>Qué se chequea</h3>
{table(['Id','Aspecto','Chequeo'],_lista)}
<h3>Lo que esto no prueba</h3>
{note('<b>Un control automático no es una persona.</b> Encuentra lo medible: lo que se rompe, lo que no se lee, lo que tarda. No me dice si alguien entiende en cinco segundos qué hago, si el humor de un texto cae bien ni si un gesto se descubre solo. Por eso analizo la experiencia y la interfaz midiendo lo que hacen las personas, no lo que opinan.','m-open')}
<p>La prueba mínima, así la planteo: cinco personas del público real (alguien con un comercio, alguien de marketing, alguien de selección de personal), sin explicarles nada.</p>
<ol><li>Abren la portada y, a los cinco segundos, les pregunto qué hago.</li>
<li>Buscan un resultado concreto de un caso, y mido cuánto tardan en encontrarlo.</li>
<li>Me escriben, y cuento cuántos toques necesitaron.</li>
<li>Sin avisarles, miro si descubren que una cifra se puede mantener presionada y que la laptop de la portada es mi propio producto.</li>
<li>Lo repito en el celular, y anoto dónde dudan.</li></ol>
<p class="m-lbl m-privado">Se corre con: <code>python3 tools/verificar_sitio.py</code> (necesita el sitio abierto en el servidor local). Escribe <code>sitio-src/verificacion.json</code>.</p>
'''))
