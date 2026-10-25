/* Riihimaen Keha-Ketut — automatic news cards, source /uutiset/ */
(function(){
 "use strict";
 if(window.__RKK_NEWS_MODULE_INITIALIZED)return;
 var mount=document.getElementById("rkk-news-slot");
 if(!mount)return;
 window.__RKK_NEWS_MODULE_INITIALIZED=true;

 // Central BoxerBase iframe resizer. Yhdistysavain may keep the old
 // fixed-height player block and strip inline scripts from that block.
 // Resizing is accepted only from our own actual iframe window.
 if(!window.__RKK_WIDGET_RESIZE_HOST_V2){
   window.__RKK_WIDGET_RESIZE_HOST_V2=true;
   window.addEventListener("message",function(event){
     if(event.origin!=="https://glesima.github.io" ||
        !event.data || event.data.type!=="RKK_WIDGET_HEIGHT")return;
     var h=Number(event.data.height);
     if(!Number.isFinite(h)||h<130||h>5000)return;
     var frames=document.querySelectorAll('iframe[src*="glesima.github.io/kehaketut-feed/widget.html"]');
     for(var i=0;i<frames.length;i++){
       var frame=frames[i];
       if(frame.contentWindow!==event.source)continue;
       try{
         var url=new URL(frame.src,document.baseURI);
         if(url.searchParams.get("view")!==event.data.view)continue;
       }catch(err){continue}
       frame.style.setProperty("height",Math.ceil(h)+"px","important");
       frame.style.setProperty("min-height","0px","important");
       frame.setAttribute("height",String(Math.ceil(h)));
       return;
     }
   });
   // If this script loads after a lazy iframe's initial resize event,
   // request a fresh measurement instead of leaving Yhdistysavain's old height.
   function requestMeasurements(){
     var frames=document.querySelectorAll('iframe[src*="glesima.github.io/kehaketut-feed/widget.html"]');
     for(var i=0;i<frames.length;i++){
       (function(frame){
         function ask(){
           try{if(frame.contentWindow)frame.contentWindow.postMessage({type:"RKK_REQUEST_HEIGHT"},"https://glesima.github.io")}catch(ex){}
         }
         frame.addEventListener("load",ask,{once:true});
         ask();
       })(frames[i]);
     }
   }
   requestMeasurements();
   if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",requestMeasurements,{once:true});
 }

 mount.innerHTML="<!-- RKK News v1.0 | Kehaketut.fi custom front page, live source: /uutiset/ -->\n<section id=\"rkk-news-live\" aria-labelledby=\"rkk-news-title\">\n<style>\n#rkk-news-live{--rk-red:#b91c2b;--rk-black:#171a1f;--rk-gray:#6d7780;font-family:system-ui,-apple-system,'Segoe UI',Arial,sans-serif;max-width:1160px;margin:26px auto 32px;color:var(--rk-black)}\n#rkk-news-live *{box-sizing:border-box}\n#rkk-news-live .nh{display:flex;gap:14px;align-items:center;margin-bottom:15px}\n#rkk-news-live .stripe{height:48px;width:5px;border-radius:8px;background:var(--rk-red);flex:none}\n#rkk-news-live .eyebrow{display:block;color:#a7192b;font-size:10px;font-weight:850;letter-spacing:.15em;text-transform:uppercase}\n#rkk-news-live h2{font-size:clamp(25px,3.2vw,32px)!important;line-height:1.16;margin:2px 0!important;color:var(--rk-black)!important;font-weight:850;letter-spacing:-.025em}\n#rkk-news-live .all{margin-left:auto;flex:none;color:#a7192b!important;font-size:12px;font-weight:800;text-decoration:none;padding:10px 12px;border:1px solid #edcbd0;border-radius:9px;background:#fff}\n#rkk-news-live .all:hover{background:#fff3f4}\n#rkk-news-live .cards{display:grid;grid-template-columns:minmax(0,1.16fr) minmax(0,1fr);grid-template-rows:repeat(2,minmax(136px,auto));gap:12px}\n#rkk-news-live .item{position:relative;display:flex;flex-direction:column;justify-content:space-between;min-width:0;border:1px solid #e3e6e9;background:#fff;border-radius:14px;padding:20px 22px;text-decoration:none!important;color:var(--rk-black)!important;transition:border-color .16s,transform .16s,box-shadow .16s}\n#rkk-news-live .item:hover,#rkk-news-live .item:focus-visible{border-color:#b91c2b;transform:translateY(-2px);box-shadow:0 6px 22px rgba(18,24,31,.08)}\n#rkk-news-live .item:focus-visible{outline:3px solid #b91c2b;outline-offset:2px}\n#rkk-news-live .item.lead{grid-row:span 2;min-height:286px;padding:25px 26px;background:linear-gradient(145deg,#fff,#faf8f8)}\n#rkk-news-live .meta{display:flex;gap:9px;align-items:center;margin-bottom:10px;font-size:10px;font-weight:850;letter-spacing:.08em;color:#a7192b;text-transform:uppercase}\n#rkk-news-live .tag{display:inline-flex;padding:5px 8px;background:#fff0f2;border-radius:6px}\n#rkk-news-live .group-tag{display:inline-flex;padding:5px 8px;background:#f3f5f7;color:#374151;border:1px solid #e3e7ec;border-radius:6px;font-size:10px;font-weight:800;letter-spacing:.03em}\n#rkk-news-live .date{color:#747d86;font-weight:650;letter-spacing:0;font-size:11px}\n#rkk-news-live h3{margin:0 0 10px!important;color:#1d242b!important;font-size:clamp(16px,1.7vw,20px)!important;line-height:1.28!important;letter-spacing:-.016em;font-weight:800;overflow-wrap:anywhere}\n#rkk-news-live .lead h3{font-size:clamp(23px,2.45vw,30px)!important;max-width:28ch}\n#rkk-news-live .excerpt{color:#58636d;font-size:13px;line-height:1.55;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin:0 0 10px}\n#rkk-news-live .lead .excerpt{-webkit-line-clamp:4;font-size:14px}\n#rkk-news-live .read{font-size:11px;font-weight:850;color:#a7192b;align-self:flex-start;margin-top:12px}\n#rkk-news-live .item .num{position:absolute;right:19px;bottom:18px;color:#e7eaed;font-size:38px;font-weight:900;line-height:1;letter-spacing:-.08em;pointer-events:none}\n#rkk-news-live .item.lead .num{font-size:78px;color:#f1e1e3}\n#rkk-news-live .note{color:#79838d;font-size:11px;margin:12px 0 0}\n#rkk-news-live .state{padding:22px;background:#fff;border:1px solid #e3e6e9;border-radius:14px;color:#67737e;font-size:13px}\n#rkk-news-live .state a{color:#a7192b!important;font-weight:800}\n@media(max-width:730px){#rkk-news-live .cards{grid-template-columns:1fr;grid-template-rows:auto}#rkk-news-live .item.lead{grid-row:auto;min-height:218px;padding:20px}#rkk-news-live .item{padding:17px;min-height:135px}#rkk-news-live .all{font-size:11px;padding:9px}#rkk-news-live .lead h3{font-size:24px!important}}\n@media(prefers-reduced-motion:reduce){#rkk-news-live .item{transition:none}#rkk-news-live .item:hover{transform:none}}\n</style>\n<div class=\"nh\">\n  <span class=\"stripe\" aria-hidden=\"true\"></span>\n  <div><span class=\"eyebrow\">Seuran kuulumiset</span><h2 id=\"rkk-news-title\">Ajankohtaista</h2></div>\n  <a class=\"all\" href=\"/uutiset/\">Kaikki uutiset ↗</a>\n</div>\n<div id=\"rkk-news-cards\" class=\"cards\" aria-live=\"polite\">\n  <div class=\"state\" style=\"grid-column:1/-1\">Haetaan uusimmat seurauutiset…</div>\n</div>\n<p class=\"note\">Uutiset avautuvat alkuperäisille artikkeleille. Etusivu näyttää kolme uusinta julkista uutista.</p>\n\n</section>";
 if(!document.getElementById("rkk-global-separators"))mount.insertAdjacentHTML("beforeend","\n<style id=\"rkk-global-separators\">\n#rkk-home03:after,#rkk-news-live:after,#rkk-boxers04:after{\n content:\"\";display:block;height:2px;clear:both;margin:38px auto 18px;\n background:linear-gradient(90deg,transparent,#d6dbe0 12%,#d6dbe0 46%,#b91c2b 46%,#b91c2b 54%,#d6dbe0 54%,#d6dbe0 88%,transparent);\n max-width:1160px;\n}\n#rkk-news-live{padding-top:20px!important}\n#rkk-news-live::before{content:\"\";display:block;width:100%;height:2px;max-width:1160px;margin:-8px auto 28px;background:linear-gradient(90deg,transparent,#d6dbe0 12%,#d6dbe0 46%,#b91c2b 46%,#b91c2b 54%,#d6dbe0 54%,#d6dbe0 88%,transparent);}\n#rkk-boxers04{padding-top:20px!important}\n@media(max-width:600px){#rkk-home03:after,#rkk-news-live:after,#rkk-boxers04:after{margin:26px auto 14px}}\n</style>");
 
(function(){
  'use strict';
  var wrap=document.getElementById('rkk-news-cards');
  if(!wrap)return;
  var root='/uutiset/';
  var pfx='/uutiset/';
  function clean(s){return (s||'').replace(/\s+/g,' ').replace(/^[\s›»•]+|[\s›»•]+$/g,'').trim();}
  function validNews(href){
    try{
      var u=new URL(href,location.href);
      return (u.hostname==='kehaketut.fi'||u.hostname==='www.kehaketut.fi') &&
        u.pathname.startsWith(pfx) && u.pathname!==pfx &&
        u.pathname.slice(pfx.length).replace(/\/$/,'').length>2 ? u.href:null;
    }catch(e){return null;}
  }
  function getDate(txt,el){
    var t=el.querySelector('time[datetime]');
    if(t){var d=(t.getAttribute('datetime')||'').slice(0,10);if(/^20\d{2}-\d\d-\d\d$/.test(d))return d.split('-').reverse().join('.');}
    var m=txt.match(/\b(\d{1,2}\.\d{1,2}\.20\d{2})\b/g);
    return m?m[0]:'';
  }
  function parseNews(html){
    var dom=new DOMParser().parseFromString(html,'text/html');
    var seen=new Set(),out=[];
    Array.from(dom.querySelectorAll('a[href]')).forEach(function(a){
      var url=validNews(a.getAttribute('href'));
      if(!url||seen.has(url))return;
      var raw=clean(a.textContent);
      if(raw.length<9)return;
      var node=a.closest('article,li,[class*="news-item"],[class*="newsItem"]')||a;
      var date=getDate(raw,a)||getDate(clean(node.textContent),node);
      var cut=date?raw.indexOf(date):-1;
      var title=cut>4?clean(raw.slice(0,cut)):clean(raw.split(/ [\.!?] /)[0]);
      var excerpt=cut>0?clean(raw.slice(cut+date.length)):'';
      if(title.length>130){title=title.slice(0,127).replace(/\s+\S*$/,'')+'…';}
      if(!excerpt){
        var surrounding=clean(node.textContent);
        if(surrounding.length>raw.length&&surrounding.length<600)excerpt=clean(surrounding.slice(raw.length));
      }
      if(excerpt.length>220)excerpt=excerpt.slice(0,217).replace(/\s+\S*$/,'')+'…';
      if(!title||title.toLowerCase()==='uutiset')return;
      seen.add(url);out.push({url:url,title:title,date:date,excerpt:excerpt});
    });
    return out.slice(0,3);
  }
  function el(tag,cl,txt){var x=document.createElement(tag);if(cl)x.className=cl;if(txt)x.textContent=txt;return x;}
  function render(items){
    wrap.replaceChildren();
    items.forEach(function(n,i){
      var a=el('a','item'+(i===0?' lead':''));a.href=n.url;
      var head=el('div'),meta=el('div','meta');var labels={general:'Koko seura',competitive:'Kilpanyrkkeily',juniors:'Juniorit',fitness:'Kuntonyrkkeily',women:'Naisten nyrkkeily'};var groups=Array.isArray(n.groups)?n.groups.filter(function(g){return !!labels[g]}):[];if(!groups.length){meta.appendChild(el('span','tag',i===0?'Uusin uutinen':'Seurauutiset'));}else{groups.slice(0,2).forEach(function(g){meta.appendChild(el('span','group-tag',labels[g]));});}
      if(n.date)meta.appendChild(el('span','date',n.date));head.appendChild(meta);
      head.appendChild(el('h3','',n.title));
      if(n.excerpt)head.appendChild(el('p','excerpt',n.excerpt));
      a.appendChild(head);a.appendChild(el('span','read','Lue uutinen ↗'));
      a.appendChild(el('span','num','0'+(i+1)));wrap.appendChild(a);
    });
  }
  function fail(){wrap.className='';wrap.replaceChildren();var p=el('div','state','Uutisia ei saatu ladattua tähän näkymään. ');var a=el('a','', 'Avaa seuran uutiset ↗');a.href=root;p.appendChild(a);wrap.appendChild(p);}
  function showFeed(){
    var payload=window.RKK_NEWS_PAYLOAD;
    if(!payload||!Array.isArray(payload.items)||!payload.items.length){fail();return}
    var items=payload.items.slice(0,3).filter(function(n){
      try{var u=new URL(n.url);return u.protocol==='https:'&&/^(www\.)?kehaketut\.fi$/.test(u.hostname)&&u.pathname.startsWith('/uutiset/')}catch(e){return false}
    });
    if(!items.length){fail();return}
    render(items);
  }
  if(window.RKK_NEWS_PAYLOAD&&window.RKK_NEWS_PAYLOAD.items){
    showFeed();
  }else{
    document.addEventListener('rkk-news-ready',showFeed,{once:true});
    var data=document.createElement('script');
    data.src='https://glesima.github.io/kehaketut-feed/news-data.js';
    data.async=true;
    data.onerror=fail;
    document.head.appendChild(data);
  }
})();

})();
