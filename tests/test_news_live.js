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
