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
