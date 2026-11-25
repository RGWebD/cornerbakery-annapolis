/* The Corner Bakery — interactions (RGWebD) */
(function(){
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = (s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];

/* ---------- loader (home only, once per session) ---------- */
const ld=$('.loader');
if(ld){
  let seen=false; try{seen=sessionStorage.getItem('cb-ld')}catch(e){}
  if(RM||seen){ld.classList.add('gone')}
  else{
    try{sessionStorage.setItem('cb-ld','1')}catch(e){}
    const go=()=>{ld.classList.add('done');setTimeout(()=>ld.classList.add('gone'),1000)};
    setTimeout(go,1250);
  }
}

/* ---------- hours / live badge (America/New_York) ---------- */
const HOURS={0:[6,20],1:[7,21],2:[7,21],3:[7,21],4:[7,21],5:[7,21],6:[6,21]};
const HOLIDAY={'2026-11-26':'Thanksgiving — our flyer says open all night; hours may differ','2026-11-27':'Black Friday — hours may differ'};
const DAYS=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
function ny(){
  const p=Object.fromEntries(new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hour12:false,weekday:'short'}).formatToParts(new Date()).map(x=>[x.type,x.value]));
  const wd={Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6}[p.weekday];
  let h=+p.hour; if(h===24)h=0;
  return {wd,h,m:+p.minute,date:`${p.year}-${p.month}-${p.day}`};
}
const fmt=h=>{const ap=h>=12?'PM':'AM';const x=h%12||12;return x+' '+ap};
function status(){
  const t=ny(),[o,c]=HOURS[t.wd],now=t.h+t.m/60;
  if(HOLIDAY[t.date]) return {cls:'holiday-mode',txt:t.date==='2026-11-26'?'Thanksgiving · open late (call to confirm)':'Holiday hours may vary · call ahead',wd:t.wd,date:t.date};
  if(now>=o&&now<c) return {cls:'open',txt:`Open now · until ${fmt(c)}`,wd:t.wd,date:t.date};
  if(now<o) return {cls:'closed',txt:`Closed · opens ${fmt(o)} today`,wd:t.wd,date:t.date};
  const n=(t.wd+1)%7; return {cls:'closed',txt:`Closed · opens ${fmt(HOURS[n][0])} tomorrow`,wd:t.wd,date:t.date};
}
function paint(){
  const s=status();
  $$('.live').forEach(el=>{el.classList.remove('open','closed','holiday-mode');el.classList.add(s.cls);const t=el.querySelector('.lt');if(t)t.textContent=s.txt});
  $$('.hours tr[data-d]').forEach(r=>r.classList.toggle('today',+r.dataset.d===s.wd));
  const hs=$('.holiday'); if(hs){ const end='2026-11-28'; let closed=false; try{closed=sessionStorage.getItem('cb-hol')}catch(e){} hs.hidden = !(s.date<end) || !!closed; }
}
paint(); setInterval(paint,60000);
const hx=$('.holiday button'); if(hx) hx.addEventListener('click',()=>{$('.holiday').hidden=true;try{sessionStorage.setItem('cb-hol','1')}catch(e){}});

/* ---------- nav, drawer ---------- */
const nav=$('.nav'), bar=$('.progress'), mbar=$('.mbar');
const burger=$('.burger'), drawer=$('.drawer');
if(burger){
  burger.addEventListener('click',()=>{
    const o=burger.getAttribute('aria-expanded')!=='true';
    burger.setAttribute('aria-expanded',o); drawer.classList.toggle('open',o); drawer.setAttribute('aria-hidden',!o);
    document.body.style.overflow=o?'hidden':'';
    if(o) setTimeout(()=>drawer.querySelector('a').focus(),300);
  });
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&drawer.classList.contains('open')){burger.click();burger.focus()}});
  $$('a',drawer).forEach(a=>a.addEventListener('click',()=>{if(drawer.classList.contains('open'))burger.click()}));
}

/* ---------- scroll: progress, nav, mbar, parallax ---------- */
const par=$$('[data-speed]');
let ticking=false;
function onScroll(){
  const y=scrollY, h=document.documentElement.scrollHeight-innerHeight;
  if(bar) bar.style.transform=`scaleX(${h>0?y/h:0})`;
  if(nav) nav.classList.toggle('scrolled',y>20);
  if(mbar) mbar.classList.toggle('show',y>innerHeight*.5);
  if(!RM) par.forEach(el=>{const r=el.getBoundingClientRect();const c=Math.max(-innerHeight,Math.min(innerHeight,r.top+r.height/2-innerHeight/2));el.style.transform=`translate3d(0,${(-c*parseFloat(el.dataset.speed)).toFixed(1)}px,0)`});
  ticking=false;
}
addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(onScroll);ticking=true}},{passive:true});
onScroll();

