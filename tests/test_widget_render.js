// Node-only DOM stub test: verifies winner identity, corners and compact box layout.
// No network or browser dependencies. Run: node tests/test_widget_render.js
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const html = fs.readFileSync("docs/widget.html", "utf8");
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script, "Widget inline script must exist");
new Function(script);

class Element {
  constructor(tag) {
    this.tag = tag; this.className = ""; this.textContent = "";
    this.children = []; this.style = {}; this.attrs = {};
  }
  appendChild(el) { this.children.push(el); return el; }
  replaceChildren(...children) { this.children = children; this.textContent = ""; }
  setAttribute(key,val) { this.attrs[key] = val; }
  getBoundingClientRect() { return {top:0,bottom:462,height:462}; }
}
function collect(node) {
  return [node.textContent, ...node.children.map(collect)].join(" ").replace(/\s+/g," ").trim();
}
function findAll(node,cls) {
  return [ ...(node.className.split(" ").includes(cls) ? [node] : []),
    ...node.children.flatMap(x => findAll(x,cls))];
}
const sample = {
 matches:[
  {id:"a",boxer:"Gleb Simanov",opponent:"Sampo Paananen",result:"tappio",
   event:"Hämeenlinnan juhlakisat",event_date:"2026-10-24",url:"https://boxerbase.com/e/a/m/a",
   red_boxer:"Gleb Simanov",blue_boxer:"Sampo Paananen",
   boxer_corner:"red",winner_corner:"blue",decision:"5-0",method:"PTS"},
  {id:"b",boxer:"Rami Vuori",opponent:"Hans Guttorm",result:"voitto",
   event:"Nääsnyrkkeilyt",event_date:"2026-10-10",url:"https://boxerbase.com/e/b/m/b",
   red_boxer:"Rami Vuori",blue_boxer:"Hans Guttorm",
   boxer_corner:"red",winner_corner:"red",decision:"RSC R2",method:"RSC",round:2}
 ],
 registrations:[
  {boxer:"Ilo Grönroos",event:"Nuorten SM-kilpailut",
   event_id:"zdyYMbmXqIuV",event_date:"2099-11-06",status:"registered",
   event_url:"https://boxerbase.com/e/zdyYMbmXqIuV"},
  {boxer:"Kosmo Grönroos",event:"Nuorten SM-kilpailut",
   event_id:"zdyYMbmXqIuV",event_date:"2099-11-06",status:"registered",
   event_url:"https://boxerbase.com/e/zdyYMbmXqIuV"}
 ],
 boxers:[{id:"1",name:"Boxer",matches:1,wins:1,losses:0,
          boxerbase_url:"https://boxerbase.com/boxer/1"}],
 matches_checked_at:"2026-10-25T21:32:56Z"
};
async function render(view) {
  const root = new Element("main");
  const handlers = {};
  const calls = [];
  const parent = {postMessage(data){calls.push(data)}};
  const context = {
   document:{getElementById(id){assert.equal(id,"rkk-root");return root},
             createElement(tag){return new Element(tag)},
             documentElement:{scrollHeight:1800}},
   parent,window:{addEventListener(name,cb){handlers[name]=cb}},
   location:{search:"?view="+view},
   URLSearchParams,
   ResizeObserver:class{observe(){}},
   fetch(){return Promise.resolve({ok:true,json(){return Promise.resolve(sample)}})}
  };
  vm.runInNewContext(script,context);
  await new Promise(resolve=>setImmediate(resolve));
  return {root,handlers,calls,parent};
}
async function main() {
  const {root,handlers,calls,parent} = await render("updates");
  const bouts=findAll(root,"bout");
  assert.equal(bouts.length,2,"Two compact bout rows");
  const text=collect(root);
  assert.match(text,/Voittaja:\s*Sampo Paananen/);
  assert.match(text,/Kehä-Ketut: tappio/);
  assert.match(text,/Voittaja:\s*Rami Vuori/);
  assert.match(text,/Kehä-Ketut: voitto/);
  assert.match(text,/Keskeytys \(RSC\)/);
  assert.match(text,/Ilo Grönroos/);
  assert.match(text,/Kosmo Grönroos/);
  assert.equal(findAll(root,"corner-square").length,4,"Only small color squares");
  assert.equal(findAll(root,"fighter--red").length,0,"No bulky colored fighter boxes");
  assert.ok(calls.some(x=>x.type==="RKK_WIDGET_HEIGHT"&&x.height===470),
            "Measured content 462+8, not iframe viewport 1800");
  const count=calls.length;
  handlers.message({source:parent,data:{type:"RKK_REQUEST_HEIGHT"}});
  assert.equal(calls.length,count+1,"Late host resize handshake works");
  const boxer=await render("boxers");
  assert.match(collect(boxer.root),/Ottelijat/);
  assert.ok(boxer.calls.some(x=>x.type==="RKK_WIDGET_HEIGHT"));
  console.log("Compact results, winner identities, registrations and intrinsic widget height verified.");
}
main().catch(err=>{console.error(err);process.exitCode=1});
