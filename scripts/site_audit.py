#!/usr/bin/env python3
"""Bounded read-only audit of public Kehä-Ketut pages.

Records page-level metadata and editorial issues, NOT page body copies.
Never logs in, reads member pages, submits forms, or follows offsite URLs.
Designed for a weekly GitHub Actions job rather than continuous crawling.
"""
from __future__ import annotations

import argparse
import json
import re
import time
import urllib.robotparser
from collections import deque, Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
HOST = "www.kehaketut.fi"
BASE = "https://" + HOST
USER_AGENT = "RKKSiteAudit/1.0 (+https://www.kehaketut.fi/)"
MAX_PAGES = 90
CATEGORIES = ("harjoittelu", "kilpailijat", "uutiset", "seura", "liity", "yhteystiedot")
REVIEWED_2026 = datetime(2026, 10, 26, tzinfo=timezone.utc)
BLOCKED_PARTS = ("admin", "hallitus", "jasenet", "jasensivut",
                 "login", "kirjaudu", "tili", "account", "logout")
NON_HTML = (".pdf", ".docx", ".jpg", ".jpeg", ".png", ".gif",
            ".webp", ".zip", ".css", ".js", ".mp4", ".svg", ".ics")


def normalized_public_url(url, base=BASE):
    candidate = urljoin(base, url)
    p = urlparse(candidate)
    if p.scheme != "https" or p.hostname not in (HOST, "kehaketut.fi"):
        return None
    if p.username or p.password or p.port not in (None, 443):
        return None
    # Exclude all query strings; never accidentally index login/reset tokens.
    if p.query:
        return None
    path = re.sub(r"/+", "/", p.path or "/")
    if not path.startswith("/"):
        return None
    if any(part.casefold() in BLOCKED_PARTS
           for part in path.split("/") if part):
        return None
    if path.lower().endswith(NON_HTML):
        return None
    if path != "/" and not path.endswith("/"):
        path += "/"
    if path != "/":
        first = path.strip("/").split("/", 1)[0]
        if first not in CATEGORIES:
            return None
    return urlunparse(("https", HOST, path, "", "", ""))


def extract_internal_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    seen, links = set(), []
    for tag in soup.find_all("a", href=True):
        url = normalized_public_url(tag["href"], base)
        if url and url not in seen:
            seen.add(url)
            links.append(url)
    return links


def kind_of(path):
    if path == "/":
        return "etusivu"
    if path.startswith("/uutiset/"):
        return "uutiset"
    if path.startswith("/harjoittelu/") and "/tuloksia/" in path:
        return "historialliset_tulokset"
    if path.startswith("/harjoittelu/"):
        return "harjoittelu"
    if path.startswith("/kilpailijat/"):
        return "kilpailijat"
    if path.startswith("/seura/"):
        return "seura_ja_historia"
    return path.strip("/") or "muu"


def inspect_page(html, url, status_code=200):
    path = urlparse(url).path
    record = {"url": url, "path": path, "kind": kind_of(path),
              "http_status": status_code, "title": "", "h1": "",
              "h1_count": 0, "images_without_alt": 0, "warnings": []}
    if status_code != 200:
        record["warnings"].append("http_error")
        return record
    soup = BeautifulSoup(html, "html.parser")
    if soup.title:
        record["title"] = " ".join(soup.title.stripped_strings)[:140]
    h1s = soup.select("h1")
    record["h1_count"] = len(h1s)
    record["h1"] = " ".join(h1s[0].stripped_strings)[:110] if h1s else ""
    if len(h1s) == 0:
        record["warnings"].append("missing_h1")
    elif len(h1s) > 1:
        record["warnings"].append("multiple_h1")
    main = soup.find("main") or soup.find(attrs={"role":"main"})
    # Use just the main content for optional image accessibility checks.
    if main:
        record["images_without_alt"] = sum(1 for img in main.select("img")
                                           if not img.has_attr("alt"))
    if not soup.select_one('meta[name="description"]'):
        record["warnings"].append("meta_description_review")
    for x in soup(["style", "script", "noscript", "footer", "nav", "header"]):
        x.decompose()
    body = soup.find("main") or soup.body or soup
    text = " ".join(body.stripped_strings)
    if path == "/":
        if re.search(r"25\.8\.2026|25\.08\.2026", text):
            record["warnings"].append("stale_august_2026_course_on_home")
        if "eivät vielä päivity automaattisesti" in text.casefold():
            record["warnings"].append("outdated_automation_claim_on_home")
    if path == "/yhteystiedot/" and "Rihimäki" in text:
        record["warnings"].append("address_city_typo")
    if "/hinnat-ja-lisenssit/" in path:
        record["warnings"].append("manual_review_current_prices_and_licences")
        if "2018" in text:
            record["warnings"].append("old_2018_licence_explanation")
    if path.startswith("/kilpailijat/") and path != "/kilpailijat/":
        if "17.5.2026" in text or "17.05.2026" in text:
            record["warnings"].append("historical_boxer_stats_need_date_label")
    if path.startswith("/harjoittelu/") and path.endswith("/harjoitusajat/"):
        record["warnings"].append("manual_review_training_schedule")
    if path == "/liity/":
        record["warnings"].append("check_membership_form_in_browser")
    return record


