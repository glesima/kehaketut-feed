/* RKK news bootstrap: source-only news plus a time-limited club notice. */
(function(){
  'use strict';
  if(window.__RKK_NEWS_LOADER_RUNNING)return;
  window.__RKK_NEWS_LOADER_RUNNING=true;
  function resumptionNotice(slot){
    var now=Date.now();
    if(now<Date.parse('2026-10-30T00:00:00+02:00') ||
       now>=Date.parse('2026-11-06T00:00:00+02:00'))return;
    var id='rkk-resumption-20261030';
    if(document.getElementById(id))return;
    var notice=document.createElement('section');
    notice.id=id;
    notice.setAttribute('aria-label','Harjoitukset jatkuvat normaalisti 30.10. alkaen');
    notice.style.cssText='max-width:1160px;margin:16px auto 10px;padding:18px 20px;border:1px solid #c4ddce;border-left:5px solid #22643d;border-radius:10px;background:#f3faf6;color:#171a1f;font:500 15px/1.6 system-ui,-apple-system,Segoe UI,sans-serif';
    var link=document.createElement('a');
    link.href='https://glesima.github.io/kehaketut-feed/tiedotteet/harjoitukset-jatkuvat-2026-10-30.html';
    link.style.cssText='display:block;color:#174d2e;font-weight:800;text-decoration:none;margin-bottom:5px;font-size:clamp(17px,2.2vw,22px);line-height:1.3';
    link.textContent='Harjoitukset jatkuvat normaalisti perjantaina 30.10.';
    notice.appendChild(link);
    notice.appendChild(document.createTextNode('Kamppailukeskuksen harjoitukset jatkuvat 30.10.2026 klo 17.00 alkaen. Tämän jälkeen harjoitellaan tavallisen aikataulun mukaisesti. Aiempi 27.–29.10. peruutus on päättynyt.'));
    slot.parentNode.insertBefore(notice,slot);
  }
  function boot(){
    var slot=document.getElementById('rkk-news-slot');
    if(!slot)return;
    resumptionNotice(slot);
    if(window.__RKK_NEWS_MODULE_INITIALIZED)return;
    var script=document.createElement('script');
    script.src='https://glesima.github.io/kehaketut-feed/news-embed.js?v='+Math.floor(Date.now()/60000);
    script.async=true;
    script.onerror=function(){
      if(!slot||window.__RKK_NEWS_MODULE_INITIALIZED)return;
      var notice=document.createElement('p');
      notice.style.cssText='padding:15px;border-left:4px solid #b91c2b;background:#fff4f5;font:14px system-ui';
      notice.textContent='Uutisnäkymää ei saatu ladattua. ';
      var link=document.createElement('a');
      link.href='/uutiset/';
      link.textContent='Avaa kaikki uutiset';
      notice.appendChild(link);
      slot.appendChild(notice);
    };
    document.head.appendChild(script);
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',boot,{once:true});
  }else boot();
})();
