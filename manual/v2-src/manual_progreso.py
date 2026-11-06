# Indicadores de progreso y de carga · rediseño sobre la especificación estándar.
# Se ejecuta desde manual_c.py y deja definida la variable PROGRESS (HTML de la sección).
import math
from manual_lib import ratio, css_var, SURF_HEX, SURF

def lin(p=62,t=4,ind=False,wavy=False,label='Progreso',w=None):
    cls=['d-lin']
    if t!=4: cls.append(f'd-lin--t{t}')
    if wavy: cls.append('d-lin--wavy d-lin--t'+str(t) if t==4 else 'd-lin--wavy')
    if ind: cls.append('d-lin--ind')
    if p>=100 and not ind: cls.append('d-lin--full')
    cls=' '.join(dict.fromkeys(' '.join(cls).split()))
    aria=f'role="progressbar" aria-label="{label}"'+('' if ind else f' aria-valuemin="0" aria-valuemax="100" aria-valuenow="{p}"')
    st=f'--p:{p};'+(f'width:{w}px;' if w else '')
    stop='' if ind else '<i class="d-lin__stop"></i>'
    return f'<div class="{cls}" style="{st}" {aria}><div class="d-lin__track"></div><div class="d-lin__fill"></div>{stop}</div>'
def lbox(inner,w=320,cap=None):
    c=f'<span class="m-lbl" style="width:auto">{cap}</span>' if cap else ''
    return f'<div style="display:grid;gap:10px;width:{w}px;max-width:100%">{inner}{c}</div>'

def dpath(wavy=False,A=5,lam=26,n=420):
    if not wavy: return 'M0 12 H67 A85 85 0 0 1 67 182 H0'
    L=67+math.pi*85+67; pts=[]
    for i in range(n+1):
        s=L*i/n
        if s<=67: x,y,nx,ny=s,12,0,-1
        elif s<=67+math.pi*85:
            th=-math.pi/2+(s-67)/85; x,y=67+85*math.cos(th),97+85*math.sin(th); nx,ny=math.cos(th),math.sin(th)
        else:
            u=s-67-math.pi*85; x,y,nx,ny=67-u,182,0,1
        o=A*math.sin(2*math.pi*s/lam); pts.append((x+nx*o,y+ny*o))
    return 'M'+' L'.join(f'{x:.1f} {y:.1f}' for x,y in pts)
def cir(p=62,h=64,ind=False,wavy=False,thick=False,label='Progreso',txt=None,colors=None,btn=False):
    fd=max(4,p); ts=min(100,fd+3); tl=max(0,100-ts)
    sty=f'height:{h}px;--fd:{fd};--ts:{ts};--tl:{tl};'
    if colors: sty+=f'--a:{colors[0]};--tr:{colors[1]};'
    if thick: sty+='--w:30;'
    cls='d-cir'+(' d-cir--ind' if ind else '')+(' d-cir--btn' if btn else '')
    aria=f'role="progressbar" aria-label="{label}"'+('' if ind else f' aria-valuemin="0" aria-valuemax="100" aria-valuenow="{p}"')
    flat=dpath(False); active=dpath(wavy,A=(4 if thick else 3.2),lam=57) if wavy else flat
    t=f'<text x="62" y="118" text-anchor="middle" style="font:700 46px var(--d-sans);fill:var(--d-on)">{txt}</text>' if txt else ''
    return f'<span class="{cls}" style="{sty}" {aria}><svg viewBox="-10 -6 180 204" xmlns="http://www.w3.org/2000/svg"><path class="t" pathLength="100" d="{flat}"/><path class="f" pathLength="100" d="{active}"/>{t}</svg></span>'
def cell(inner,cap): return f'<div style="display:grid;gap:8px;justify-items:center">{inner}<span class="m-lbl" style="width:auto;text-align:center">{cap}</span></div>'
def load(size='',label='Cargando'): return f'<div class="d-load {size}" role="progressbar" aria-label="{label}"><i></i></div>'

# ---------- contrastes calculados ----------
ACT=css_var('d-atencion'); TRK=css_var('d-atencion-cont')
r_act=ratio(ACT,SURF); r_trk=ratio(TRK,SURF)
r_trk_low=ratio(TRK,SURF_HEX['low']); r_act_low=ratio(ACT,SURF_HEX['low'])
r_btn=ratio('#0F1B2D','#E890CC')

