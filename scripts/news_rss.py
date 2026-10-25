"""Safe, stable RSS 2.0 for RKK's APPROVED Yhdistysavain news.

This exports published public news only. It never posts to social networks,
creates scheduled posts or authorizes any publication.
"""
from datetime import datetime, timezone
from email.utils import format_datetime
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

TITLE = "Riihimäen Kehä-Ketut – seurauutiset"
BASE = "https://www.kehaketut.fi/uutiset/"
AUDIENCES = {
    "general": "Koko seura",
    "competitive": "Kilpanyrkkeily",
    "juniors": "Juniorit",
    "fitness": "Kuntonyrkkeily",
    "women": "Naisten nyrkkeily",
}


def valid_public_news_url(url):
    try:
        p = urlparse(url or "")
        return (
            p.scheme == "https"
            and p.hostname in ("kehaketut.fi", "www.kehaketut.fi")
            and p.path.startswith("/uutiset/")
            and p.path.rstrip("/") != "/uutiset"
            and not p.username
            and not p.password
        )
    except ValueError:
        return False


def build_rss(news_document, max_items=10):
    if not isinstance(news_document, dict):
        raise ValueError("news_document must be an object")
    root = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(root, "channel")
    for key, val in (
        ("title", TITLE),
        ("link", BASE),
        ("description", "Kehä-Kettujen toimituksellisesti julkaistut uutiset, ei ottelukohtaista automaattispämmiä."),
        ("language", "fi"),
    ):
        ET.SubElement(channel, key).text = val
    seen = set()
    count = 0
    for news in news_document.get("items") or []:
        if count >= max_items:
            break
        url = str(news.get("url") or "")
        title = str(news.get("title") or "").strip()
        if not valid_public_news_url(url) or url in seen or not title:
            continue
        try:
            published = datetime.strptime(news["date"], "%d.%m.%Y").replace(
                hour=12, tzinfo=timezone.utc
            )
        except (KeyError, TypeError, ValueError):
            continue
        seen.add(url)
        count += 1
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title[:180]
        ET.SubElement(item, "link").text = url
        ET.SubElement(item, "guid", {"isPermaLink": "true"}).text = url
        ET.SubElement(item, "pubDate").text = format_datetime(published)
        ET.SubElement(item, "description").text = str(news.get("excerpt") or "")[:300]
        groups = news.get("groups") or []
        if isinstance(groups, list):
            for group in sorted(set(groups) & AUDIENCES.keys()):
                ET.SubElement(item, "category").text = AUDIENCES[group]
    if count == 0:
        raise ValueError("Refusing to publish an empty news RSS feed")
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
