#!/usr/bin/env python3
"""Read-only browser check of public BoxerBase participant search and paging.
No private sign-in, hidden API calls, DOB, names, emails or secrets in logs.
"""
import json
import re
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

URL="https://fin.boxerbase.com/e/zdyYMbmXqIuV/participants"
opt=Options()
opt.binary_location="/usr/bin/google-chrome"
for x in ("--headless=new","--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--window-size=1360,900"):
    opt.add_argument(x)
opt.set_capability("goog:loggingPrefs",{"performance":"ALL"})
driver=webdriver.Chrome(service=Service("/usr/bin/chromedriver"),options=opt)
driver.set_page_load_timeout(35)
try:
    driver.get(URL)
    WebDriverWait(driver,30).until(lambda d: len(d.find_elements(By.CSS_SELECTOR,"table tbody tr"))>0)
    before=len(driver.find_elements(By.CSS_SELECTOR,"table tbody tr"))
    print("BROWSER ready visible rows:",before)
    # Interact with the SAME search input available to an unauthenticated visitor.
    inputs=driver.find_elements(By.CSS_SELECTOR,"input[placeholder*='Search']")
    print("BROWSER public searchable inputs:",len(inputs))
    if inputs:
        inputs[0].clear()
        inputs[0].send_keys("Riihimäen")
        time.sleep(3.5)
        rows=driver.find_elements(By.CSS_SELECTOR,"table tbody tr")
        print("BROWSER after publicly searching club visible rows:",len(rows))
        club_counts={}
        for tr in rows[:25]:
            cells=tr.find_elements(By.CSS_SELECTOR,"td")
            if len(cells)>=2:
                club=" ".join(cells[1].text.split())
                club_counts[club]=club_counts.get(club,0)+1
        print("BROWSER filtered club name counts only:",club_counts)
        print("BROWSER top page labels:",[x.get_attribute("aria-label") for x in driver.find_elements(By.CSS_SELECTOR,"button[aria-label^='Page ']")][:12])
    # Record only origin/path, not query parameters or headers.
    entries=driver.get_log("performance")
    urls=set()
    for entry in entries:
        try:
            item=json.loads(entry["message"])["message"]
            if item.get("method") not in ("Network.requestWillBeSent","Network.responseReceived"):
                continue
            args=item.get("params",{})
            raw=(args.get("request") or args.get("response") or {}).get("url","")
            p=urlparse(raw)
            if p.hostname=="fin.boxerbase.com" and ("/api/" in p.path or "/__data.json" in p.path):
                urls.add(p.path[:160])
        except Exception:
            continue
    print("BROWSER public UI network API paths only:",sorted(urls)[:15])
finally:
    driver.quit()