# ---------- piezas ----------
anat=lbox(lin(38,t=4,wavy=True),w=520)
anat_html=f'''<div style="position:relative;width:520px;max-width:100%;padding:6px 0 56px">{lin(38,t=4,wavy=True)}
<span class="m-lbl" style="position:absolute;left:0;top:34px;width:auto">▲ tramo activo</span>
<span class="m-lbl" style="position:absolute;left:52%;top:34px;width:auto">▲ pista</span>
<span class="m-lbl" style="position:absolute;right:0;top:34px;width:auto">▲ parada</span></div>
<p class="m-lbl" style="margin:0 0 18px;width:auto">El tramo activo termina en una D acostada (lado plano atrás, lado redondo adelante). La pista es el mismo color, en tono. La parada es un círculo de 4 px.</p>'''
anat_ring=R(cell(cir(38,120,wavy=False),'tramo activo y pista; sin punto de parada'),cell(cir(38,120,wavy=True),'el tramo activo, ondulado'),top=True)

flat_rows=''.join(R(lbox(lin(62,t=t),w=300,cap=f'plano · {t} px'),lbox(lin(62,t=t,wavy=True),w=300,cap=f'ondulado · {t} px'),top=True) for t in (4,8,12,16))
states_lin=R(lbox(lin(0),w=220,cap='0 %: empieza como un punto'),lbox(lin(25),w=220,cap='25 %'),lbox(lin(62),w=220,cap='62 %'),lbox(lin(100),w=220,cap='100 %: sin pista ni parada'),top=True)
ind_lin=R(lbox(lin(ind=True),w=300,cap='indeterminado · plano'),lbox(lin(ind=True,wavy=True),w=300,cap='indeterminado · ondulado'),top=True)
to_det=R(lbox(lin(ind=True),w=220,cap='1 · no se sabe cuánto falta'),lbox(lin(35),w=220,cap='2 · se supo: pasa a determinado'),top=True)

sizes=R(cell(cir(0,24),'24 px · mínimo'),cell(cir(25,40),'40 px'),cell(cir(62,64),'64 px'),cell(cir(62,120),'120 px'),cell(cir(100,200),'200 px · completo'),top=True)
cir_var=R(cell(cir(62,120),'plana'),cell(cir(62,120,wavy=True),'ondulada'),cell(cir(62,120,thick=True),'gruesa'),cell(cir(62,120,wavy=True,thick=True),'ondulada y gruesa'),cell(cir(0,120,ind=True),'indeterminada: crece y se achica mientras recorre la D'),top=True)

frame_top=f'''<div style="width:100%;max-width:520px;border:1px solid #2B3A52;background:var(--d-surface)"><div class="d-appbar" style="height:56px"><span style="font:600 1rem var(--d-sans)">Kol Accesorios</span><span class="d-grow"></span><span class="d-label-m" style="color:var(--d-on-var)">cargando el caso</span></div>{lin(ind=True,label="Cargando el caso")}<div style="padding:20px"><div style="height:12px;background:var(--d-low);width:62%;margin-bottom:10px"></div><div style="height:12px;background:var(--d-low);width:88%;margin-bottom:10px"></div><div style="height:12px;background:var(--d-low);width:74%"></div></div></div>'''
frame_card=f'''<div class="d-card" style="padding:0;overflow:hidden;width:300px"><div style="padding:20px"><h3 style="font:600 1.125rem/1.5rem var(--d-sans);margin:0 0 6px">Campaign Suite</h3><p style="margin:0">Actualizando los datos de la semana.</p></div>{lin(ind=True,label="Actualizando la tarjeta")}<div style="height:4px"></div></div>'''
frame_center=f'''<div class="d-card d-card--outlined" style="width:300px;height:170px;display:grid;place-items:center">{cir(0,64,ind=True,label="Cargando las capturas")}</div>'''
btns=R(f'<button class="d-btn d-st" aria-busy="true" aria-label="Enviando el mensaje">{cir(0,20,ind=True,btn=True)} Enviando</button>',f'<button class="d-btn d-btn--tonal d-st" aria-busy="true">{cir(0,20,ind=True,btn=True)} Enviando</button>',f'<button class="d-btn d-btn--outlined d-st" aria-busy="true">{cir(0,20,ind=True,btn=True)} Enviando</button>',f'<button class="d-btn d-btn--d d-st" aria-busy="true">{cir(0,20,ind=True,btn=True)} Enviando</button>')
more=f'''<div class="d-list" style="width:320px"><a class="d-item d-st" href="#"><span class="d-item__l">01</span><span><b>Kol Accesorios</b></span><span></span></a><a class="d-item d-st" href="#"><span class="d-item__l">02</span><span><b>Sistemas de trading</b></span><span></span></a><div style="display:grid;place-items:center;height:72px">{load(label="Cargando más casos")}</div></div>'''
do_group=f'''<div class="d-card d-card--outlined" style="width:280px"><div style="padding:0 0 12px">{lin(48,label="Subiendo 3 archivos")}</div><div class="d-body-s" style="color:var(--d-on-var)">Subiendo 3 archivos · 48 %</div><div class="d-body-m" style="margin-top:10px">captura-1.webp<br>captura-2.webp<br>captura-3.webp</div></div>'''
dont_group=f'''<div class="d-card d-card--outlined" style="width:280px;display:grid;gap:12px"><div><div class="d-body-m">captura-1.webp</div>{lin(80,t=4,label="captura 1")}</div><div><div class="d-body-m">captura-2.webp</div>{lin(35,t=4,label="captura 2")}</div><div><div class="d-body-m">captura-3.webp</div>{lin(10,t=4,label="captura 3")}</div></div>'''
dont_btns=R(f'<button class="d-btn d-btn--tonal d-st">{cir(0,20,ind=True,btn=True)} Copiar</button>',f'<button class="d-btn d-btn--tonal d-st">{cir(0,20,ind=True,btn=True)} Compartir</button>',f'<button class="d-btn d-btn--tonal d-st">{cir(0,20,ind=True,btn=True)} Descargar</button>')
ext=(R(lbox(f'<div class="d-steps">{"".join(["<div class=\"d-step is-done\"><i></i><span>01 Mensaje</span></div>","<div class=\"d-step is-now\" style=\"--p:60%\"><i></i><span>02 Revisión</span></div>","<div class=\"d-step\"><i></i><span>03 Enviado</span></div>"])}</div>',w=420,cap='Pasos: un proceso con etapas. Un segmento por etapa; el actual, a medias.'),top=True)
 +R(lbox(f'<div class="d-readbar" style="--p:40%"><i></i></div>',w=420,cap='Lectura (celeste): dónde estás en un texto largo. No es un proceso: es una posición.'),top=True)
 +R(cell(cir(75,120,colors=('var(--d-dato)','var(--d-dato-cont)'),txt='3/4',label='3 de cada 4 respuestas de IA con un dato mal'),'proporción de un dato (azul)'),cell(cir(100,120,colors=('var(--d-dato)','var(--d-dato-cont)'),txt='27',label='27 páginas'),'una cifra completa'),top=True))
