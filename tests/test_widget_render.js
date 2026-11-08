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
          boxerbase_url:"https://boxerbase.com/boxer/1"},
         {id:"i",name:"Ilo Grönroos"}, {id:"k",name:"Kosmo Grönroos"}],
 matches_checked_at:"2026-10-25T21:32:56Z"
};
async function render(view, data=sample, query) {
  const root = new Element("main");
  const handlers = {};
  const calls = [];
  const parent = {postMessage(data){calls.push(data)}};
  const context = {
   document:{getElementById(id){assert.equal(id,"rkk-root");return root},
             createElement(tag){return new Element(tag)},
             documentElement:{scrollHeight:1800}},
   parent,window:{addEventListener(name,cb){handlers[name]=cb}},
   location:{search:query||"?view="+view},
   URLSearchParams,
   ResizeObserver:class{observe(){}},
   fetch(){return Promise.resolve({ok:true,json(){return Promise.resolve(data)}})}
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
  // Regression: every canonical boxer ID must resolve from the merged public club feed.
  const live = JSON.parse(fs.readFileSync("docs/data.json","utf8"));
  assert.equal(live.club_id,"mZjkT0LW248X");
  assert.equal(live.boxers.length,9,"All nine merged RKK boxer records present");
  const ids=new Set(live.boxers.map(x=>x.id));
  for(const athlete of live.boxers){
    assert.match(athlete.boxerbase_url,/^https:\/\/boxerbase\.com\/boxer\/[A-Za-z0-9_-]+$/);
    assert.equal(athlete.boxerbase_url.split("/").pop(),athlete.id);
    assert.equal(ids.has(athlete.id),true);
    assert.equal(live.profile_ids_by_slug[Object.keys(live.profile_ids_by_slug).find(
      slug=>live.profile_ids_by_slug[slug]===athlete.id)],athlete.id);
  }
  for(const [oldId,newId] of Object.entries(live.boxer_id_aliases||{})){
    assert.equal(ids.has(newId),true,"Legacy profile maps to real current ID: "+oldId);
  }
  const realCards=await render("boxers",live);
  const cards=findAll(realCards.root,"card");
  assert.equal(cards.length,9);
  for(const athlete of live.boxers){
    const card=cards.find(c=>collect(c).includes(athlete.name));
    assert.ok(card,"Card exists for "+athlete.name);
    const external=card.children.find(c=>c.tag==="a");
    assert.equal(external.href,athlete.boxerbase_url,"Correct canonical link for "+athlete.name);
  }
  const otso=cards.find(c=>collect(c).includes("Otso Västilä"));
  assert.match(collect(otso),/0 voittoa · 0 tappiota/);
  assert.doesNotMatch(collect(otso),/BoxerBase-ottelua/);
  assert.match(collect(otso),/0 ottelua/);
  const rami=cards.find(c=>collect(c).includes("Rami Vuori"));
  assert.match(collect(rami),/1 ottelu 1 voitto · 0 tappiota/);
  const josiasSingular=cards.find(c=>collect(c).includes("Josias Joseph Ndikumana"));
  assert.match(collect(josiasSingular),/1 ottelu 0 voittoa · 1 tappio/);
  const josias=cards.find(c=>collect(c).includes("Josias Joseph Ndikumana"));
  assert.match(collect(josias),/1 ottelu/);
  const otsoProfile=await render("profile",live,"?view=profile&slug=otso-vastila");
  assert.match(collect(otsoProfile.root),/Näytetyt nollat koskevat saatavilla olevia tilastoja/);
  // General calendar alone is never displayed; club participation is required.
  const eventList=[
    {id:"future1",name:"Tuleva salikisa",date:"2099-11-14",url:"https://fin.boxerbase.com/e/future1"},
    {id:"future2",name:"Tuleva SM",date:"2099-12-04",url:"https://boxerbase.com/e/future2"},
    {id:"future3",name:"Muut kisat",date:"2099-12-05",url:"https://boxerbase.com/e/future3"}
  ];
  const base={...sample,matches:[],registrations:[],discovered_events:eventList};
  const unknown=await render("updates",base);
  assert.equal(findAll(unknown.root,"public-event").length,0,"Do not list unrelated future competitions");
  assert.match(collect(unknown.root),/ei ole vielä julkaistua vahvistusta/);
  assert.doesNotMatch(collect(unknown.root),/Tuleva salikisa|Tuleva SM/);
  const known={boxer:"Ilo Grönroos",boxer_id:"i",event:"Tuleva salikisa",
    event_id:"future1",event_url:"https://fin.boxerbase.com/e/future1",
    event_date:"2099-11-14",status:"registered"};
  const confirmed=await render("updates",{...base,registrations:[known]});
  assert.equal(findAll(confirmed.root,"public-event").length,1);
  assert.match(collect(confirmed.root),/Ilmoittautuneet: Ilo Grönroos/);
  assert.doesNotMatch(collect(confirmed.root),/Tuleva SM|Muut kisat/);
  // An old public observation is not a current verified registration.
  const stale=await render("updates",{...base,registrations:[{...known,current_visibility:"previously_observed"}]});
  assert.equal(findAll(stale.root,"public-event").length,0);
  const forged=await render("updates",{...base,registrations:[
    {...known,event_url:"https://attacker.example/e/future1"},
    {...known,boxer:"Tuntematon nyrkkeilijä"},
    {...known,boxer_id:"wrong"}
  ]});
  assert.equal(findAll(forged.root,"public-event").length,0);
  // Even a large real registry yields a maximum of three relevant items.
  const entries=Array.from({length:6},(_,i)=>({
    ...known,event_id:"event"+i,event_url:"https://fin.boxerbase.com/e/event"+i,
    event:"Kilpailu "+i,event_date:"2099-12-"+String(10+i)
  }));
  const capped=await render("updates",{...base,registrations:entries});
  assert.equal(findAll(capped.root,"public-event").length,3);
  assert.doesNotMatch(collect(capped.root),/Kilpailu 3|Kilpailu 4|Kilpailu 5/);
  // Published bouts remain visible and share the three-item allowance.
  const bout={...sample.matches[0],result:"vahvistettu ottelu",event_date:"2099-12-01",
    event_url:"https://fin.boxerbase.com/e/bout1",url:"https://fin.boxerbase.com/e/bout1/m/m1"};
  const withBout=await render("updates",{...base,matches:[bout],registrations:entries});
  assert.equal(findAll(withBout.root,"bout").length,1);
  assert.equal(findAll(withBout.root,"public-event").length,2);
  // Duplicate registrations in one event produce one compact card and unique names.
  const duplicates=await render("updates",{...base,registrations:[known,known,{...known,
    boxer:"Kosmo Grönroos",boxer_id:"k"}]});
  assert.equal(findAll(duplicates.root,"public-event").length,1);
  assert.match(collect(duplicates.root),/Ilmoittautuneet: Ilo Grönroos, Kosmo Grönroos/);
  console.log("All nine boxer links, compact club-only upcoming events and registration safeguards verified.");
}
main().catch(err=>{console.error(err);process.exitCode=1});
