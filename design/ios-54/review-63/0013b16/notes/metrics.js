() => { const r=e=>{if(!e)return null;const b=e.getBoundingClientRect();return [Math.round(b.x*10)/10,Math.round(b.y*10)/10,Math.round(b.width*10)/10,Math.round(b.height*10)/10]};
 const s=document.querySelector('.sheet'); if(!s) return null; const sr=s.getBoundingClientRect();
 const rel=e=>{if(!e)return null;const b=e.getBoundingClientRect();return [Math.round((b.x-sr.x)*10)/10,Math.round((b.y-sr.y)*10)/10,Math.round(b.width*10)/10,Math.round(b.height*10)/10]};
 const cs=(e,ps)=>e?ps.map(p=>getComputedStyle(e)[p]).join(' | '):null;
 const h2=s.querySelector('h2');
 return {sheet:[sr.width,sr.height], radius:getComputedStyle(s).borderRadius, shadow:getComputedStyle(s).boxShadow.slice(0,60),
  h2:cs(h2,['fontFamily','fontSize','fontWeight','lineHeight','letterSpacing']), h2rel:rel(h2),
  sub:rel(s.querySelector('.sh-head p')), subcs:cs(s.querySelector('.sh-head p'),['fontSize','lineHeight','color']),
  head:rel(s.querySelector('.sh-head')), headpad:cs(s.querySelector('.sh-head'),['paddingTop','paddingLeft','paddingBottom']),
  closex:rel(s.querySelector('.closex')), foot:rel(s.querySelector('.sh-foot')), footpad:cs(s.querySelector('.sh-foot'),['paddingTop','paddingLeft']),
  btns:[...s.querySelectorAll('.btn')].slice(0,6).map(b=>({t:b.textContent.trim().slice(0,22),r:rel(b),pad:getComputedStyle(b).padding,fs:getComputedStyle(b).fontSize,fw:getComputedStyle(b).fontWeight})),
  grps:[...s.querySelectorAll('.grp')].slice(0,4).map(g=>rel(g)),
  gn:cs(s.querySelector('.gn'),['fontSize','fontWeight']), chg:cs(s.querySelector('.chg'),['fontSize','lineHeight']), meta:cs(s.querySelector('.meta'),['fontSize','fontWeight']),
  err:rel(s.querySelector('.err')), errcs:cs(s.querySelector('.err'),['fontSize','fontWeight','padding','borderRadius','backgroundColor','color']),
  errbtn:rel(s.querySelector('.err .btn')), errbtncs:cs(s.querySelector('.err .btn'),['textDecorationLine','color'])};
}
