#!/usr/bin/env python3
"""BoxerBase public-UI registration search; no credentials and no private data.

The server's initial HTML shows only 20 rows for an event with 157 registered.
The public browser's SvelteKit search searches the full visible participant list.
Only canonical RKK boxer IDs and public event/name/club links are retained.
"""
import json
import logging
import os
import sys
import time
from datetime import date,datetime,timedelta,timezone
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from update import CONFIG, OUT, allowed_url, robots_permits
from event_discovery import event_id_from_url,parse_public_registrations

LOG=logging.getLogger("rkk-public-registrations")


def events_to_check(data):
    events={}
    for e in list(data.get("discovered_events",[]))+list(CONFIG.get("tracked_events",[])):
        eid=e.get("id") or event_id_from_url(e.get("url",""))
        if not eid or not e.get("date") or not e.get("url"):
            continue
        try:
            day=date.fromisoformat(e["date"])
        except ValueError:
            continue
        if date.today()-timedelta(days=1)<=day<=date.today()+timedelta(days=90):
            events[eid]={**e,"id":eid}
    return list(events.values())[:12]


def open_public_browser():
    options=Options()
    options.binary_location="/usr/bin/google-chrome"
    for flag in ("--headless=new","--no-sandbox","--disable-dev-shm-usage",
                 "--disable-gpu","--window-size=1360,900"):
        options.add_argument(flag)
    driver=webdriver.Chrome(service=Service("/usr/bin/chromedriver"),options=options)
    driver.set_page_load_timeout(35)
    return driver


def examine_event(driver,event,boxers):
    url=event["url"].rstrip("/")+"/participants"
    if not allowed_url(url) or not robots_permits(url):
        raise RuntimeError("Participant list not allowed by public robots.txt")
    driver.get(url)
    search=WebDriverWait(driver,25).until(
        lambda b:b.find_elements(By.CSS_SELECTOR,"input[placeholder*='Search']"))[0]
    search.clear()
    search.send_keys("Riihimäen")
    time.sleep(2.7)
    # The browser only exposes public rows. No data-hydration scraping.
    body=driver.find_element(By.TAG_NAME,"body").get_attribute("innerHTML")
    html="<html><body>"+body+"</body></html>"
    observed,meta=parse_public_registrations(
        html,url,boxers,CONFIG["club_names"]+
        CONFIG.get("registration_club_aliases",[]))
    if not observed:
        # Read only public club labels, not names or birth years, to diagnose
        # officially spelled / abbreviated organization names.
        from bs4 import BeautifulSoup
        soup=BeautifulSoup(html,"html.parser")
        clubs=set()
        for tr in soup.select("table tbody tr"):
            cells=tr.find_all("td",recursive=False)
            for i,cell in enumerate(cells):
                link=cell.select_one('a[href*="/participants/"]')
                if link and i+1 < len(cells):
                    clubs.add(" ".join(cells[i+1].stripped_strings)[:90])
                    break
        LOG.info("Public event %s filtered rows=%d, visible club labels=%s",
                 event["id"],len(soup.select("table tbody tr")),sorted(clubs)[:6])
    now=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows=[]
    for p in observed:
        rows.append({**p,"event_id":event["id"],"event":event["name"],
                     "event_url":event["url"],"event_date":event["date"],
                     "observed_at":now,"coverage":"filtered_public_browser_ui"})
    return rows,meta


def main():
    if not OUT.exists():
        LOG.error("No published BoxerBase data; do not invent participants")
        return 1
    data=json.loads(OUT.read_text(encoding="utf-8"))
    boxers=data.get("boxers",[])
    events=events_to_check(data)
    if not boxers or not events:
        LOG.info("No upcoming public competitions to check")
        return 0
    driver=None
    successful=set()
    found=[]
    try:
        driver=open_public_browser()
        for event in events:
            try:
                regs,meta=examine_event(driver,event,boxers)
                successful.add(event["id"])
                found.extend(regs)
                LOG.info("Event %s: %d club registrations on public search",
                         event["id"],len(regs))
            except Exception as error:
                LOG.warning("Event %s cannot be searched publicly: %s",event["id"],error)
    finally:
        if driver:
            driver.quit()
    if not successful:
        LOG.warning("No public event search completed; leaving data unchanged")
        return 0
    # Replace only successfully checked event observations. Failed events
    # retain older snapshots, and disappearance is not labelled cancellation.
    canonical={b.get("name") for b in boxers}
    prior={
        (p.get("event_id"),p.get("boxer_id")):p
        for p in data.get("registrations",[])
        if p.get("event_id") not in successful and p.get("boxer_id")
    }
    for p in found:
        if p["boxer"] not in canonical:
            continue
        key=(p["event_id"],p["boxer_id"])
        existing=prior.get(key)
        if existing is None or p["registered_club"] in CONFIG["club_names"]:
            prior[key]=p
    data["registrations"]=sorted(
        prior.values(),key=lambda p:(p.get("event_date") or "",p.get("boxer") or ""))
    data["registrations_checked_at"]=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data["registration_coverage"]="Public browser search; organiser-hidden entries are unavailable."
    OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    LOG.info("Published %d public registrations from %d checked events",
             len(data["registrations"]),len(successful))
    return 0


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO,format="%(levelname)s %(message)s")
    sys.exit(main())
