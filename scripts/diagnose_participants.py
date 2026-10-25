#!/usr/bin/env python3
"""One-run READ-ONLY diagnostic of PUBLIC BoxerBase page structure.
No participant names, birth years, emails, tokens or hidden form values logged.
Uses normal public GET through update.fetch with robots check and 1.1s delay.
"""
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from update import fetch, CONFIG

URL="https://fin.boxerbase.com/e/zdyYMbmXqIuV/participants"

html=fetch(URL)
soup=BeautifulSoup(html,"html.parser")
print("DIAG size:",len(html))
print("DIAG title:", (soup.title.get_text(" ",strip=True) if soup.title else "")[:100])
print("DIAG table count:",len(soup.select("table")),"table row count:",len(soup.select("table tr")))
print("DIAG HTML frameworks:",{m:(m.lower() in html.lower()) for m in
    ['__next_f','__NEXT_DATA__','__NUXT_DATA__','data-sveltekit','window.__INITIAL_STATE__','livewire','inertia','alpine','data-table']})
print("DIAG script src:",[urlparse(urljoin(URL,a["src"])).path[:140] for a in soup.select("script[src]")][:18])
print("DIAG forms:",[{"action":urlparse(urljoin(URL,a.get("action",""))).path[:140],"method":a.get("method","GET"),
  "inputs":[inp.get("name","") for inp in a.select("input[name]")][:12]} for a in soup.select("form")][:8])
print("DIAG selects:",[{"name":x.get("name"),"id":x.get("id"),"options":len(x.select("option"))} for x in soup.select("select")][:14])
print("DIAG pagination links:",[{"href":urlparse(urljoin(URL,a.get("href",""))).path[:110],
  "query_keys":sorted(set(k for k in re.findall(r"[?&]([A-Za-z0-9_-]+)=",a.get("href",""))))} for a in soup.select("a[href]") if re.search(r"page|next|prev|perPage|limit",a.get("href",""),re.I)][:15])
print("DIAG buttons:",[{"type":x.get("type","button"),"aria_label":(x.get("aria-label") or "")[:80],
  "text":x.get_text(" ",strip=True)[:35]} for x in soup.select("button")][:25])
print("DIAG custom component tags:",sorted({x.name for x in soup.find_all() if "-" in x.name})[:25])
print("DIAG data attr keys:",sorted({key for x in soup.find_all() for key in x.attrs if key.startswith("data-")})[:40])
# Note: No source code is extracted from proprietary scripts and no undocumented endpoint is called.


import shutil
print("DIAG chrome paths:", {x: shutil.which(x) for x in ("google-chrome","chromedriver","chromium","chromium-browser","firefox","geckodriver")})
print("DIAG public app endpoints:", sorted({
   urlparse(urljoin(URL, str(x.attrs[k]))).path[:150]
   for x in soup.select("[data-api], [data-url]")
   for k in ("data-api", "data-url")
   if x.has_attr(k) and not str(x.attrs[k]).startswith("javascript:")
})[:25])
print("DIAG inline scripts:", [
 {"type":x.get("type","text/javascript"),
  "length":len(x.get_text()),
  "contains_157":('"157"' in x.get_text()),
  "contains_total_keys":("totalCount" in x.get_text() or "total:" in x.get_text()),
  "contains_roster":any(name in x.get_text() for name in ("Riihimäen Kehä-Ketut","RIIHIMÄEN KEHÄ-KETUT","Gleb Simanov"))}
 for x in soup.find_all("script") if not x.get("src")
][:12])
print("DIAG modulepreloads:", [urlparse(urljoin(URL,x.get("href",""))).path[:130] for x in soup.select('link[rel="modulepreload"]')][:18])
print("DIAG page number buttons:", [x.get("aria-label") for x in soup.select("button[aria-label^='Page ']")][:20])
print("DIAG safe user-interface only; no hidden/private requests executed")
