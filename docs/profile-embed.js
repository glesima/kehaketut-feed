/* Stable slugs avoid hard-coded BoxerBase IDs after provider merges. */
(function(){
"use strict";
var mount=document.getElementById("rkk-profile-slot");
if(!mount||mount.dataset.mergedProfile==="1")return;
mount.dataset.mergedProfile="1";
var names={"daniela-taskila":"Daniela Taskila","ilo-gronroos":"Ilo Grönroos","josias-ndikumana":"Josias Joseph Ndikumana","josias-joseph-ndikumana":"Josias Joseph Ndikumana","kosmo-gronroos":"Kosmo Grönroos","maarjo-ranne":"Maarjo Ranne","gleb-simanov":"Gleb Simanov","rami-vuori":"Rami Vuori","simo-poyry":"Simo Pöyry","otso-vastila":"Otso Västilä"};
var slug=location.pathname.replace(/\/+$/,"").split("/").pop().toLowerCase();
if(!Object.prototype.hasOwnProperty.call(names,slug)){mount.textContent="Nyrkkeilijän ottelutietoja ei löytynyt.";return;}
var f=document.createElement("iframe");
f.id="rkk-live-profile-"+slug;f.title="Nyrkkeilijän ottelutilastot";
f.loading="lazy";f.style.cssText="display:block;width:100%;height:280px;border:0;background:transparent;";
f.src="https://glesima.github.io/kehaketut-feed/widget.html?view=profile&slug="+encodeURIComponent(slug)+"&name="+encodeURIComponent(names[slug]);
mount.appendChild(f);
window.addEventListener("message",function(e){
 if(e.origin!=="https://glesima.github.io"||e.source!==f.contentWindow||!e.data||e.data.type!=="RKK_WIDGET_HEIGHT"||e.data.view!=="profile")return;
 var h=Number(e.data.height);if(Number.isFinite(h))f.style.height=Math.max(230,Math.min(1200,h))+"px";
});
if(!document.getElementById("rkk-boxerbase-link-fix")){
 var s=document.createElement("script");s.id="rkk-boxerbase-link-fix";s.src="https://glesima.github.io/kehaketut-feed/boxerbase-links.js?v=20261108";s.async=true;document.head.appendChild(s);
}
})();
