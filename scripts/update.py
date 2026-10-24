#!/usr/bin/env python3
"""Create public, sanitized RKK site data from publicly visible BoxerBase pages and
(optionally) Instagram's official API. Does not post to social networks.

This file is a deployment-ready integration prototype, not proof BoxerBase permits
periodic extraction or that its HTML structure will remain stable. Respect
robots.txt, rate limits, and provider permissions before enabling scheduled runs.
"""
import json
import os
import re
import sys
import time
import logging
import urllib.robotparser
from pathlib import Path
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.etree import ElementTree as ET
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "data.json"
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
UA = "KehaketutWebsiteFeed/0.1 (+https://www.kehaketut.fi/)"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": UA, "Accept": "text/html,application/json;q=.9"})
ROBOTS = {}
LOG = logging.getLogger("rkk")


def allowed_url(url):
    p = urlparse(url)
    return (p.scheme == "https" and
            (p.hostname == "boxerbase.com" or p.hostname.endswith(".boxerbase.com")))


def robots_permits(url):
    host = urlparse(url).netloc
    if host not in ROBOTS:
        robots_url = f"https://{host}/robots.txt"
        try:
            resp = SESSION.get(robots_url, timeout=12)
            if resp.status_code == 404:
                ROBOTS[host] = None  # robots file absent
            elif resp.status_code == 200:
                rp = urllib.robotparser.RobotFileParser()
                rp.parse(resp.text.splitlines())
                ROBOTS[host] = rp
            else:
                raise RuntimeError(f"robots.txt returned {resp.status_code}")
        except Exception as exc:
            raise RuntimeError(f"Could not verify robots.txt for {host}: {exc}") from exc
    rule = ROBOTS[host]
    return rule is None or rule.can_fetch(UA, url)


def fetch(url):
    if not allowed_url(url):
        raise ValueError("Blocked a URL outside *.boxerbase.com")
    if not robots_permits(url):
        raise RuntimeError(f"robots.txt disallows fetching: {url}")
    time.sleep(1.1)
    r = SESSION.get(url, timeout=20)
    r.raise_for_status()
    if "text/html" not in r.headers.get("content-type", "text/html"):
        raise ValueError("Unexpected BoxerBase response type")
    # BoxerBase pages are UTF-8; requests may otherwise default to Latin-1.
    return r.content.decode("utf-8", errors="replace")


def compact(value):
    return " ".join(value.split())


def parse_club(html, root_url):
    soup = BeautifulSoup(html, "html.parser")
    fighters = []
    seen = set()
    for row in soup.select("tr"):
        link = row.select_one('a[href*="/boxer/"]')
        if not link:
            continue
        url = urljoin(root_url, link.get("href", ""))
        if not allowed_url(url) or url in seen:
            continue
        cells = row.find_all("td")
        # Name can be in a single anchor or split across two cells.
        name = compact(link.get_text(" ", strip=True))
        if len(cells) >= 2:
            neighbor = compact(cells[1].get_text(" ", strip=True))
            if neighbor and not name.casefold().endswith(neighbor.casefold()) and not neighbor.isdigit():
                name += " " + neighbor
        name = compact(name)
        if not name or len(name) > 90:
            continue
        match_count = None
        if cells:
            last = compact(cells[-1].get_text(" ", strip=True))
            if last.isdigit():
                match_count = int(last)
        fighters.append({"id": urlparse(url).path.rstrip("/").split("/")[-1],
                         "name": name, "boxerbase_url": url,
                         "matches": match_count, "wins": None, "losses": None})
        seen.add(url)
    if not fighters:
        raise ValueError("BoxerBase club roster could not be parsed; refusing empty overwrite")
    return fighters


def parse_profile(html):
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    count = re.search(r"\b(\d+)\s+Matches\b", text, re.I)
    wl = re.search(r"\b(\d+)\s+Wins?\s+(\d+)\s+Losses?\b", text, re.I)
    return {"matches": int(count.group(1)) if count else None,
            "wins": int(wl.group(1)) if wl else None,
            "losses": int(wl.group(2)) if wl else None}



def prefer_alias_stats(primary, secondary):
    """Temporary choice for a VERIFIED SAME athlete, never add provider totals."""
    x=primary.get("matches")
    y=secondary.get("matches")
    return isinstance(y, int) and (not isinstance(x, int) or y>x)


def event_urls_from_index(html, base_url, limit=8):
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for a in soup.select('a[href]'):
        url = urljoin(base_url, a["href"]).split("?")[0].rstrip("/")
        if not allowed_url(url):
            continue
        if not re.search(r"/(?:[a-z]{2}/)?e/[^/]+$", urlparse(url).path):
            continue
        if url not in urls:
            urls.append(url)
        if len(urls) >= limit:
            break
    return urls


