/* Update ONLY retired club and known merged profile links on CMS-rendered pages. */
(function(){
"use strict";if(window.__RKK_BOXERBASE_LINKS_V1)return;window.__RKK_BOXERBASE_LINKS_V1=true;
var old="1Le8shnOwPIW",current="mZjkT0LW248X",ids=Object.create(null);
function fix(){
 document.querySelectorAll("a[href]").forEach(function(a){
  try{
   var u=new URL(a.getAttribute("href"),document.baseURI);
   if(u.protocol!=="https:"||u.username||u.password||u.port||!(u.hostname==="boxerbase.com"||u.hostname.endsWith(".boxerbase.com")))return;
   var club=u.pathname.match(/^(\/(?:[a-z]{2}\/)?o\/)([^/]+)(\/.*)?$/);
   var boxer=u.pathname.match(/^(\/(?:[a-z]{2}\/)?boxer\/)([^/]+)(\/*)$/);
   if(club&&club[2]===old){u.pathname=club[1]+current+(club[3]||"");a.href=u.href;}
   else if(boxer&&Object.prototype.hasOwnProperty.call(ids,boxer[2])){u.pathname=boxer[1]+ids[boxer[2]]+boxer[3];a.href=u.href;}
  }catch(e){}
 });
}
function boot(){
 fix();
 fetch("https://glesima.github.io/kehaketut-feed/data.json",{cache:"no-store",credentials:"omit"}).then(function(r){if(!r.ok)throw Error("No feed");return r.json()}).then(function(d){
  if(d.club_id!==current||!d.boxer_id_aliases)return;
  var valid=new Set((d.boxers||[]).map(function(b){return b.id}));
  Object.keys(d.boxer_id_aliases).forEach(function(k){var v=d.boxer_id_aliases[k];if(/^[A-Za-z0-9_-]+$/.test(k)&&valid.has(v))ids[k]=v;});
  fix();
 }).catch(function(){});
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",boot,{once:true});else boot();
})();