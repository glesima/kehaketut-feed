/* RKK live BoxerBase profile for existing /kilpailijat/.../ pages */
(function(){
  "use strict";
  var mount=document.getElementById("rkk-profile-slot");
  if(!mount)return;
  var idBySlug={
    "daniela-taskila":"Pi3gCaWD-7jD",
    "ilo-gronroos":"W9dy-RM88aLL",
    "josias-ndikumana":"vfT3Q-X7B3Tf",
    "kosmo-gronroos":"jRMAAn1JtaN6",
    "maarjo-ranne":"ir_z7p9BvsZM",
    "gleb-simanov":"h9XYEbAs3Py4",
    "rami-vuori":"nqzy3scM-NDs",
    "simo-poyry":"PxXnRMHDTclP",
    "otso-vastila":"RyBcZO1fI2Rb"
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