def match_links(html, base_url, known_names):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for a in soup.select('a[href]'):
        url = urljoin(base_url, a.get("href", ""))
        if not allowed_url(url) or not re.search(r"/(?:[a-z]{2}/)?e/[^/]+/m/[^/]+$", urlparse(url).path):
            continue
        title = compact(a.get_text(" ", strip=True))
        # Only follow bouts that refer to a named club boxer: no crawl of others.
        if any(n.casefold() in title.casefold() for n in known_names):
            if url not in results:
                results.append(url)
    return results


def parse_match(html, url, boxers, event):
    """Parse a BoxerBase bout using the match title first, then linked boxers."""
    soup = BeautifulSoup(html, "html.parser")
    text = compact(soup.get_text(" ", strip=True))
    title = compact(soup.title.get_text(" ", strip=True)) if soup.title else ""
    names = [b["name"] for b in boxers]
    competitors = []
    vs = re.search(r"(.+?)\s+vs\s+(.+?)\s+results?\s+at\s+", title, re.I)
    if vs:
        competitors = [compact(vs.group(1)), compact(vs.group(2))]
    else:
        # Fallback: the first two competitors linked in the bout header.
        for a in soup.select('a[href*="/boxer/"]'):
            raw = compact(a.get_text(" ", strip=True))
            if raw and raw not in competitors:
                competitors.append(raw)
            if len(competitors) >= 2:
                break
    if len(competitors) < 2:
        LOG.warning("Could not identify competitors for %s", url)
        return None
    side = None
    club = None
    for i, competitor in enumerate(competitors[:2]):
        for name in names:
            if name.casefold() in competitor.casefold():
                side, club = i, name
                break
        if side is not None:
            break
    if side is None:
        LOG.warning("No tracked club boxer in bout %s: %s", url, competitors)
        return None
    # Names can be duplicated in BoxerBase. Reject bouts whose participant
    # does not carry the exact verified club label, not a similarly named club.
    club_names = list(CONFIG.get("club_names", ["Riihimäen Kehä-Ketut ry"]))
    # Specific historic bouts were registered under BoxerBase's duplicate club.
    # Accept that label only for a manually verified known competition, never generally.
    if event.get("allow_alias_club_on_bouts") and event.get("verified_as_duplicate_label"):
        club_names.append(event["verified_as_duplicate_label"])
    player_links = [compact(a.get_text(" ", strip=True)) for a in soup.select('a[href*="/participants/"], a[href*="/boxer/"]')]
    if not any(any(n in label for n in club_names) and club.casefold() in label.casefold() for label in player_links):
        LOG.warning("Skipping bout without verified club participant: %s", url)
        return None
    opponent = competitors[1-side][:100]
    # Only report official winners; scheduled bouts are never counted as results.
    win = re.search(r"\bWinner\s+(Red|Blue)\b.{0,110}?\b(\d+\s*[-–]\s*\d+|RSC(?:\s+R\d+)?|KO(?:\s+R\d+)?|ABD(?:\s+R\d+)?)\b", text, re.I)
    result = "vahvistettu ottelu"
    decision = None
    if win:
        red_won = win.group(1).casefold() == "red"
        decision = compact(win.group(2)).replace("–", "-")
        result = "voitto" if red_won == (side == 0) else "tappio"
    return {"id": urlparse(url).path.rsplit("/", 1)[-1],
            "boxer": club, "opponent": opponent,
            "result": result, "decision": decision,
            "event": event["name"], "event_date": event.get("date"),
            "event_url": event["url"], "url": url}


def get_instagram():
    token = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "").strip()
    if not token:
        LOG.info("No Instagram API token; leave media feed unchanged")
        return None
    header = {"Authorization": f"Bearer {token}"}
    base = "https://graph.instagram.com"
    user = requests.get(base + "/me", params={"fields":"id,username"},
                        headers=header, timeout=20)
    user.raise_for_status()
    username = user.json().get("username", "").casefold()
    if username != CONFIG["expected_ig_username"].casefold():
        raise RuntimeError(f"Instagram token belongs to @{username}, not the approved RKK account")
    response = requests.get(base + "/me/media",
                            params={"fields":"id,caption,media_type,media_url,thumbnail_url,permalink,timestamp", "limit":12},
                            headers=header, timeout=20)
    response.raise_for_status()
    medias = []
    for item in response.json().get("data", []):
        if item.get("media_type") == "VIDEO":
            thumbnail = item.get("thumbnail_url")
        else:
            thumbnail = item.get("media_url")
        link = item.get("permalink", "")
        if not link.startswith("https://www.instagram.com/") and not link.startswith("https://instagram.com/"):
            continue
        if not thumbnail or not thumbnail.startswith("https://"):
            continue
        medias.append({"id":str(item.get("id")), "url":link,
                       "image":thumbnail, "caption":compact(item.get("caption", ""))[:180],
                       "date":str(item.get("timestamp", ""))[:10]})
    return medias[:6]


