/* Reviewed BoxerBase identifiers after the 4 November 2026 merge. */
(function(){
'use strict';
if(window.__RKK_BOXERBASE_LINKS_V1)return;
window.__RKK_BOXERBASE_LINKS_V1=true;
var aliases={"KyEKnjm-NRp4":"Pi3gCaWD-7jD","U2N_OOYxyFui":"h9XYEbAs3Py4","0efaqUGeO1JP":"W9dy-RM88aLL","rLyNGj8sCoF7":"vfT3Q-X7B3Tf","RGUkxNVIo4px":"jRMAAn1JtaN6","5A-7Dh4jmTdy":"ir_z7p9BvsZM","CVjkkb7fii6a":"RyBcZO1fI2Rb","2zTFqL5gFsqg":"nqzy3scM-NDs","vK0bN2sPxnbo":"PxXnRMHDTclP"};
function rewrite(a){
 try{
  var raw=a.getAttribute('href');if(!raw)return;
  var u=new URL(raw,document.baseURI);
  if(u.protocol!=='https:'||u.username||u.password||u.port||
      !(u.hostname==='boxerbase.com'||u.hostname.endsWith('.boxerbase.com')))return;
  var parts=u.pathname.split('/'),changed=false;
  for(var i=0;i<parts.length-1;i++){
   if(parts[i]==='o'&&parts[i+1]==='1Le8shnOwPIW'){parts[i+1]='mZjkT0LW248X';changed=true;}
   if(parts[i]==='boxer'&&Object.prototype.hasOwnProperty.call(aliases,parts[i+1])){parts[i+1]=aliases[parts[i+1]];changed=true;}
  }
  if(changed){u.pathname=parts.join('/');a.setAttribute('href',u.href);}
 }catch(e){}
}
function scan(root){
 if(root.matches&&root.matches('a[href]'))rewrite(root);
 if(root.querySelectorAll)root.querySelectorAll('a[href]').forEach(rewrite);
}
function boot(){
 scan(document);
 if(window.MutationObserver&&document.body){
  new MutationObserver(function(records){records.forEach(function(r){r.addedNodes.forEach(scan);});})
   .observe(document.body,{childList:true,subtree:true});
 }
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
