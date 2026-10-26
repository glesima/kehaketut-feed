/* Regression test: browser article text parser and direct-source loading. */
"use strict";
const fs = require("node:fs");
const assert = require("node:assert/strict");
const file = fs.readFileSync("docs/news-embed.js", "utf8");
const start = file.indexOf("  function dateValue(s){");
const end = file.indexOf("  function parseNews(html){", start);
assert(start >= 0 && end > start, "news item parser must be present");
const clean = s => (s || "").replace(/\s+/g, " ").trim();
const parse = new Function("clean", file.slice(start, end) + "\nreturn parseItem;")(clean);
const plain = {querySelector(){return null}};
let n = parse(
  "Harjoitukset peruttu 27.–29.10.2026 26.10.2026 Riihimäen Kehä-Kettujen vuorot peruttu.",
  plain
);
assert.equal(n.title, "Harjoitukset peruttu 27.–29.10.2026");
assert.equal(n.date, "26.10.2026");
assert.match(n.excerpt, /Riihimäen/);

n = parse(
  "Nyrkkeilykoulu alkaa tiistaina 13.1.2026 klo 17 30.12.2025 Tervetuloa!",
  plain
);
assert.equal(n.date, "30.12.2025");
assert.match(n.title, /13\.1\.2026/);

n = parse(
  "Kehä-Ketut kilpailivat lokakuussa 25.10.2026 Riihimäen Kehä-Kettujen nyrkkeilijöitä nähtiin lokakuussa kahdessa kilpailutapahtumassa: Nääsnyrkkeilyissä Tampereella 10.10.2026.",
  plain
);
assert.equal(n.date, "25.10.2026");

const dated = {querySelector(){return {getAttribute(name){return name==="datetime"?"2026-10-26":null;},textContent:"26.10.2026"};}};
n = parse("Kilpailut 26.10.2026 26.10.2026 Kolme ottelua.", dated);
assert.equal(n.title, "Kilpailut 26.10.2026");
assert.equal(n.date, "26.10.2026");
assert.equal(parse("Uutinen ilman päivämäärää", plain), null);

assert(file.includes("fetch(liveUrl.href,{cache:'no-store'"), "direct same-origin refresh is required");
assert(file.includes("document.head.appendChild(data)"), "fallback feed must remain available");
console.log("Live news item parsing: OK (date-in-title and same-origin live refresh checks)");


// Full headings must never be shortened; font size adapts to actual wrapping.
const fittingStart = file.indexOf("  function fitHeadline(");
const fittingEnd = file.indexOf("  function fitVisibleHeadlines(", fittingStart);
assert(fittingStart >= 0 && fittingEnd > fittingStart);
const fitHeadline = new Function("window",file.slice(fittingStart,fittingEnd)+"\nreturn fitHeadline;")({innerWidth:1200});
function mockHeading(content,width){
  const node={textContent:content,px:0,style:{setProperty(name,value){
    assert.equal(name,"--rkk-headline-px");
    node.px=parseInt(value,10);
  }},getBoundingClientRect(){
    const lines=Math.ceil((node.textContent.length*node.px*0.56)/width);
    return {width,height:lines*node.px*1.23};
  }};
  return node;
}
const shortHeading=mockHeading("Seuran tiedote",360);
const longHeading=mockHeading("Harjoitukset peruttu 27.–29.10.2026 – Kamppailukeskuksen korjaukset",360);
fitHeadline(shortHeading,true);
fitHeadline(longHeading,true);
assert(shortHeading.px>=28);
assert(longHeading.px<shortHeading.px);
assert(longHeading.px>=19);
assert.equal(longHeading.textContent,"Harjoitukset peruttu 27.–29.10.2026 – Kamppailukeskuksen korjaukset");
assert(file.includes("overflow-wrap:anywhere"));
assert(file.includes("data.src='https://glesima.github.io/kehaketut-feed/news-data.js?fresh='+Date.now()"));
assert(file.includes("var backup=window.RKK_NEWS_PAYLOAD"));
console.log("Responsive headline fit and fresh fallback checks: OK");


// Permanent one-time Yhdistysavain embed switch should load fresh code
// without copying a whole new HTML widget on every future release.
const loader=fs.readFileSync("docs/news-loader.js","utf8");
new Function(loader); // valid JS
assert(loader.includes("document.getElementById('rkk-news-slot')"));
assert(loader.includes("news-embed.js?v='+Math.floor(Date.now()/60000)"));
assert(loader.includes("__RKK_NEWS_LOADER_RUNNING"));
console.log("Stable news bootstrap versioning checks: OK");