def parse_event_date(html):
    """Best-effort date from the event landing page (English BoxerBase display)."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.select('time[datetime]'):
        val = tag.get("datetime", "")
        if re.match(r"^20\d{2}-\d{2}-\d{2}", val):
            return val[:10]
    text = compact(soup.get_text(" ", strip=True))
    m = re.search(r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\s+"
                  r"(?:January|February|March|April|May|June|July|August|September|October|November|December)"
                  r"\s+\d{1,2},?\s+20\d{2}", text)
    if not m:
        return None
    for fmt in ("%a, %B %d, %Y", "%a %B %d, %Y"):
        try:
            return datetime.strptime(m.group(), fmt).date().isoformat()
        except ValueError:
            pass
    return None


def write_rss(doc):
    """Syndicate recent confirmed bouts as event-level RSS items."""
    rss = ET.Element("rss", {"version":"2.0"})
    ch = ET.SubElement(rss, "channel")
    for key,value in (("title","Kehä-Ketut – kilpailutulokset"),
                      ("link","https://www.kehaketut.fi/"),
                      ("description","Riihimäen Kehä-Kettujen julkisiin ottelutuloksiin perustuva kooste"),
                      ("language","fi")):
        ET.SubElement(ch,key).text=value
    groups={}
    for m in doc.get("matches",[]):
        if m.get("result") not in ("voitto","tappio") or not m.get("event_date"):
            continue
        eventid=m.get("event_url") or m.get("event")
        groups.setdefault((m["event_date"], eventid),[]).append(m)
    for (date, ev_url), group in sorted(groups.items(), reverse=True)[:10]:
        one=group[0]
        item=ET.SubElement(ch,"item")
        title=f"{one['event']} – {len(group)} Kehä-Kettujen ottelua"
        ET.SubElement(item,"title").text=title
        ET.SubElement(item,"link").text=ev_url
        ET.SubElement(item,"guid",{"isPermaLink":"false"}).text="rkk:"+date+":"+one["event"]
        text="; ".join(f"{m['boxer']} – {m['opponent']}: {m['result']} ({m.get('decision') or 'ei pisteitä'})" for m in group)
        ET.SubElement(item,"description").text=text
        dt=datetime.fromisoformat(date+"T12:00:00+00:00")
        ET.SubElement(item,"pubDate").text=format_datetime(dt)
    tree=ET.ElementTree(rss)
    ET.indent(tree,space="  ")
    tree.write(ROOT/"docs"/"rss.xml",encoding="utf-8",xml_declaration=True)


def update():
    previous = {}
    if OUT.exists():
        try:
            previous = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:
            LOG.warning("Invalid prior JSON; starting from empty")
    out = dict(previous)
    out.setdefault("boxers", [])
    out.setdefault("matches", [])
    out.setdefault("instagram", [])
    errors = []
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        boxers = parse_club(fetch(CONFIG["club_url"]), CONFIG["club_url"])
        previous_map = {v.get("id"):v for v in previous.get("boxers", [])}
        for boxer in boxers:
            try:
                profile = parse_profile(fetch(boxer["boxerbase_url"]))
                for field, value in profile.items():
                    if value is not None:
                        boxer[field] = value
                old = previous_map.get(boxer["id"], {})
                for field in ("wins", "losses", "matches"):
                    if boxer[field] is None:
                        boxer[field] = old.get(field)
            except Exception as ex:
                errors.append(f"Profile {boxer['id']}: {ex}")
                old = previous_map.get(boxer["id"], {})
                for field in ("wins", "losses", "matches"):
                    if boxer[field] is None:
                        boxer[field] = old.get(field)
        # Temporary verified BoxerBase duplicate: keep canonical club roster,
        # use alternate stats only while they are MORE complete.
        # Once a coach merges the records, canonical automatically wins ties.
        for boxer in boxers:
            alias = CONFIG.get("verified_stat_aliases", {}).get(boxer["id"])
            if not isinstance(alias, dict):
                continue
            try:
                url = str(alias["url"])
                body = fetch(url)
                description = compact(BeautifulSoup(body, "html.parser").get_text(" ", strip=True))
                if (alias["person_name"].casefold() not in description.casefold()
                    or alias["club_label"].casefold() not in description.casefold()):
                    raise ValueError("Alias identity/club could not be verified")
                extra = parse_profile(body)
                if prefer_alias_stats(boxer, extra):
                    for key in ("matches", "wins", "losses"):
                        if extra.get(key) is not None:
                            boxer[key] = extra[key]
                    boxer["stats_source_url"] = url
                    boxer["stats_source_note"] = "Väliaikainen rinnakkaisprofiili"
                    LOG.info("Temporary historical stats selected for %s", boxer["name"])
            except Exception as exc:
                LOG.warning("Temporary alias unavailable for %s: %s", boxer["name"], exc)
        out["boxers"] = boxers
        if previous.get("club_id") != CONFIG.get("club_id"):
            LOG.info("Club profile corrected: drop matches from the unverified duplicate club")
            out["matches"] = []
            out.pop("matches_checked_at", None)
        out["club_id"] = CONFIG.get("club_id")
        out["club_url"] = CONFIG["club_url"]
        out["boxers_checked_at"] = now
    except Exception as ex:
        errors.append(f"Club roster: {ex}")
        boxers = out.get("boxers", [])

    if boxers:
        events = CONFIG["tracked_events"][:]
        known_events = {e["url"] for e in events}
        try:
            index = CONFIG["event_index"]
            for url in event_urls_from_index(fetch(index), index, CONFIG["max_index_events"]):
                if url not in known_events:
                    events.append({"url":url, "name":"BoxerBase-kilpailu", "date":None})
        except Exception as exc:
            errors.append(f"Event discovery: {exc}")
        old_matches = {m.get("url"):m for m in out.get("matches", [])}
        found_count = 0
        for event in events:
            try:
                info = event.copy()
                if not info.get("date") or info.get("name") == "BoxerBase-kilpailu":
                    eventhtml = fetch(info["url"])
                    page = BeautifulSoup(eventhtml, "html.parser")
                    h1 = page.find("h1")
                    if h1:
                        info["name"] = compact(h1.get_text(" ", strip=True))[:120]
                    if not info.get("date"):
                        info["date"] = parse_event_date(eventhtml)
                list_url = info["url"].rstrip("/") + "/matches"
                html = fetch(list_url)
                names = [b["name"] for b in boxers]
                names += [n.replace("Joseph ", "") for n in names if "Joseph " in n]
                links = match_links(html, list_url, names)
                LOG.info("Event %s: %d candidate club matches", info["name"], len(links))
                for url in links:
                    try:
                        found = parse_match(fetch(url), url, boxers, info)
                        if found:
                            if not found["event_date"]:
                                found["event_date"] = old_matches.get(url,{}).get("event_date")
                            # Drop identical older snapshots under another host / stale URL.
                            for prior_url, prior in list(old_matches.items()):
                                if (prior_url != url and
                                    prior.get("boxer") == found["boxer"] and
                                    prior.get("opponent") == found["opponent"] and
                                    prior.get("event_date") == found["event_date"]):
                                    del old_matches[prior_url]
                            old_matches[url] = found
                            found_count += 1
                    except Exception as exc:
                        errors.append(f"Match {url}: {exc}")
            except Exception as exc:
                errors.append(f"Event {event['url']}: {exc}")
        if found_count or old_matches:
            if found_count:
                out["matches_checked_at"] = now
            out["matches"] = sorted(old_matches.values(),
                                    key=lambda m: (m.get("event_date") or "", m["id"]),
                                    reverse=True)[:80]
    try:
        instagram = get_instagram()
        if instagram is not None:
            out["instagram"] = instagram
            out["instagram_checked_at"] = now
    except Exception as exc:
        errors.append(f"Instagram: {exc}")

    if not out["boxers"]:
        raise RuntimeError("No valid prior or fetched club data; no file will be published")
    # Fail closed if nothing was refreshed: keep the previous published feed.
    successful = any(out.get(k)==now for k in ("boxers_checked_at", "matches_checked_at", "instagram_checked_at"))
    if not successful:
        raise RuntimeError("No source updated; leave previous public feed intact")
    out["generated_at"] = now
    out["data_origin"] = "BoxerBase public views and optionally Instagram official API"
    # Detailed diagnostics remain only in CI logs, never in publicly hosted JSON.
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_rss(out)
    LOG.info("Updated %s: %d boxers, %d matches, %d IG items; %d warnings", OUT,
             len(out["boxers"]),len(out["matches"]),len(out["instagram"]),len(errors))
    for msg in errors[:12]: LOG.warning(msg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    try:
        update()
    except Exception as ex:
        LOG.error("Update failed: %s", ex)
        sys.exit(1)
