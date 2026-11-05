/* Medición (Medición, 1/11/2026). Archivo aparte (assets/medicion.js): lo pide el arranque de site.js después de la carga.
   Escrito dentro de la página, el celular de Lighthouse pintaba la frase de la portada 0,3 s más tarde y bajaba a 99.
   GA4 y Clarity se cargan solo después de «Aceptar»; sin aceptar no se mide nada. Los ID salen de <meta name="didi-ga4"> y <meta name="didi-clarity">.
   Contrato como el de Kol: window.didiMedicion = {estado(), cuandoAcepte(fn), reabrir()} y el evento de documento «didi:medicion» con 'si' o 'no'.
   Origen de la visita como en Kol: se guarda en el navegador por 30 días y solo con «Aceptar»; la campaña pisa lo anterior y una visita sin campaña no pisa una campaña. */
(function(){
  var d=document,h=d.documentElement;
  function meta(n){var m=d.querySelector('meta[name="'+n+'"]');return m?m.content:''}
  var GA=meta('didi-ga4'),CL=meta('didi-clarity');if(!GA&&!CL)return;
  var KEY='didi_medicion_v1',OKEY='didi_origen_v1',IKEY='didi_interno',DIAS=30;
  function get(k){try{return localStorage.getItem(k)}catch(e){return null}}
  function put(k,v){try{if(v===null)localStorage.removeItem(k);else localStorage.setItem(k,v)}catch(e){}}
  var lang=(h.lang||'es').slice(0,2),path=location.pathname,listo=false,fns=[];
  if(/[?&]interno=1/.test(location.search))put(IKEY,'1');else if(/[?&]interno=0/.test(location.search))put(IKEY,null);
  var interno=get(IKEY)==='1';

  /* Qué página es */
  var m=path.match(/\/casos\/([\w-]+)\.html/),caso=m?m[1]:'';
  var tipo=caso?'caso':/sobre-mi\.html/.test(path)?'sobre-mi':/contacto\.html/.test(path)?'contacto':/privacidad\.html/.test(path)?'privacidad':/marcas\/guidelines\.html/.test(path)?'guidelines':/marcas\//.test(path)?'marcas':'portada';
  var tono=(d.querySelector('.s-case')||h).style.getPropertyValue('--tone');
  var trabajo={accion:'campañas',nav:'producto',atencion:'ux',ok:'automatización',dato:'académico'}[(tono.match(/--d-(\w+)/)||[])[1]]||'';

  /* De dónde vino esta visita (en memoria: se guarda solo con «Aceptar») */
  var q=new URLSearchParams(location.search);
  function host(u){try{return new URL(u).hostname.replace(/^www\./,'')}catch(e){return ''}}
  function propio(r){return r===location.hostname.replace(/^www\./,'')||/(^|\.)malquidebora\.com$|^deboramalqui\.github\.io$/.test(r)}
  function etiqueta(o){
    if(o.utm_source)return o.utm_source+' / '+(o.utm_medium||'(sin medio)');
    if(o.gclid)return 'google / cpc';
    if(o.fbclid)return 'meta / social';
    var r=o.ref||'';if(!r)return 'directo';
    var ia=r.match(/chatgpt|openai|perplexity|claude|gemini|copilot|deepseek|you\.com/);
    if(ia)return (ia[0]==='openai'?'chatgpt':ia[0].replace('.com',''))+' / ia';
    var bus=r.match(/google|bing|duckduckgo|yahoo|yandex|ecosia|baidu/);if(bus)return bus[0]+' / orgánico';
    if(/linkedin|lnkd\.in/.test(r))return 'linkedin / social';
    var red=r.match(/facebook|instagram|threads|twitter|^t\.co$|^x\.com$|youtube|pinterest|behance|dribbble/);if(red)return red[0].replace(/^t\.co$|^x\.com$/,'x')+' / social';
    if(/marketingmedido/.test(r))return 'medido / referencia';
    return r+' / referencia';
  }
  var ahora=(function(){
    var o={},ref=host(d.referrer);
    ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','gclid','fbclid'].forEach(function(k){var v=q.get(k);if(v)o[k]=v.slice(0,100)});
    var campana=!!(o.utm_source||o.gclid||o.fbclid);
    if(!campana&&ref&&propio(ref))return null;   // navegación dentro del sitio: no es un origen nuevo
    o.entrada=path;if(ref)o.ref=ref;o.etiqueta=etiqueta(o);o.campana=campana;o.t=Date.now();return o;
  })();
  function guardado(){
    try{var o=JSON.parse(get(OKEY)||'null');if(o&&Date.now()-o.t<DIAS*864e5)return o}catch(e){}
    return null;
  }
  function elegir(g){   // como Kol: la campaña pisa todo; una visita sin campaña no pisa una campaña; entrar directo no pisa nada
    if(!ahora)return g;if(ahora.campana||!g)return ahora;
    if(g.campana||ahora.etiqueta==='directo')return g;
    return ahora;
  }
  function guardarOrigen(){var o=elegir(guardado());if(o&&o===ahora)put(OKEY,JSON.stringify(ahora))}
  function textoOrigen(o){return o?o.etiqueta+(o.utm_campaign?' · '+o.utm_campaign:''):'(sin dato)'}

  /* El formulario lleva el origen como campo oculto: llega en el mail, acepte o no (no guarda nada en el navegador) */
  var oi=d.querySelector('form.s-form input[name="origen"]');
  if(oi)oi.value=textoOrigen(elegir(get(KEY)==='si'?guardado():null));

  /* Eventos: sin «Aceptar» no sale nada */
  function ev(n,p){
    if(!listo)return;p=p||{};p.idioma=lang;
    if(GA&&window.gtag)gtag('event',n,p);
    if(CL&&window.clarity)clarity('event',n);
  }
  function cargar(src){var s=d.createElement('script');s.async=true;s.src=src;d.head.appendChild(s)}
  function empezar(){
    if(listo)return;listo=true;guardarOrigen();
    var g=guardado();
    if(GA){
      window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};
      gtag('js',new Date());
      var cfg={idioma:lang,tipo_pagina:tipo,user_properties:{idioma_sitio:lang,origen:g?g.etiqueta:'(sin dato)'}};
      if(caso)cfg.caso=caso;
      if(interno)cfg.traffic_type='internal';
      gtag('config',GA,cfg);   // los datos fijos van en config: «set» no viaja (prueba de Medido)
      cargar('https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(GA));
    }
    if(CL){
      window.clarity=window.clarity||function(){(clarity.q=clarity.q||[]).push(arguments)};
      clarity('consentv2',{ad_Storage:'denied',analytics_Storage:'granted'});
      clarity('set','idioma',lang);if(interno)clarity('set','interno','1');
      cargar('https://www.clarity.ms/tag/'+encodeURIComponent(CL));
    }
    if(caso){
      var r=host(d.referrer),rp='';try{rp=new URL(d.referrer).pathname}catch(e){}
      var desde=!d.referrer?'directo':!propio(r)?'otro sitio':/\/casos\//.test(rp)?'siguiente caso':/sobre-mi/.test(rp)?'sobre-mi':/marcas/.test(rp)?'marcas':'portada';
      ev('ver_caso',{caso:caso,tipo_trabajo:trabajo,desde:desde});
    }
    fns.splice(0).forEach(function(fn){try{fn()}catch(e){}});
  }
  function borrarCookies(){
    var dom=location.hostname.replace(/^www\./,'');
    d.cookie.split(';').forEach(function(c){
      var n=c.split('=')[0].trim();
      if(/^(_ga|_gid|_cl|CLID|MUID)/.test(n))['',';domain='+location.hostname,';domain=.'+dom].forEach(function(x){d.cookie=n+'=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/'+x});
    });
  }
  window.didiMedicion={
    estado:function(){return get(KEY)},
    cuandoAcepte:function(fn){if(listo)fn();else fns.push(fn)},
    reabrir:function(){h.classList.remove('ck-ok');var b=d.querySelector('#s-ck [data-ck]');if(b)b.focus()}
  };

  /* El aviso */
  d.addEventListener('click',function(e){
    var b=e.target.closest('[data-ck]');
    if(b){
      var v=b.getAttribute('data-ck'),antes=get(KEY);
      put(KEY,v);h.classList.add('ck-ok');
      try{d.dispatchEvent(new CustomEvent('didi:medicion',{detail:v}))}catch(x){}
      if(v==='si')empezar();
      else{put(OKEY,null);if(antes==='si'){borrarCookies();location.reload()}}   // si retira el «sí», la página se recarga y deja de medir
      return;
    }
    if(e.target.closest('[data-ck-abrir]')){didiMedicion.reabrir();return}
  });
  if(get(KEY)==='si')empezar();

  /* Clics */
  function donde(el){return el.closest('.s-head')?'barra':el.closest('.s-fab')?'boton flotante':el.closest('.s-foot')?'pie':el.closest('.s-cta-row')?'final del caso':tipo}
  d.addEventListener('click',function(e){
    if(!listo)return;
    var hoja=e.target.closest('[data-sheet]');if(hoja){ev('abrir_hoja',{hoja:hoja.getAttribute('data-sheet').replace(/^rec-/,'')});return}
    var libro=e.target.closest('[data-book]');if(libro){ev('abrir_manual',{manual:libro.getAttribute('data-book')});return}
    var a=e.target.closest('a[href]');if(!a)return;
    var u=a.href,hs=host(u),w=donde(a);
    if(/campaign-suite-demo/.test(u)){ev('abrir_demo',{demo:'campaign-suite',donde:w});return}
    if(/coupons-pwa-demo/.test(u)){ev('abrir_demo',{demo:'cupones-santo-tome',donde:w});return}
    if(/^mailto:/.test(u)){ev('clic_mail',{donde:w});return}
    if(/wa\.me|whatsapp/.test(hs)){ev('clic_whatsapp',{donde:w});return}
    if(/linkedin\.com/.test(hs)){ev('clic_linkedin',{donde:w});return}
    if(a.closest('.s-lang')){var al=(a.getAttribute('lang')||'').slice(0,2);if(al&&al!==lang)ev('cambiar_idioma',{de:lang,a:al});return}
    var arch=(u.split(/[?#]/)[0].match(/[^\/]+\.(pdf|vcf|zip)$/i)||[])[0];
    if(arch||a.hasAttribute('download')){arch=arch||'archivo';ev(/\.vcf$/i.test(arch)?'guardar_contacto':'descargar',{archivo:arch});return}
    if(/contacto\.html/.test(u)&&tipo!=='contacto'){ev('ir_a_contacto',{donde:w});return}
    if(hs&&!propio(hs)&&/^https?:/.test(u))ev('enlace_saliente',{destino:/marketingmedido/.test(hs)?'medido':hs,donde:w});
  },true);

  /* Hasta dónde baja: 25, 50, 75 y 100 %, una vez cada uno por página */
  var marcas=[25,50,75,100],raf=0;
  function medir(){
    raf=0;if(!listo)return;
    var alto=Math.max(d.documentElement.scrollHeight,1),pct=(scrollY+innerHeight)/alto*100;
    while(marcas.length&&pct>=(marcas[0]===100?99:marcas[0])){var p=marcas.shift(),o={porcentaje:p};if(caso)o.caso=caso;ev('profundidad',o)}
  }
  addEventListener('scroll',function(){if(!raf)raf=requestAnimationFrame(medir)},{passive:true});

  /* El formulario se envió bien (no el clic): .s-form__ok se muestra */
  var ok=d.querySelector('.s-form__ok'),avisado=false;
  function lead(){if(avisado||!listo||!ok||ok.hidden)return;avisado=true;ev('generate_lead',{forma:'formulario'})}
  if(ok){didiMedicion.cuandoAcepte(lead);new MutationObserver(lead).observe(ok,{attributes:true,attributeFilter:['hidden']})}
})();
