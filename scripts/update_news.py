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
from news_rss import build_rss

BASE = "https://www.kehaketut.fi/uutiset/"
DEST = Path(__file__).resolve().parents[1] / "docs"
UA = "KehaketutWebsiteFeed/0.2 (+https://www.kehaketut.fi/)"
LOG = logging.getLogger("rkk-news")

GROUP_TAGS = {"general", "competitive", "juniors", "fitness", "women"}


def load_approved_groups():
    """Never classify article readers' interests or participants by guessing."""
    path = DEST.parent / "config" / "news_audiences.json"
    try:
        entries = json.loads(path.read_text(encoding="utf-8")).get("articles", [])
    except (OSError, ValueError):
        return {}
    groups = {}
    for entry in entries:
        url = entry.get("url", "")
        approved = entry.get("groups", [])
        if (url.startswith("https://www.kehaketut.fi/uutiset/")
                and isinstance(approved, list)
                and set(approved).issubset(GROUP_TAGS)):
            groups[url] = list(dict.fromkeys(approved))
    return groups





def clean(text):
    return " ".join((text or "").split())



NEWS_DATE_RE = re.compile(r"(?<!\d)([0-3]?\d\.[01]?\d\.20\d{2})(?!\d)")
TITLE_DATE_CUES = ("alkaa", "peruttu", "perutaan", "klo", "järjestetään", "pidetään")


def split_news_record(raw, anchor, *, today=None):
    """Separate headline, Yhdistysavain publication date and article excerpt.

    A date inside a headline, e.g. 'Peruttu 27.–29.10.2026', is not the
    publication date. Prefer a real HTML time/date marker when available.
    """
    candidates = []
    for m in NEWS_DATE_RE.finditer(raw):
        try:
            parsed = datetime.strptime(m.group(1), "%d.%m.%Y").date()
            candidates.append((m, parsed))
        except ValueError:
            continue
    if not candidates:
        return None
    picked = None
    for node in anchor.select("time, [itemprop='datePublished'], [class*='date'], [class*='Date']"):
        val = (node.get("datetime") or node.get("content") or clean(node.get_text(" ", strip=True)))
        try:
            if re.fullmatch(r"20\d{2}-\d{2}-\d{2}(?:T.*)?", val):
                dt = datetime.strptime(val[:10], "%Y-%m-%d").date()
            elif re.fullmatch(r"[0-3]?\d\.[01]?\d\.20\d{2}", val):
                dt = datetime.strptime(val, "%d.%m.%Y").date()
            else:
                continue
        except ValueError:
            continue
        matches = [m for m, d in candidates if d == dt]
        if matches:
            picked = matches[-1]  # same date can appear earlier in the headline
            break
    if picked is None:
        picked = candidates[0][0]
        if len(candidates) > 1:
            first, date1 = candidates[0]
            second, date2 = candidates[1]
            near = second.start() - first.end() <= 110
            prefix = raw[:first.start()].casefold()
            title_date = (any(cue in prefix for cue in TITLE_DATE_CUES)
                          or prefix.rstrip().endswith(("–", "-", "—")))
            reference = today or datetime.now(timezone.utc).date()
            if near and date2 <= reference and (
                title_date or date1 > reference
                or (date2 > date1 and second.start() - first.end() <= 30)
            ):
                picked = second
    return (clean(raw[:picked.start()].strip(" -|")),
            picked.group(1), clean(raw[picked.end():]))


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
        record = split_news_record(raw, anchor)
        if not record:
            parent = anchor.parent
            around = clean(parent.get_text(" ", strip=True)) if parent else raw
            record = split_news_record(around, parent or anchor)
            if not record:
                continue
        title, date, excerpt = record
        if len(title) < 8:
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
    allowed_groups = load_approved_groups()
    for item in news:
        item["groups"] = allowed_groups.get(item["url"], [])
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
    # Approved newsroom articles, not every BoxerBase registration/bout.
    # Stable article URLs as GUIDs prevent the same item recurring on every run.
    (DEST / "news-rss.xml").write_bytes(build_rss(doc))
    LOG.info("Updated news: %d posts, newest %s", len(news), news[0]["title"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    refresh_news()