/* ---------- split text ---------- */
$$('.split').forEach(el=>{
  const walk=n=>{[...n.childNodes].forEach(ch=>{
    if(ch.nodeType===3){const parts=ch.textContent.split(/(\s+)/);const f=document.createDocumentFragment();
      parts.forEach(p=>{if(!p)return; if(/^\s+$/.test(p)){f.appendChild(document.createTextNode(p));return}
        const w=document.createElement('span');w.className='w';const i=document.createElement('span');i.textContent=p;w.appendChild(i);f.appendChild(w)});
      ch.replaceWith(f)}
    else if(ch.nodeType===1&&!ch.classList.contains('w')){ if(ch.tagName==='BR')return; const w=document.createElement('span');w.className='w';const i=document.createElement('span');ch.replaceWith(w);i.appendChild(ch);w.appendChild(i)}
  })};
  walk(el);
  $$('.w>span',el).forEach((s,i)=>s.style.transitionDelay=(i*0.06+ (ld&&!ld.classList.contains('gone')?1.3:0.1))+'s');
});

/* ---------- reveals + counters ---------- */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -6% 0px'});
$$('.rv,.split').forEach(el=>io.observe(el));
function count(el){
  const to=parseFloat(el.dataset.to),d=1600,t0=performance.now();
  if(RM){el.textContent=to;return}
  const step=t=>{const p=Math.min(1,(t-t0)/d),e=1-Math.pow(1-p,3);el.textContent=Math.round(to*e);if(p<1)requestAnimationFrame(step);else el.textContent=to};
  requestAnimationFrame(step);
}
const cio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){count(e.target);cio.unobserve(e.target)}}),{threshold:.4});
$$('[data-to]').forEach(el=>cio.observe(el));

