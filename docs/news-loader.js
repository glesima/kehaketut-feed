/* RKK news bootstrap: load a fresh news renderer on each page visit.
 * Intended as a ONE-TIME replacement for a directly embedded news-embed.js
 * <script src> in Yhdistysavain. Does not touch other Yhdistysavain blocks.
 */
(function(){
  'use strict';
  if(window.__RKK_NEWS_LOADER_RUNNING)return;
  window.__RKK_NEWS_LOADER_RUNNING=true;
  function boot(){
    var slot=document.getElementById('rkk-news-slot');
    if(!slot||window.__RKK_NEWS_MODULE_INITIALIZED)return;
    var script=document.createElement('script');
    // Keep browser caching for up to one minute, not across a fresh news release.
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