def crawl(max_pages=MAX_PAGES, sleep=0.35, request=requests.get):
    if not isinstance(max_pages, int) or max_pages < 1 or max_pages > 120:
        raise ValueError("max_pages must be within 1..120")
    robots = request(BASE + "/robots.txt", headers={"User-Agent": USER_AGENT},
                     timeout=12)
    rp = None
    if robots.status_code == 200:
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(robots.text.splitlines())
    elif robots.status_code != 404:
        raise RuntimeError("Cannot verify public robots.txt")
    queue = deque([(BASE + "/", 0)])
    visited, pages, errors = set(), [], []
    while queue and len(visited) < max_pages:
        url, depth = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        if rp is not None and not rp.can_fetch(USER_AGENT, url):
            pages.append({"url": url, "path": urlparse(url).path,
                          "kind": kind_of(urlparse(url).path), "warnings":["robots_disallowed"],
                          "http_status": None})
            continue
        try:
            time.sleep(sleep)
            response = request(url, headers={"User-Agent": USER_AGENT}, timeout=15,
                               allow_redirects=True)
            final_url = normalized_public_url(response.url)
            if final_url is None:
                errors.append({"url":url,"reason":"redirected_offsite_or_nonpublic"})
                continue
            if response.status_code != 200:
                pages.append(inspect_page("", url, response.status_code))
                continue
            ctype = response.headers.get("content-type", "text/html")
            if "text/html" not in ctype:
                errors.append({"url":url,"reason":"non_html_response"})
                continue
            if len(response.content) > 2_000_000:
                errors.append({"url":url,"reason":"oversized_html"})
                continue
            html = response.content.decode("utf-8", errors="replace")
            pages.append(inspect_page(html, url))
            # Only follow publicly linked pages, no guessed member/admin paths.
            if depth < 9:
                for link in extract_internal_links(html, url):
                    if link not in visited and not any(entry[0] == link for entry in queue):
                        queue.append((link, depth+1))
        except requests.RequestException as exc:
            errors.append({"url":url,"reason":type(exc).__name__})
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    counts = Counter(p.get("kind") for p in pages)
    return {
        "generated_at":now, "base_url":BASE, "source":"public pages only",
        "max_pages":max_pages, "scanned":len(pages),
        "complete_bounded_scan":not bool(queue),
        "pending_queued":len(queue),
        "counts_by_kind":dict(sorted(counts.items())),
        "warnings_total":sum(len(p.get("warnings", [])) for p in pages),
        "pages":sorted(pages,key=lambda p:p["path"]),
        "fetch_errors":errors,
    }


def markdown_report(report):
    out = [
        "# Kehä-Ketut: julkisen sivuston automaattinen inventaario",
        "",
        "Tarkistettu (UTC): " + report["generated_at"],
        "",
        "**Tämä on tekninen sisällön inventaario, ei todistus kaikkien "
        "sivujen ajantasaisuudesta tai kuva- ja käyttöoikeuksista.** "
        "Vanhat kilpailutulokset ovat arvokasta historiaa, eikä niitä poisteta.",
        "",
        "Sivuja tarkistettu: **%s** / sallittu enimmäismäärä %s. "
        % (report["scanned"],report["max_pages"]),
        "Jonoon jääneitä: %s. Latausvirheitä: %s."
        % (report["pending_queued"],len(report["fetch_errors"])),
        "",
        "| Osio | Sivuja |",
        "| --- | ---: |",
    ]
    for group,n in report["counts_by_kind"].items():
        out.append("| %s | %s |" %(group,n))
    out.extend(["","## Sivukohtaiset havainnot","","| Julkinen sivu | Otsikko | Tarkista |","| --- | --- | --- |"])
    for p in report["pages"]:
        out.append("| [%s](%s) | %s | %s |" % (
            p["path"],p["url"], (p.get("h1") or p.get("title") or "—").replace("|","/"),
            ", ".join(p.get("warnings", [])) or "Ei automaattista huomautusta"))
    out.extend(["","## Seuraavat toimet",
                "",
                "1. Hyväksytä aikataulut, hinnat ja lisenssit ryhmävastaavilla "
                "ennen kuin vanhoja väitteitä muutetaan.",
                "2. Uudista harjoittelun ja liittymisen sivut yhdellä tyylijärjestelmällä.",
                "3. Säilytä vuosien 2002–2019 kilpailutulokset ja Hall of Fame "
                "omana historiallisena arkistonaan.",
                "4. Varmista kuvat, vanhat esittelytekstit ja juniorien julkaisuluvat.",
                "5. Älä muuta Yhdistysavaimen alkuperäisiä sivuja tämän "
                "GitHub-auditin perusteella ilman toimituksellista hyväksyntää.",
                ""])
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pages", type=int, default=MAX_PAGES)
    parser.add_argument("--sleep", type=float, default=0.35)
    args = parser.parse_args()
    if not 0.2 <= args.sleep <= 5:
        raise SystemExit("Unsafe rate limit")
    report = crawl(max_pages=args.max_pages, sleep=args.sleep)
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    (docs/"site-audit.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    (docs/"SIVUSTON_AUTOMAATTINEN_AUDITTI.md").write_text(
        markdown_report(report), encoding="utf-8")
    print("Audited",report["scanned"],"public pages; queued left",
          report["pending_queued"],"; fetch errors",len(report["fetch_errors"]))
    if report["scanned"] < 7:
        raise SystemExit("Public site audit unexpectedly incomplete")

if __name__ == "__main__":
    main()
