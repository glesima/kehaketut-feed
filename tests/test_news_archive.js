/* Unified news archive regression: approved GitHub and native history together. */
"use strict";
const assert=require("node:assert/strict");
const fs=require("node:fs");
const vm=require("node:vm");
const archiveHTML=fs.readFileSync("docs/uutiset/index.html","utf8");
const ownedJS=fs.readFileSync("docs/news-owned.js","utf8");
const native=JSON.parse(fs.readFileSync("docs/news-archive.json","utf8"));
const script=archiveHTML.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script,"Archive requires a browser renderer");
new Function(script);
new Function(ownedJS);
assert.match(archiveHTML,/Kaikki uutiset/);
assert.match(archiveHTML,/https:\/\/www\.kehaketut\.fi\/uutiset\//,"Preserve original native archive access");
assert.ok(native.items.length>=3,"Seed native article history");

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
 assert.equal(cards.length,native.items.length+1,"Own news and all native entries are included");
 assert.match(text(cards[0]),/Ilo Grönroos/,"Approved SM gold article is first");
 assert.ok(find(cards[0],"img").length===1,"SM gold article retains its photo");
 for(const nativeItem of native.items)assert.ok(cards.some(c=>find(c,"a").some(a=>a.href===nativeItem.url)),nativeItem.url);
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
