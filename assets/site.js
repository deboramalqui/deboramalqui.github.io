/* Resalta en el riel la sección que se está leyendo. Sin dependencias; sin el script el sitio funciona igual. */
(function(){
  var links=[].slice.call(document.querySelectorAll('.s-rail .d-raili'));
  if(!links.length||!('IntersectionObserver' in window))return;
  var secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))}).filter(Boolean);
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.toggle('is-active',a.getAttribute('href')==='#'+e.target.id)})}})},{rootMargin:'-15% 0px -75% 0px'});
  secs.forEach(function(s){io.observe(s)});
  document.querySelectorAll('.s-menu a').forEach(function(a){a.addEventListener('click',function(){document.querySelector('.s-menu').removeAttribute('open')})});
})();
