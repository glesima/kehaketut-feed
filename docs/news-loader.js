/* RKK news bootstrap: load source-only news without an extra club notice. */
(function(){
  'use strict';
  if(window.__RKK_NEWS_LOADER_RUNNING)return;
  window.__RKK_NEWS_LOADER_RUNNING=true;
  // Only on the Yhdistysavain homepage: make visible native news navigation
  // point to the club's unified GitHub news archive. Native /uutiset/ itself
  // remains untouched and accessible for historical articles.
  function fixHomepageNewsLinks(){
    if(!/^(www\\.)?kehaketut\\.fi$/.test(location.hostname)||location.pathname!=="/")return;
    var destination="https://glesima.github.io/kehaketut-feed/uutiset/";
    var sel='a.d4-main-nav__link[href="/uutiset/"],a.d4-mobile-nav__link[href="/uutiset/"],a.button[href="/uutiset/"]';
    document.querySelectorAll(sel).forEach(function(a){a.href=destination;});
  }
  function boot(){
    fixHomepageNewsLinks();
    if(!document.getElementById('rkk-boxerbase-link-fix')){
      var fix=document.createElement('script');fix.id='rkk-boxerbase-link-fix';
      fix.src='https://glesima.github.io/kehaketut-feed/boxerbase-links.js?v=20261108';
      fix.async=true;document.head.appendChild(fix);
    }
    var slot=document.getElementById('rkk-news-slot');
    if(!slot)return;
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
      link.href='https://glesima.github.io/kehaketut-feed/uutiset/';
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
