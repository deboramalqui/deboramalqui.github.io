/* DiDí · gestos. Sin dependencias; sin este script, todo se puede ver (las galerías son una tira que se desplaza,
   las capturas se abren en otra pestaña con el clic, y las fuentes están en las tablas).
   Gestos: deslizar (galería), tocar y doble toque (ampliar), pellizcar y desplazar (dentro de lo ampliado),
   mantener presionado (fuente de una cifra), arrastrar (antes y después), atrás (cierra lo ampliado). */
(function(){
  var q=function(s,r){return [].slice.call((r||document).querySelectorAll(s))};
  var LANG=((document.documentElement.getAttribute('lang')||'es').slice(0,2));
  var T={
    es:{lb:'Captura ampliada',zoom:'Acercar o alejar',close:'Cerrar',region:'Captura, se puede desplazar',hint:'Doble toque o la lupa: acercar y alejar. Pellizcá para acercar. Esc o Atrás: cerrar.',open:'Ampliar la captura',hold:'. Mantené presionado para ver la fuente.',src:'Fuente',before:'Antes',after:'Después',between:'Entre el antes y el después'},
    en:{lb:'Enlarged screenshot',zoom:'Zoom in or out',close:'Close',region:'Screenshot, scrollable',hint:'Double-tap or the magnifier: zoom in and out. Pinch to zoom. Esc or Back: close.',open:'Enlarge the screenshot',hold:'. Press and hold to see the source.',src:'Source',before:'Before',after:'After',between:'Between before and after'},
    he:{lb:'צילום מסך מוגדל',zoom:'התקרבות או התרחקות',close:'סגירה',region:'צילום מסך, ניתן לגלילה',hint:'הקשה כפולה או המגדלת: התקרבות והתרחקות. צבטו כדי להתקרב. Esc או חזרה: סגירה.',open:'הגדלת צילום המסך',hold:'. לחיצה ממושכת להצגת המקור.',src:'מקור',before:'לפני',after:'אחרי',between:'בין לפני לאחרי'}
  }[LANG]||{};
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ICON={zoom:'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M10 4a6 6 0 100 12 6 6 0 000-12zM15 15l5 5M10 7v6M7 10h6"/></svg>',
            close:'<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'};

  /* ---------- galería: deslizar ---------- */
  q('.d-gal').forEach(function(g){
    var v=g.querySelector('.d-gal__view'),items=q('.d-gal__item',v),dots=q('.d-gal__dots i',g),
        prev=g.querySelector('[data-gal="prev"]'),next=g.querySelector('[data-gal="next"]'),count=g.querySelector('.d-gal__count');
    function idx(){var c=v.scrollLeft+v.clientWidth/2,best=0,bd=1e9;items.forEach(function(it,i){var d=Math.abs(it.offsetLeft+it.offsetWidth/2-c);if(d<bd){bd=d;best=i}});return best}
    function upd(){var i=idx();dots.forEach(function(d,j){d.classList.toggle('is-on',j===i)});if(prev)prev.disabled=i===0;if(next)next.disabled=i===items.length-1;if(count)count.textContent=(i+1)+' / '+items.length}
    function go(i){i=Math.max(0,Math.min(items.length-1,i));v.scrollTo({left:items[i].offsetLeft-(v.clientWidth-items[i].offsetWidth)/2,behavior:reduce?'auto':'smooth'})}
    var raf=0;v.addEventListener('scroll',function(){cancelAnimationFrame(raf);raf=requestAnimationFrame(upd)},{passive:true});
    if(prev)prev.addEventListener('click',function(){go(idx()-1)});if(next)next.addEventListener('click',function(){go(idx()+1)});
    v.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){go(idx()+1);e.preventDefault()}else if(e.key==='ArrowLeft'){go(idx()-1);e.preventDefault()}});
    upd();
  });

  /* ---------- ampliar: tocar, doble toque, pellizcar, atrás ---------- */
  var lb=null,lastFocus=null,tapT=0,tapX=0,tapY=0;
  function build(){
    if(lb)return lb;
    lb=document.createElement('dialog');lb.className='d-lightbox';lb.setAttribute('aria-label',T.lb);
    lb.innerHTML='<div class="d-lightbox__bar"><span class="d-lightbox__cap"></span><button type="button" class="d-iconbtn d-st" data-lb="zoom" aria-label="'+T.zoom+'">'+ICON.zoom+'</button><button type="button" class="d-iconbtn d-st" data-lb="close" aria-label="'+T.close+'">'+ICON.close+'</button></div><div class="d-lightbox__scroll is-fit" tabindex="0" role="region" aria-label="'+T.region+'"><img alt=""></div><div class="d-lightbox__hint">'+T.hint+'</div>';
    document.body.appendChild(lb);
    var sc=lb.querySelector('.d-lightbox__scroll'),im=lb.querySelector('img');
    function toggle(x,y){var full=sc.classList.contains('is-fit');var r=im.getBoundingClientRect();var fx=(x-r.left)/r.width,fy=(y-r.top)/r.height;
      sc.classList.toggle('is-fit',!full);sc.classList.toggle('is-full',full);
      if(full){var r2=im.getBoundingClientRect();sc.scrollLeft+=r2.left+fx*r2.width-x;sc.scrollTop+=r2.top+fy*r2.height-y}}
    lb._toggle=toggle;
    lb.addEventListener('click',function(e){var b=e.target.closest('[data-lb]');if(!b)return;if(b.dataset.lb==='close')lb.close();else{var r=sc.getBoundingClientRect();toggle(r.left+r.width/2,r.top+r.height/2)}});
    im.addEventListener('dblclick',function(e){toggle(e.clientX,e.clientY)});
    im.addEventListener('touchend',function(e){var t=e.changedTouches[0],n=Date.now();if(e.touches.length)return;if(n-tapT<320&&Math.abs(t.clientX-tapX)<30&&Math.abs(t.clientY-tapY)<30){toggle(t.clientX,t.clientY);e.preventDefault();tapT=0}else{tapT=n;tapX=t.clientX;tapY=t.clientY}},{passive:false});
    lb.addEventListener('close',function(){if(history.state&&history.state.dlb)history.back();if(lastFocus&&lastFocus.focus)lastFocus.focus()});
    lb.addEventListener('keydown',function(e){if(e.key==='+'||e.key==='='||e.key==='-'){var r=sc.getBoundingClientRect();toggle(r.left+r.width/2,r.top+r.height/2)}});
    window.addEventListener('popstate',function(){if(lb.open){lb.close()}});
    return lb;
  }
  function openLb(src,alt,cap,from){
    var d=build();lastFocus=from||document.activeElement;
    var sc=d.querySelector('.d-lightbox__scroll'),im=d.querySelector('img');sc.classList.add('is-fit');sc.classList.remove('is-full');
    im.src=src;im.alt=alt||'';d.querySelector('.d-lightbox__cap').textContent=cap||'';
    history.pushState({dlb:1},'');d.showModal();sc.scrollTop=0;sc.scrollLeft=0;sc.focus();
  }
  q('[data-zoom]').forEach(function(f){
    var img=f.querySelector('img'),cap=f.querySelector('figcaption'),full=f.getAttribute('data-zoom')||img.src;
    var b=document.createElement('button');b.type='button';b.className='d-zoombtn d-iconbtn d-st';b.setAttribute('aria-label',T.open);b.innerHTML=ICON.zoom;f.appendChild(b);
    function go(e){e.preventDefault();openLb(full,img.alt,cap?cap.textContent:'',b)}
    b.addEventListener('click',go);img.addEventListener('click',go);
  });

  /* ---------- mantener presionado: la fuente de una cifra ---------- */
  var RING='<svg viewBox="-10 -6 180 204" aria-hidden="true"><path class="t" pathLength="100" d="M0 12 H67 A85 85 0 0 1 67 182 H0"/><path class="f" pathLength="100" d="M0 12 H67 A85 85 0 0 1 67 182 H0"/></svg>';
  var openPop=null;
  function closePop(){if(openPop){openPop.remove();openPop=null}}
  q('[data-hold]').forEach(function(el){
    el.classList.add('d-hold');el.setAttribute('tabindex','0');el.setAttribute('role','button');el.setAttribute('aria-label',(el.textContent||'').replace(/\s+/g,' ').trim()+T.hold);
    var ring=document.createElement('span');ring.className='d-hold__ring';ring.innerHTML=RING;el.appendChild(ring);
    var t=0;
    function start(){closePop();el.classList.add('is-holding');clearTimeout(t);t=setTimeout(show,600)}
    function cancel(){clearTimeout(t);el.classList.remove('is-holding')}
    function show(){el.classList.remove('is-holding');closePop();var p=document.createElement('div');p.className='d-hold__pop';p.setAttribute('role','status');
      var parts=(el.getAttribute('data-hold')||'').split('|');p.innerHTML='<b>'+(parts[1]||T.src)+'</b>'+(parts[0]||'');el.appendChild(p);openPop=p;if(navigator.vibrate)navigator.vibrate(10);setTimeout(function(){if(openPop===p)closePop()},5000)}
    el.addEventListener('pointerdown',function(e){if(e.button>0)return;start()});
    ['pointerup','pointerleave','pointercancel'].forEach(function(n){el.addEventListener(n,cancel)});
    el.addEventListener('keydown',function(e){if((e.key==='Enter'||e.key===' ')&&!e.repeat){e.preventDefault();start()}});
    el.addEventListener('keyup',function(e){if(e.key==='Enter'||e.key===' ')cancel()});
    el.addEventListener('blur',cancel);
  });
  document.addEventListener('pointerdown',function(e){if(openPop&&!openPop.parentNode.contains(e.target))closePop()});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closePop()});

  /* ---------- arrastrar: antes y después ---------- */
  q('.d-ba').forEach(function(b){
    var r=b.querySelector('input[type="range"]'),max=+b.getAttribute('data-max')||30,rows=q('[data-a]',b);
    function upd(){var k=+r.value/100;r.style.setProperty('--v',r.value+'%');rows.forEach(function(row){var a=+row.dataset.a,v=+row.dataset.b,x=a+(v-a)*k;row.querySelector('i').style.width=(x/max*100)+'%';row.querySelector('.d-ba__val').textContent=Math.round(x)});
      r.setAttribute('aria-valuetext',k<.03?T.before:k>.97?T.after:T.between)}
    r.addEventListener('input',upd);upd();
  });
})();