morph=R(cell(load(),'48 px'),cell(load('d-load--lg'),'72 px'),top=True)

PROGRESS=f'''
<h3>Progress indicators</h3>
<p class="m-lbl" style="max-width:84ch;font-size:.8125rem;margin:-2px 0 10px">Rediseñados sobre la especificación estándar de indicadores de progreso: dos variantes, lineal y circular; determinado e indeterminado; plano y ondulado; grosor de 4 px o variable; tres partes: tramo activo, pista y punto de parada. La forma es de DiDí: el tramo activo termina en una D acostada y el circular es la D del logo.</p>
<h4 class="m-h4">Anatomía</h4>
<div class="m-panel"><div class="didi m-demo">{anat_html}{anat_ring}</div></div>
<ul style="margin:10px 0 4px"><li><strong>Tramo activo.</strong> Lo que ya avanzó. Amarillo, porque un proceso en curso es atención. Aparece apenas empieza el proceso, como un punto, para que se note que algo avanza.</li><li><strong>Pista.</strong> Lo que falta, en el tono del mismo color. Entre el tramo y la pista hay una separación de 4 px.</li><li><strong>Punto de parada.</strong> Un círculo de 4 px al final de la pista, solo en el lineal determinado. Es obligatorio si la pista no llega a 3:1 contra lo que tiene detrás: acá la pista da {r_trk:.1f}:1 sobre la superficie, así que se usa siempre.</li></ul>
<h4 class="m-h4">Lineal · determinado</h4>
<div class="m-panel"><div class="didi m-demo">{states_lin}</div></div>
<h4 class="m-h4">Lineal · grosor y forma</h4>
<div class="m-panel"><div class="didi m-demo">{flat_rows}</div></div>
<p class="m-lbl">Grosor de 4 px por defecto y 8, 12 o 16 si el lugar lo pide. La onda crece con el grosor (amplitud 3, 4, 5 y 6 px; longitud de onda de 40 px). Esos valores son míos: la especificación muestra la onda en gráficos, sin cifras. El lineal siempre ocupa el ancho de su contenedor, con 4 px de margen en cada punta, y no se usa en elementos de menos de 40 px.</p>
<h4 class="m-h4">Lineal · indeterminado, y el paso a determinado</h4>
<div class="m-panel"><div class="didi m-demo">{ind_lin}{to_det}</div></div>
<p class="m-lbl">El indeterminado crece y se achica mientras recorre la pista. En cuanto se sepa cuánto falta, pasa a determinado.</p>
<h4 class="m-h4">Circular · la D</h4>
<div class="m-panel"><div class="didi m-demo">{sizes}{cir_var}</div></div>
<p class="m-lbl">Recorre la D desde la línea de arriba, hacia la derecha (el sentido de las agujas del reloj). Tamaños de 24 a 240 px; la onda se escala con el tamaño y a 24 px casi no se ve, ahí va plano. No lleva punto de parada.</p>
<h4 class="m-h4">Dónde va cada uno</h4>
<div class="m-panel"><div class="didi m-demo">{R(lbox(frame_top,w=520,cap='Arriba de la página: un solo indicador para todo lo que carga.'),lbox(frame_card,w=300,cap='Pegado al borde de la tarjeta que se actualiza.'),lbox(frame_center,w=300,cap='Circular centrado en lo que carga.'),top=True)}{R(lbox(btns,w=560,cap='En un botón: circular chico; el tramo toma el color del texto y no hay pista (así llega a {r_btn:.1f}:1). En botones muy chicos, plano.'.format(r_btn=r_btn)),lbox(more,w=320,cap='Cargando más elementos: en el hueco donde van a aparecer, sin tapar lo que ya está.'),top=True)}</div></div>
<h4 class="m-h4">Cuándo usar cuál</h4>
{table(['Espera esperada','Qué mostrar'],[['Instantánea (menos de 200 ms)','Nada: mostrar el contenido enseguida.'],['Corta (de 200 ms a 5 s)','Indicador de carga (el de abajo).'],['Larga (más de 5 s)','Indicador de progreso. Si es muy larga, dejar que la persona siga navegando mientras termina.']])}
<div class="m-two"><div class="m-do"><b>Sí</b><div class="m-lbl" style="margin:0 0 10px">Un solo indicador para el grupo</div><div class="didi" style="padding:14px">{do_group}</div></div><div class="m-dont"><b>No</b><div class="m-lbl" style="margin:0 0 10px">Un indicador por cada actividad</div><div class="didi" style="padding:14px">{dont_group}</div></div></div>
<div class="m-two" style="margin-top:14px"><div class="m-do"><b>Sí</b><p style="margin:0 0 6px">Un proceso se representa siempre con la misma variante en todo el sitio: si el envío del formulario usa el circular en el botón, siempre es el circular en el botón. Circular para actividades de menos de 5 s.</p></div><div class="m-dont"><b>No</b><div class="m-lbl" style="margin:0 0 10px">Un indicador en cada botón de una lista</div><div class="didi" style="padding:14px">{dont_btns}</div></div></div>
<h4 class="m-h4">Accesibilidad</h4>
{table(['Qué','Valor','Resultado'],[
 ['Tramo activo y punto de parada sobre la superficie',f'{ACT} sobre {SURF}',f'{r_act:.1f}:1 · pasa 3:1'],
 ['Tramo activo sobre una tarjeta (contenedor bajo)',f'{ACT} sobre {SURF_HEX["low"]}',f'{r_act_low:.1f}:1 · pasa 3:1'],
 ['Pista sobre la superficie',f'{TRK} sobre {SURF}',f'{r_trk:.1f}:1 · no llega a 3:1: <strong>el punto de parada es obligatorio</strong>'],
 ['Tramo en un botón rosa (color del texto, sin pista)','#0F1B2D sobre #E890CC',f'{r_btn:.1f}:1 · pasa 3:1']])}
<div class="m-pre">&lt;div class="d-lin" role="progressbar" aria-label="Cargando el caso"
     aria-valuemin="0" aria-valuemax="100" aria-valuenow="62" style="--p:62"&gt;
  &lt;div class="d-lin__track"&gt;&lt;/div&gt;&lt;div class="d-lin__fill"&gt;&lt;/div&gt;&lt;i class="d-lin__stop"&gt;&lt;/i&gt;
&lt;/div&gt;
&lt;!-- indeterminado: sin aria-valuenow --&gt;</div>
<ul style="margin:10px 0 4px"><li>Rol <code>progressbar</code> y una etiqueta que dice el proceso y el contenido: "Cargando el caso", "Actualizando la tarjeta", "Enviando el mensaje". Nunca solo "Cargando".</li><li>En una escritura de derecha a izquierda, el lineal se espeja y el circular no.</li><li>Con movimiento reducido, el indeterminado queda quieto en una posición legible.</li></ul>
<h4 class="m-h4">Indicador de carga</h4>
<div class="m-panel"><div class="didi m-demo">{morph}</div></div>
<p class="m-lbl">Para esperas de 200 ms a 5 s. Una forma que cambia entre las tres del logo, la D, la barra y la píldora, dentro de un contenedor en D. Con movimiento reducido queda la D quieta.</p>
<h4 class="m-h4">Extensiones DiDí (no están en la base)</h4>
<div class="m-panel"><div class="didi m-demo">{ext}</div></div>
<ul style="margin:10px 0 4px"><li><strong>Amarillo</strong> = un proceso en curso. <strong>Celeste</strong> = dónde estás en una lectura. <strong>Azul</strong> = la proporción de un dato; no es un proceso, pero usa el mismo dibujo.</li><li>Un proceso que termina no se pinta de verde: el verde es verificado, y terminar de cargar no verifica nada.</li></ul>'''