/* ---------- tilt + magnetic ---------- */
const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
if(fine&&!RM){
  $$('.tilt').forEach(c=>{
    c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.transform=`perspective(900px) rotateY(${x*9}deg) rotateX(${-y*9}deg) translateY(-6px)`});
    c.addEventListener('pointerleave',()=>c.style.transform='');
  });
  $$('.mag').forEach(b=>{
    b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.25}px,${(e.clientY-r.top-r.height/2)*.35}px)`});
    b.addEventListener('pointerleave',()=>b.style.transform='');
  });
}

/* ---------- hotspots ---------- */
$$('.spot-stage').forEach(st=>{
  const pins=$$('.pin',st);
  const close=()=>pins.forEach(p=>{p.setAttribute('aria-expanded','false');$('#'+p.getAttribute('aria-controls')).hidden=true});
  pins.forEach(p=>p.addEventListener('click',e=>{e.stopPropagation();const open=p.getAttribute('aria-expanded')==='true';close();if(!open){p.setAttribute('aria-expanded','true');$('#'+p.getAttribute('aria-controls')).hidden=false}}));
  document.addEventListener('click',close);
  document.addEventListener('keydown',e=>{if(e.key==='Escape')close()});
});

/* ---------- reviews carousel ---------- */
$$('.carousel').forEach(car=>{
  const tr=$('.track',car),sl=$$('.slide',car),dots=$('.dots',car);let i=0,timer;
  sl.forEach((s,k)=>{const b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Show review '+(k+1));b.addEventListener('click',()=>go(k));dots.appendChild(b)});
  function go(k){i=(k+sl.length)%sl.length;tr.style.transform=`translateX(${-100*i}%)`;sl.forEach((s,n)=>{s.setAttribute('aria-hidden',n!==i);s.inert=n!==i});$$('button',dots).forEach((b,n)=>b.setAttribute('aria-current',n===i))}
  $('.prev',car).addEventListener('click',()=>go(i-1));$('.next',car).addEventListener('click',()=>go(i+1));
  const play=()=>{if(RM)return;stop();timer=setInterval(()=>go(i+1),6500)},stop=()=>clearInterval(timer);
  car.addEventListener('mouseenter',stop);car.addEventListener('mouseleave',play);car.addEventListener('focusin',stop);car.addEventListener('focusout',play);
  let sx=null;tr.addEventListener('touchstart',e=>{sx=e.touches[0].clientX},{passive:true});tr.addEventListener('touchend',e=>{if(sx===null)return;const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)go(i+(dx<0?1:-1));sx=null});
  go(0);play();
});

/* ---------- draggable gallery + lightbox ---------- */
const gal=$('.gallery');
if(gal){
  let down=false,sx=0,sl=0,moved=0;
  gal.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;moved=0;sx=e.clientX;sl=gal.scrollLeft;gal.classList.add('drag')});
  addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-sx;moved=Math.max(moved,Math.abs(dx));gal.scrollLeft=sl-dx});
  addEventListener('pointerup',()=>{down=false;gal.classList.remove('drag')});
  gal.addEventListener('click',e=>{if(moved>6){e.preventDefault();e.stopPropagation();moved=0}},true);
  const step=()=>gal.clientWidth*.7;
  const pb=$('.gal-prev'),nb=$('.gal-next');
  if(pb)pb.addEventListener('click',()=>gal.scrollBy({left:-step(),behavior:RM?'auto':'smooth'}));
  if(nb)nb.addEventListener('click',()=>gal.scrollBy({left:step(),behavior:RM?'auto':'smooth'}));
  const items=$$('.gi',gal),box=$('.cbx'),img=$('img',box),cap=$('.cbx-cap',box);let cur=0,last=null;
  const show=k=>{cur=(k+items.length)%items.length;const it=items[cur];img.src=it.dataset.full;img.alt=it.querySelector('img').alt;cap.textContent=it.querySelector('img').alt+'  ·  '+(cur+1)+' / '+items.length};
  const open=k=>{last=document.activeElement;show(k);box.classList.add('open');box.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';$('.cbx-x',box).focus()};
  const close=()=>{box.classList.remove('open');box.setAttribute('aria-hidden','true');document.body.style.overflow='';if(last)last.focus()};
  items.forEach((it,k)=>it.addEventListener('click',()=>open(k)));
  $('.cbx-x',box).addEventListener('click',close);$('.cbx-p',box).addEventListener('click',()=>show(cur-1));$('.cbx-n',box).addEventListener('click',()=>show(cur+1));
  box.addEventListener('click',e=>{if(e.target===box)close()});
  document.addEventListener('keydown',e=>{if(!box.classList.contains('open'))return;
    if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(cur-1);if(e.key==='ArrowRight')show(cur+1);
    if(e.key==='Tab'){const f=$$('button',box);const a=f.indexOf(document.activeElement);e.preventDefault();f[(a+(e.shiftKey?-1:1)+f.length)%f.length].focus()}});
  let tx=null;box.addEventListener('touchstart',e=>{tx=e.touches[0].clientX},{passive:true});box.addEventListener('touchend',e=>{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;if(Math.abs(dx)>40)show(cur+(dx<0?1:-1));tx=null});
}

/* ---------- scroll-drawn timeline ---------- */
$$('.timeline').forEach(tl=>{
  const p=$('svg.tl path.draw',tl); if(!p)return;
  const svg=$('svg.tl',tl);
  const set=()=>{const h=tl.offsetHeight;svg.setAttribute('viewBox',`0 0 24 ${h}`);p.setAttribute('d',`M12 0 V${h}`);$('svg.tl path.base',tl).setAttribute('d',`M12 0 V${h}`);p.style.strokeDasharray=h;return h};
  let H=set(); addEventListener('resize',()=>{H=set()});
  const draw=()=>{const r=tl.getBoundingClientRect();const pr=Math.min(1,Math.max(0,(innerHeight*.75-r.top)/r.height));p.style.strokeDashoffset=RM?0:H*(1-pr)};
  addEventListener('scroll',()=>requestAnimationFrame(draw),{passive:true});draw();
});

/* ---------- cake order mailto ---------- */
const form=$('#cake-form');
if(form){form.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(form);
  const lines=[`Name: ${d.get('name')}`,`Phone: ${d.get('phone')}`,`Date needed: ${d.get('date')}`,`Occasion: ${d.get('occasion')}`,`Guests / size: ${d.get('size')}`,`Flavor ideas: ${d.get('flavor')}`,'',`Design notes: ${d.get('notes')}`,'','(I can attach an inspiration photo to this email.)'];
  location.href='mailto:bakerygalleria@icloud.com?subject='+encodeURIComponent('Custom cake request – '+(d.get('occasion')||'celebration')+' – '+(d.get('date')||''))+'&body='+encodeURIComponent(lines.join('\n'));
})}

/* ---------- demo pill ---------- */
const demo=$('.demo');
if(demo){let h=false;try{h=sessionStorage.getItem('cb-demo')}catch(e){} if(h)demo.hidden=true;
  $('button',demo).addEventListener('click',()=>{demo.hidden=true;try{sessionStorage.setItem('cb-demo','1')}catch(e){}})}

$$('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());
})();
