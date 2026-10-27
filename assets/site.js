/* Resalta en el riel la sección que se está leyendo. Sin dependencias; sin el script el sitio funciona igual. */
(function(){
  var links=[].slice.call(document.querySelectorAll('.s-rail .d-raili'));
  if(!links.length||!('IntersectionObserver' in window))return;
  var secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))}).filter(Boolean);
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('is-active',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-15% 0px -75% 0px'});
  secs.forEach(function(s){io.observe(s)});
  document.querySelectorAll('.s-menu a').forEach(function(a){a.addEventListener('click',function(){document.querySelector('.s-menu').removeAttribute('open')})});
})();

/* Prototipo clicable de las pantallas: zonas activas, flechas, teclado y espera automática */
(function(){
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.s-proto').forEach(function(root){
    var frames=[].slice.call(root.querySelectorAll('.s-proto__frame')),caps=[].slice.call(root.querySelectorAll('.s-proto__cap')),dots=[].slice.call(root.querySelectorAll('.s-proto__dots i')),
        count=root.querySelector('.s-proto__count'),prev=root.querySelector('[data-p="prev"]'),next=root.querySelector('[data-p="next"]'),i=0,timer=0;
    function show(n){
      i=Math.max(0,Math.min(frames.length-1,n));clearTimeout(timer);
      frames.forEach(function(f,k){f.classList.toggle('is-on',k===i)});caps.forEach(function(c,k){c.classList.toggle('is-on',k===i)});
      dots.forEach(function(d,k){d.classList.toggle('is-on',k<=i)});if(count)count.textContent=(i+1)+' / '+frames.length;
      if(prev)prev.disabled=i===0;if(next)next.disabled=i===frames.length-1;
      var f=frames[i],fill=f.querySelector('.s-proto__fill'),auto=parseInt(f.getAttribute('data-auto')||'0',10);
      if(fill){fill.style.animation='none';void fill.offsetWidth;fill.style.animation=reduce?'none':'s-proto-fill '+auto+'ms linear forwards'}
      if(auto&&!reduce)timer=setTimeout(function(){if(frames[i]===f)show(i+1)},auto);
    }
    root.addEventListener('click',function(e){
      var b=e.target.closest('button');if(!b||!root.contains(b))return;
      var p=b.getAttribute('data-p'),a=b.getAttribute('data-act');
      if(p==='next')show(i+1);else if(p==='prev')show(i-1);else if(p==='reset')show(0);
      else if(a==='next')show(i+1);else if(a==='prev')show(i-1);else if(a==='reset')show(0);else if(a==='toggle')b.classList.toggle('is-on');
    });
    root.addEventListener('keydown',function(e){if(e.target!==root)return;if(e.key==='ArrowRight'){show(i+1);e.preventDefault()}else if(e.key==='ArrowLeft'){show(i-1);e.preventDefault()}});
    show(0);
  });
})();

/* Hojas modales de reconocimientos: <dialog> nativo (foco atrapado, Esc cierra); se cierra también con el fondo, "Listo" o arrastrando hacia abajo */
(function(){
  if(!document.querySelector('dialog.s-sheet'))return;
  function lock(on){document.body.classList.toggle('s-lock',on)}
  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-sheet]');
    if(t){var d=document.getElementById(t.getAttribute('data-sheet'));if(d&&d.showModal){d.showModal();lock(true)}return}
    var c=e.target.closest('[data-close]');if(c){var dd=c.closest('dialog');if(dd)dd.close();return}
    if(e.target.tagName==='DIALOG'&&e.target.classList.contains('s-sheet')){var r=e.target.getBoundingClientRect();if(e.clientY<r.top||e.clientY>r.bottom||e.clientX<r.left||e.clientX>r.right)e.target.close()}
  });
  document.querySelectorAll('dialog.s-sheet').forEach(function(d){
    d.addEventListener('close',function(){lock(false)});
    var g=d.querySelector('.s-sheet__grab'),y0=null;
    if(g){
      g.addEventListener('touchstart',function(e){y0=e.touches[0].clientY},{passive:true});
      g.addEventListener('touchmove',function(e){if(y0===null)return;var dy=e.touches[0].clientY-y0;if(dy>0)d.style.transform='translateY('+dy+'px)'},{passive:true});
      g.addEventListener('touchend',function(e){var dy=e.changedTouches[0].clientY-y0;y0=null;d.style.transform='';if(dy>80)d.close()});
    }
  });
})();

/* Componentes incrustados: el iframe toma el alto real de su contenido (las medidas fijas de CSS quedan como respaldo sin JS) */
(function(){
  document.querySelectorAll('iframe.s-embed').forEach(function(f){
    function fit(){
      try{
        var d=f.contentDocument;if(!d||!d.body)return;
        var h=Math.ceil(d.body.getBoundingClientRect().height+d.body.getBoundingClientRect().top);
        if(h>200)f.style.height=h+'px';
      }catch(e){}
    }
    f.addEventListener('load',function(){
      fit();
      try{if('ResizeObserver' in window)new ResizeObserver(fit).observe(f.contentDocument.body)}catch(e){}
      try{f.contentWindow.addEventListener('resize',fit)}catch(e){}
    });
    if(f.contentDocument&&f.contentDocument.readyState==='complete')fit();
  });
})();
