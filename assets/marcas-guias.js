(function(){var L=(document.documentElement.lang||"es").slice(0,2);var T={"es": {}, "en": {"Página": "Page", "de": "of", "Ir a": "Go to", "página": "page", "Hojear: página de 1 a": "Browse: page 1 to", "páginas": "pages", "pestañas": "tabs", "← Volver a la suite": "← Back to the suite"}, "he": {"Página": "עמוד", "de": "מתוך", "Ir a": "מעבר אל", "página": "עמוד", "Hojear: página de 1 a": "דפדוף: עמוד 1 עד", "páginas": "עמודים", "pestañas": "לשוניות", "← Volver a la suite": "← חזרה לסוויטה"}};window.__gt=function(s){return (T[L]||{})[s]||s};})();

(function(){
const BOOKS = JSON.parse(document.getElementById('books').textContent);
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = (s, r=document) => r.querySelector(s);
const reader = $('#reader'), sheet = $('#sheet'), book = $('#book'), tabsEl = $('#tabs'), chipsEl = $('#chips'), strip = $('#strip'), range = $('#range');
let B = null, idx = 0, busy = false, lastFocus = null;
const src = (p) => B.dir + String(p).padStart(3,'0') + '.webp';
function thumbPos(p, w){ const k = p-1, s = w / B.tw; return { size: `${B.cols*B.tw*s}px auto`, pos: `${-(k % B.cols)*B.tw*s}px ${-Math.floor(k / B.cols)*B.th*s}px` }; }
function chapterOf(p){ let c = B.chapters[0]; for (const ch of B.chapters) if (ch.p <= p) c = ch; return c; }
function isDark(hex){ const n=parseInt(hex.slice(1),16), r=n>>16&255, g=n>>8&255, b=n&255; return (0.299*r+0.587*g+0.114*b) > 170; }
function placeholder(el, p){ const t = thumbPos(p, el.clientWidth || 800); el.style.backgroundImage = `url(${B.dir}miniaturas.webp)`; el.style.backgroundSize = t.size; el.style.backgroundPosition = t.pos; }
function setSheet(p){ placeholder(sheet, p); const img = sheet.querySelector('img'); img.src = src(p); img.alt = `${__gt('Página')} ${p} ${__gt('de')} ${B.n}: ${chapterOf(p).t}`; preload(p); }
function preload(p){ const i = B.pages.indexOf(p); [1,2,-1].forEach(d => { const q = B.pages[i+d]; if (q){ const im = new Image(); im.src = src(q); } }); }
function stacks(){ const maxT = Math.min(34, 6 + B.n * 0.13), done = idx / Math.max(1, B.pages.length-1);
  $('#stack-r').style.width = Math.max(2, maxT * (1-done)) + 'px'; $('#stack-l').style.width = Math.max(idx ? 2 : 0, maxT * done) + 'px';
  book.style.setProperty('--rt', Math.max(2, maxT*(1-done)) + 'px'); }
function status(){ const p = B.pages[idx], ch = chapterOf(p);
  $('#st-page').textContent = `${__gt('Página')} ${p} ${__gt('de')} ${B.n}`; $('#st-ch').textContent = ch.t; range.value = idx;
  document.querySelectorAll('.tab,.chip').forEach(t => t.classList.toggle('is-on', +t.dataset.p === ch.p));
  const th = strip.children[idx]; strip.querySelectorAll('.is-on').forEach(x => x.classList.remove('is-on'));
  if (th){ th.classList.add('is-on'); const s = th.offsetLeft - strip.clientWidth/2 + th.clientWidth/2; strip.scrollTo({left: s, behavior: RM ? 'auto' : 'smooth'}); }
  const chip = chipsEl.querySelector('.is-on'); if (chip) chipsEl.scrollTo({left: chip.offsetLeft - 20, behavior: 'auto'});
  stacks(); }
function go(to, animate){
  to = Math.max(0, Math.min(B.pages.length-1, to)); if (to === idx || busy) { if (!busy && to === idx) status(); return; }
  const from = idx, fwd = to > from, step = Math.abs(to-from) === 1;
  if (!animate || RM || !step){ idx = to; setSheet(B.pages[idx]); status(); return; }
  busy = true;
  const leaf = document.createElement('div'); leaf.className = 'leaf';
  const pFront = fwd ? B.pages[from] : B.pages[to];
  leaf.innerHTML = `<div class="face"><img alt="" src="${src(pFront)}"></div><div class="face back"></div><div class="shade"></div>`;
  placeholder(leaf.firstChild, pFront);
  book.appendChild(leaf);
  if (fwd){ idx = to; setSheet(B.pages[idx]); }
  const kf = fwd ? [{transform:'rotateY(0deg)'},{transform:'rotateY(-180deg)'}] : [{transform:'rotateY(-180deg)'},{transform:'rotateY(0deg)'}];
  const a = leaf.animate(kf, {duration: 720, easing: 'cubic-bezier(.3,.1,.2,1)'});
  leaf.querySelector('.shade').animate([{opacity:0},{opacity:1,offset:.5},{opacity:0}], {duration: 720});
  a.onfinish = () => { leaf.remove(); if (!fwd){ idx = to; setSheet(B.pages[idx]); } busy = false; status(); };
  if (!fwd){ /* el destino aparece cuando la hoja termina de volver */ }
  status();
}
function build(b){
  B = b; idx = 0; reader.style.setProperty('--acc', B.accent);
  $('#r-name').textContent = `${B.title} · ${B.sub}`; $('#r-meta').textContent = `${B.n} ${__gt('páginas')} · ${B.chapters.length} ${__gt('pestañas')}` ;
  const nt = B.chapters.length; book.style.setProperty('--th', `calc((100% - ${(nt-1)*3}px) / ${nt})`);
  tabsEl.innerHTML = ''; chipsEl.innerHTML = '';
  B.chapters.forEach((ch, i) => {
    const num = (ch.t.match(/^([0-9.]+|Anexo)/)||[''])[0] || (i===0 ? '·' : '');
    const label = ch.t.replace(/^([0-9.]+\s*·?\s*)/, '');
    const t = document.createElement('button'); t.className = 'tab' + (isDark(ch.c) ? ' dark' : ''); t.style.setProperty('--c', ch.c); t.dataset.p = ch.p;
    t.innerHTML = `<span class="tn">${num || '•'}</span><span>${label}</span>`; t.setAttribute('aria-label', `${__gt('Ir a')} ${ch.t}, ${__gt('página')} ${ch.p}`);
    t.onclick = () => jumpTo(ch.p); tabsEl.appendChild(t);
    const c = document.createElement('button'); c.className = 'chip'; c.style.setProperty('--c', ch.c); c.dataset.p = ch.p; c.textContent = ch.t; c.onclick = () => jumpTo(ch.p); chipsEl.appendChild(c);
  });
  strip.innerHTML = '';
  B.pages.forEach((p, i) => { const t = document.createElement('button'); t.className = 'thumb'; t.setAttribute('aria-label', `${__gt('Página')} ${p}`);
    const tp = thumbPos(p, 96); t.style.backgroundImage = `url(${B.dir}miniaturas.webp)`; t.style.backgroundSize = tp.size; t.style.backgroundPosition = tp.pos;
    t.onclick = () => go(i, Math.abs(i-idx) === 1); strip.appendChild(t); });
  range.max = B.pages.length-1; range.value = 0; range.setAttribute('aria-label', `${__gt('Hojear: página de 1 a')} ${B.n}`);
  setSheet(B.pages[0]); status();
}
function jumpTo(p){ let i = B.pages.indexOf(p); if (i < 0) i = B.pages.findIndex(q => q > p); go(i, false); }
function open(id, fromEl){
  const b = BOOKS.find(x => x.id === id); if (!b) return; lastFocus = fromEl || document.activeElement;
  build(b); reader.classList.add('is-open'); document.body.style.overflow = 'hidden'; $('#r-close').focus();
  if (location.hash !== '#' + id) history.replaceState(null, '', '#' + id);
  if (!RM){ const h = $('#hint'); setTimeout(() => go(1, true), 380); h.classList.add('on'); setTimeout(() => h.classList.remove('on'), 2600); }
}
/* Dos flujos al cerrar: quien llegó desde Just for fun vuelve a la lista de guías; quien llegó desde la Campaign Suite (?desde=suite) vuelve a la suite. */
const DESDE = new URLSearchParams(location.search).get('desde');
if (DESDE === 'suite') { const c = $('#r-close'); if (c) c.textContent = __gt('← Volver a la suite'); }
function close(){
  if (DESDE === 'suite') { if (history.length > 1 && document.referrer) history.back(); else location.href = '../index.html'; return; }
  reader.classList.remove('is-open'); document.body.style.overflow = ''; history.replaceState(null, '', location.pathname); if (lastFocus) lastFocus.focus(); }
document.querySelectorAll('[data-book]').forEach(el => el.addEventListener('click', () => open(el.dataset.book, el)));
$('#r-close').onclick = close;
$('#prev').onclick = () => go(idx-1, true); $('#next').onclick = () => go(idx+1, true);
range.addEventListener('input', () => go(+range.value, false));
sheet.addEventListener('click', e => { const r = sheet.getBoundingClientRect(); go(idx + ((e.clientX - r.left) > r.width/2 ? 1 : -1), true); });
document.addEventListener('keydown', e => { if (!reader.classList.contains('is-open')) return;
  if (e.key === 'Escape') close(); else if (e.key === 'ArrowRight') go(idx+1, true); else if (e.key === 'ArrowLeft') go(idx-1, true);
  else if (e.key === 'Home') go(0, false); else if (e.key === 'End') go(B.pages.length-1, false);
  else if (e.key === 'PageDown' || e.key === 'PageUp'){ const p = B.pages[idx], cs = B.chapters.map(c => c.p); const n = e.key === 'PageDown' ? cs.find(c => c > p) : [...cs].reverse().find(c => c < chapterOf(p).p || (c < p && c !== chapterOf(p).p)); if (n) jumpTo(n); e.preventDefault(); } });
let sx = null; const stage = $('#stage');
stage.addEventListener('pointerdown', e => { sx = e.clientX; });
stage.addEventListener('pointerup', e => { if (sx === null) return; const dx = e.clientX - sx; sx = null; if (Math.abs(dx) > 50){ go(idx + (dx < 0 ? 1 : -1), true); e.preventDefault(); } });
const h = location.hash.slice(1); if (h && BOOKS.some(b => b.id === h)) open(h);
})();
