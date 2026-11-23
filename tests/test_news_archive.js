/* Unified news archive regression: approved GitHub and native history together. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const archiveHTML=fs.readFileSync("docs/uutiset/index.html","utf8");
const ownedJS=fs.readFileSync("docs/news-owned.js","utf8");
const originalArticle=fs.readFileSync("docs/tiedotteet/ilo-gronroos-suomen-mestariksi-2026-11-09.html","utf8");
const formerVideoPage=fs.readFileSync("docs/tiedotteet/ilo-gronroos-mestaruushaastattelu-2026-11-11.html","utf8");
assert.match(originalArticle,/<header class="site-topbar"/);
assert.match(originalArticle,/position:sticky;top:0/);
assert.match(originalArticle,/href="https:\/\/www\.kehaketut\.fi\/"[^>]*>← Etusivulle<\/a>/);
assert.match(originalArticle,/href="https:\/\/glesima\.github\.io\/kehaketut-feed\/uutiset\/"[^>]*>Kaikki uutiset<\/a>/);
assert.match(originalArticle,/7632678-file-9567687806549624587\.mp4/);
assert.match(originalArticle,/B-junioreiden yli 80/);
assert.match(formerVideoPage,/http-equiv="refresh"/);
assert.match(formerVideoPage,/ilo-gronroos-suomen-mestariksi-2026-11-09\.html/);
const native=JSON.parse(fs.readFileSync("docs/news-archive.json","utf8"));
const script=archiveHTML.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script,"Archive requires a browser renderer");
new Function(script);
new Function(ownedJS);
assert.match(archiveHTML,/Kaikki uutiset/);
assert.match(archiveHTML,/https:\/\/www\.kehaketut\.fi\/uutiset\//,"Preserve original native archive access");
assert.ok(Array.isArray(native.items),"Native public history is a list");

class Element {
  constructor(tag){this.tag=tag;this.children=[];this.textContent="";this.className="";this.href="";this.src="";}
  appendChild(el){this.children.push(el);return el;}
  replaceChildren(...v){this.children=v;this.textContent="";}
  remove(){this.removed=true;}
}
function find(el,tag){
  return [...(el.tag===tag?[el]:[]),...el.children.flatMap(x=>find(x,tag))];
}
function text(el){return [el.textContent,...el.children.map(text)].join(" ");}
async function render(snapshot){
  const root=new Element("div");
  const document={
    getElementById(id){assert.equal(id,"news-list");return root;},
    createElement(tag){return new Element(tag);},
    createTextNode(str){const t=new Element("#text");t.textContent=str;return t;},
    dispatchEvent(){}
  };
  const context={document,window:{},Date,URL,Event:class{},Set,
    fetch(url,options){
      assert.equal(url,"../news-archive.json");
      assert.equal(options.cache,"no-store");
      return Promise.resolve({ok:true,json:()=>Promise.resolve(snapshot)});
    }
  };
  vm.runInNewContext(ownedJS,context);
  vm.runInNewContext(script,context);
  await new Promise(resolve=>setImmediate(resolve));
  return root;
}
(async()=>{
 const root=await render(native);
 const cards=find(root,"article");
 assert.ok(cards.length>=1,"At least one approved GitHub article is always present");
 const goldURL="https://glesima.github.io/kehaketut-feed/tiedotteet/ilo-gronroos-suomen-mestariksi-2026-11-09.html";
 const goldCard=cards.find(c=>find(c,"a").some(a=>a.href===goldURL));
 const ruskisURL="https://glesima.github.io/kehaketut-feed/tiedotteet/keha-ketut-ruskiksen-skabat-2026-11-14.html";
 const ruskisCard=cards.find(c=>find(c,"a").some(a=>a.href===ruskisURL));
 const sparURL="https://glesima.github.io/kehaketut-feed/tiedotteet/sparripaiva-riihimaella-2026-11-21.html";
 const sparCard=cards.find(c=>find(c,"a").some(a=>a.href===sparURL));
 assert.ok(sparCard,"Approved 21.11. sparring day article is in archive");
 const maarjoURL="https://glesima.github.io/kehaketut-feed/tiedotteet/maarjo-ranne-maaratietoista-nyrkkeilya-2026-11-23.html";
 const maarjoCard=cards.find(c=>find(c,"a").some(a=>a.href===maarjoURL));
 assert.ok(maarjoCard,"Maarjo Ranne article is in the archive");
 assert.equal(cards[0],maarjoCard,"The newest 23.11. athlete article leads the archive");
 assert.match(text(maarjoCard),/Maarjo Ranne/);
 const maarjoArticle=fs.readFileSync("docs/tiedotteet/maarjo-ranne-maaratietoista-nyrkkeilya-2026-11-23.html","utf8");
 assert.match(maarjoArticle,/www\.kehaketut\.fi\/kilpailijat\/maarjo-ranne/);
 assert.match(maarjoArticle,/potkunyrkkeilystä/i);
 assert.match(text(sparCard),/sparripäivä/i);
 assert.ok(ruskisCard,"Approved Ruskiksen Skabat article is in archive");
 assert.match(text(ruskisCard),/debyytti/);
 assert.equal(find(ruskisCard,"img").length,0,"Do not display unrelated photos");
 assert.match(fs.readFileSync("docs/tiedotteet/keha-ketut-ruskiksen-skabat-2026-11-14.html","utf8"),/ensimmäistä kertaa virallisessa nyrkkeilyottelussaan/);

 const videoOnlyURL="https://glesima.github.io/kehaketut-feed/tiedotteet/ilo-gronroos-mestaruushaastattelu-2026-11-11.html";
 assert.ok(!cards.some(c=>find(c,"a").some(a=>a.href===videoOnlyURL)),"Do not duplicate the interview as a separate item");
 const sparArticle=fs.readFileSync("docs/tiedotteet/sparripaiva-riihimaella-2026-11-21.html","utf8");
 assert.match(sparArticle,/youtube-nocookie\.com\/embed\/OFtteT7I-MQ/,"Use confirmed, public RKK video");
 assert.match(sparArticle,/https:\/\/www\.kehaketut\.fi\/liity\//,"Give visitors correct join link");
 assert.match(sparArticle,/Hyvinkään Boxing-Team|Hämeenlinnan Kisa|Vanaja Boxing|Hattula Boxing/);
 assert.doesNotMatch(sparArticle,/Forssa|Espoo/,"Respect final exclusions");
 assert.ok(goldCard,"SM gold story is present independent of its chronological position");
 assert.match(text(goldCard),/Ilo Grönroos/);
 assert.match(text(goldCard),/Katso video/,"Original championship story keeps the embedded interview prominently advertised");
 assert.ok(find(goldCard,"img").length===1,"SM gold article retains its photo");
 for(const nativeItem of native.items){
  const title=String(nativeItem.title||"").toLocaleLowerCase("fi");
  const goldMirror=title.includes("ilo grönroos")&&(title.includes("mestar")||title.includes("sm-kult"));
  if(!goldMirror)assert.ok(cards.some(c=>find(c,"a").some(a=>a.href===nativeItem.url)),nativeItem.url);
 }
 // A later native story must come first WITHOUT removing the approved old story.
 const fresh={url:"https://www.kehaketut.fi/uutiset/uusi-uutinen-2026/",
  title:"Uudempi seurauutinen",date:"24.11.2026",excerpt:"Uusi uutinen"};
 const newer=await render({items:native.items.concat([fresh])});
 const newerCards=find(newer,"article");
 assert.match(text(newerCards[0]),/Uudempi seurauutinen/);
 assert.ok(newerCards.some(c=>find(c,"a").some(a=>a.href===goldURL)),"Older approved story remains in archive");
 const malicious={items:native.items.concat([
  {url:"https://attacker.example/uutiset/bad/",title:"Vaarallinen sivusto",date:"10.11.2026"},
  {url:"https://www.kehaketut.fi/uutiset/phish/?secret=1",title:"Ei sallittu",date:"10.11.2026"},
  {...native.items[0]}
 ])};
 const guarded=await render(malicious);
 assert.equal(find(guarded,"article").length,cards.length,"Untrusted and duplicate links excluded");
 assert.doesNotMatch(text(guarded),/Vaarallinen sivusto|Ei sallittu/);
 console.log("Unified owned/native news archive, all links, photos and URL safety: OK");
})().catch(e=>{console.error(e);process.exitCode=1});
