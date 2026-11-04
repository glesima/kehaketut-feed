// Pure DOM regressions; network calls are mocked, not a live website check.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const config=JSON.parse(fs.readFileSync('config.json','utf8'));
const linkScript=fs.readFileSync('docs/boxerbase-links.js','utf8');
const widget=fs.readFileSync('docs/widget.html','utf8').match(/<script>([\s\S]*?)<\/script>/)[1];
class E{
 constructor(tag){this.tag=tag;this.className='';this.textContent='';this.children=[];this.attrs={};this.style={};}
 appendChild(x){this.children.push(x);return x;}
 replaceChildren(...x){this.children=x;this.textContent='';}
 setAttribute(k,v){this.attrs[k]=v;}
 getAttribute(k){return this.attrs[k];}
 getBoundingClientRect(){return {bottom:450};}
}
function text(e){return [e.textContent,...e.children.map(text)].join(' ');}
function all(e){return [e,...e.children.flatMap(all)];}
function a(h){let x=new E('a');x.attrs.href=h;return x;}
const links=[a('https://boxerbase.com/o/1Le8shnOwPIW/boxers'),a('https://fin.boxerbase.com/fi/boxer/0efaqUGeO1JP?x=1'),
 a('https://boxerbase.com/e/c/m/m'),a('https://boxerbase.com.evil.test/o/1Le8shnOwPIW/boxers'),a('http://boxerbase.com/o/1Le8shnOwPIW/boxers'),a('https://name@boxerbase.com/o/1Le8shnOwPIW/boxers')];
const originals=links.map(x=>x.attrs.href);
const ctx={window:{},URL,document:{baseURI:'https://www.kehaketut.fi/',readyState:'complete',querySelectorAll:()=>links}};
vm.runInNewContext(linkScript,ctx);
assert.equal(links[0].attrs.href,'https://boxerbase.com/o/mZjkT0LW248X/boxers');
assert.equal(links[1].attrs.href,'https://fin.boxerbase.com/fi/boxer/W9dy-RM88aLL?x=1');
for(let i=2;i<links.length;i++)assert.equal(links[i].attrs.href,originals[i]);
vm.runInNewContext(linkScript,ctx);
async function render(id,data,view='profile'){
 const root=new E('main');
 vm.runInNewContext(widget,{document:{getElementById:()=>root,createElement:t=>new E(t)},
  window:{addEventListener(){}},parent:{postMessage(){}},location:{search:'?view='+view+'&id='+id},URLSearchParams,
  ResizeObserver:class{observe(){}},fetch:()=>Promise.resolve({ok:true,json:()=>Promise.resolve(data)})});
 await new Promise(r=>setImmediate(r));return root;
}
(async()=>{
 for(const [old,id] of Object.entries(config.boxer_id_aliases)){
  const data={boxer_id_aliases:config.boxer_id_aliases,boxers:[{id,name:'Canonical athlete',matches:3,wins:1,losses:2,boxerbase_url:'https://boxerbase.com/boxer/'+id,stats_consistency:'reported'}],matches:[]};
  const root=await render(old,data);assert.match(text(root),/Canonical athlete/);assert.doesNotMatch(text(root),/profiilia ei löytynyt/);
  assert.ok(all(root).some(x=>x.href==='https://boxerbase.com/boxer/'+id));
 }
 const d={boxers:[{id:'new',name:'Canonical athlete',matches:6,wins:4,losses:4,stats_consistency:'inconsistent',boxerbase_url:'https://boxerbase.com/boxer/new'}],matches:[{boxer:'Canonical athlete',opponent:'Opponent',event_date:'2026-10-24',result:'tappio',decision:'3-0',url:'https://boxerbase.com/e/event/m/bout'}]};
 let root=await render('new',d);assert.match(text(root),/ristiriitaiset/);assert.match(text(root),/Opponent/);
 assert.equal(all(root).filter(x=>x.tag==='b').map(x=>x.textContent).join(''),'–––');
 root=await render('',d,'boxers');assert.match(text(root),/tarkistettavana/);assert.doesNotMatch(text(root),/6 kirjattua|4 voittoa/);
 console.log('Reviewed legacy links, nine profile IDs, preserved history and inconsistent-count display verified.');
})().catch(e=>{console.error(e);process.exitCode=1;});
