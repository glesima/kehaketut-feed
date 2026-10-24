/* RKK live BoxerBase profile for existing /kilpailijat/.../ pages */
(function(){
  "use strict";
  var mount=document.getElementById("rkk-profile-slot");
  if(!mount)return;
  var idBySlug={
    "daniela-taskila":"KyEKnjm-NRp4",
    "ilo-gronroos":"0efaqUGeO1JP",
    "josias-ndikumana":"rLyNGj8sCoF7",
    "kosmo-gronroos":"RGUkxNVIo4px",
    "maarjo-ranne":"5A-7Dh4jmTdy",
    "gleb-simanov":"U2N_OOYxyFui",
    "rami-vuori":"2zTFqL5gFsqg",
    "simo-poyry":"vK0bN2sPxnbo",
    "otso-vastila":"CVjkkb7fii6a"
  };
  var slug=location.pathname.replace(/\/+$/,"").split("/").pop().toLowerCase();
  var id=idBySlug[slug];
  if(!id){mount.textContent="BoxerBase-profiilia ei löytynyt tälle sivulle.";return;}
  var f=document.createElement("iframe");
  f.id="rkk-live-profile-"+id;
  f.title="Nyrkkeilijän ajantasaiset BoxerBase-tilastot";
  f.loading="lazy";
  f.style.cssText="display:block;width:100%;height:280px;border:0;background:transparent;";
  f.src="https://glesima.github.io/kehaketut-feed/widget.html?view=profile&id="+encodeURIComponent(id);
  mount.appendChild(f);
  window.addEventListener("message",function(e){
    if(e.origin!=="https://glesima.github.io"||!e.data||e.data.type!=="RKK_WIDGET_HEIGHT"||e.data.view!=="profile")return;
    f.style.height=Math.max(230,Math.min(1200,Number(e.data.height)||280))+"px";
  });
})();
