#!/usr/bin/env python3
"""Refresh the 3 most recent publicly visible Riihimaen Keha-Ketut news posts.

Runs on GitHub Actions, not in the Yhdistysavain browser. A failed fetch
leaves the last known good news JSON/JS intact.
"""
import json
import logging
import re
import urllib.robotparser
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE = "https://www.kehaketut.fi/uutiset/"
DEST = Path(__file__).resolve().parents[1] / "docs"
UA = "KehaketutWebsiteFeed/0.2 (+https://www.kehaketut.fi/)"
LOG = logging.getLogger("rkk-news")


def clean(text):
    return " ".join((text or "").split())


def extract_news(html):
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    seen = set()
    for anchor in soup.select("a[href]"):
        url = urljoin(BASE, anchor.get("href", ""))
        p = urlparse(url)
        if p.scheme != "https" or p.hostname not in ("www.kehaketut.fi", "kehaketut.fi"):
            continue
        if not p.path.startswith("/uutiset/") or p.path.rstrip("/") == "/uutiset":
            continue
        if url in seen:
            continue
        raw = clean(anchor.get_text(" ", strip=True))
        if len(raw) < 12:
            continue
        # The Yhdistysavain listing includes date between title and excerpt.
        found = list(re.finditer(r"(?<!\d)([0-3]?\d\.[01]?\d\.20\d{2})(?!\d)", raw))
        if not found:
            parent = anchor.parent
            around = clean(parent.get_text(" ", strip=True)) if parent else raw
            found = list(re.finditer(r"(?<!\d)([0-3]?\d\.[01]?\d\.20\d{2})(?!\d)", around))
            if not found:
                continue
            raw = around
        # Prefer a date after the main headline if the title itself contains a date.
        date_match = found[0]
        if len(found) > 1 and date_match.start() > 30 and "alkaa" in raw[:date_match.start()].casefold():
            date_match = found[1]
        title = clean(raw[:date_match.start()].strip(" -|"))
        excerpt = clean(raw[date_match.end():])
        if len(title) < 8:
            continue
        date = date_match.group(1)
        try:
            parsed = datetime.strptime(date, "%d.%m.%Y")
        except ValueError:
            continue
        seen.add(url)
        articles.append({
            "url": url,
            "title": title[:180],
            "date": date,
            "excerpt": excerpt[:240]
        })
    articles.sort(key=lambda a: datetime.strptime(a["date"], "%d.%m.%Y"), reverse=True)
    return articles[:3]


def refresh_news():
    session = requests.Session()
    session.headers["User-Agent"] = UA
    robots = session.get("https://www.kehaketut.fi/robots.txt", timeout=12)
    if robots.status_code == 200:
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(robots.text.splitlines())
        if not rp.can_fetch(UA, BASE):
            raise RuntimeError("Site robots.txt disallows news fetch")
    elif robots.status_code != 404:
        raise RuntimeError("Cannot check Yhdistysavain robots policy")
    response = session.get(BASE, timeout=25)
    response.raise_for_status()
    if urlparse(response.url).hostname not in ("kehaketut.fi", "www.kehaketut.fi"):
        raise RuntimeError("Unexpected news redirect host")
    news = extract_news(response.content.decode("utf-8", errors="replace"))
    if not news:
        raise RuntimeError("No public news parsed; preserving last-known-good feed")
    doc = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": BASE,
        "items": news
    }
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / "news.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DEST / "news-data.js").write_text(
        "window.RKK_NEWS_PAYLOAD=" + json.dumps(doc, ensure_ascii=False) +
        ";\ndocument.dispatchEvent(new Event('rkk-news-ready'));\n",
        encoding="utf-8"
    )
    LOG.info("Updated news: %d posts, newest %s", len(news), news[0]["title"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    refresh_news()
