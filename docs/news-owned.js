/* Public, editorially approved Kehä-Ketut articles. Add only after publication approval.
   This is the shared source for homepage and news archive. */
(function(){
 "use strict";
 window.RKK_OWNED_NEWS={
  version:1,
  items:[{
   url:"https://glesima.github.io/kehaketut-feed/tiedotteet/ilo-gronroos-mestaruushaastattelu-2026-11-11.html",
   title:"VIDEO: Ilo Grönroos kertoo mestaruustunnelmistaan",
   date:"11.11.2026",
   excerpt:"Nyt ääneen pääsee mestari itse! Katso 1 min 41 s haastattelu – B-juniorit, yli 80 kg.",
   groups:["competitive","juniors"],
   kind:"video",
   image:"https://static.metricool.com/planner/202611/7632678-file-18034551498224287573.jpeg",
   image_alt:"Ilo Grönroos nuorten SM-kilpailuissa",
   status:"published"
  },{

   url:"https://glesima.github.io/kehaketut-feed/tiedotteet/ilo-gronroos-suomen-mestariksi-2026-11-09.html",
   title:"Ilo Grönroos nyrkkeili Suomen mestariksi Kempeleessä!",
   date:"9.11.2026",
   excerpt:"Katso video: B-junioreiden yli 80 kg sarjan Suomen mestari Ilo Grönroos kertoo kisatunnelmistaan, harjoittelusta ja tavoitteistaan.",
   groups:["competitive","juniors"],
   image:"https://static.metricool.com/planner/202611/7632678-file-18034551498224287573.jpeg",
   image_alt:"Ilo Grönroos nuorten SM-kilpailuissa Kempeleessä",
   status:"published"
  }]
 };
 document.dispatchEvent(new Event("rkk-owned-news-ready"));
})();
