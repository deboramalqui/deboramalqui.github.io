

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
