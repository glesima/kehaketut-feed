"""Conservative reading of PUBLIC BoxerBase event and registration pages.

Does not claim completeness for a paginated or hidden participant list.
Does not publish private weigh-ins, births, payment state or other personal fields.
"""
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def norm(value):
    return " ".join((value or "").casefold().split())


def event_id_from_url(url):
    found = re.search(r"/(?:[a-z]{2}/)?e/([A-Za-z0-9_-]+)(?:/|$)", urlparse(url).path)
    return found.group(1) if found else None


def discover_event_links(html, base_url, max_events=20):
    """Find public event landing pages from a public federation events listing."""
    soup = BeautifulSoup(html, "html.parser")
    out, seen = [], set()
    for a in soup.select('a[href]'):
        url = urljoin(base_url, a.get("href", "")).split("?")[0].rstrip("/")
        host = urlparse(url).hostname or ""
        if host != "boxerbase.com" and not host.endswith(".boxerbase.com"):
            continue
        if not re.fullmatch(r"/(?:[a-z]{2}/)?e/[A-Za-z0-9_-]+", urlparse(url).path):
            continue
        key = event_id_from_url(url)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(url)
        if len(out) >= max_events:
            break
    return out


def match_public_boxer(name, roster):
    """Only accept exactly identifiable canonical fighters or reviewed name aliases."""
    value = norm(name)
    matches = []
    for boxer in roster:
        candidate = norm(boxer.get("name", ""))
        aliases = {candidate}
        if " joseph " in candidate:
            aliases.add(candidate.replace(" joseph ", " "))
        if value in aliases:
            matches.append(boxer)
    return matches[0] if len(matches) == 1 else None


def parse_public_registrations(html, page_url, roster, clubs):
    """Return ONLY registered fighters visibly present in a public HTML table.

    Some public BoxerBase pages say 'Showing 190 of 190' but HTML initially
    renders 20 rows. Therefore metadata reports incomplete, and missing names
    are never interpreted as confirmed non-registration.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("tr")
    found = []
    seen = set()
    canonical_club = {norm(c) for c in clubs}
    visible_rows = 0
    for tr in rows:
        cells = tr.find_all("td", recursive=False)
        if len(cells) < 2:
            continue
        # BoxerBase tables may have a leading blank status column.
        # Find the participant hyperlink and the actual club instead of
        # assuming fixed td positions.
        anchor = None
        boxer_cell_index = None
        for index, cell in enumerate(cells):
            for link in cell.select("a[href]"):
                path = urlparse(urljoin(page_url, link.get("href",""))).path
                if re.search(r"/participants/[A-Za-z0-9_-]+$", path):
                    anchor, boxer_cell_index = link, index
                    break
            if anchor:
                break
        if not anchor:
            continue
        visible_rows += 1
        club_link = tr.select_one('a[href*="/o/"]')
        club_name = " ".join(club_link.stripped_strings) if club_link else ""
        if not club_name and boxer_cell_index is not None and boxer_cell_index+1<len(cells):
            club_name = " ".join(cells[boxer_cell_index+1].stripped_strings)
        if norm(club_name) not in canonical_club:
            continue
        boxer = match_public_boxer(anchor.get_text(" ", strip=True), roster)
        if not boxer:
            continue
        key = boxer.get("id")
        if not key or key in seen:
            continue
        seen.add(key)
        found.append({
            "boxer_id": key,
            "boxer": boxer["name"],
            "participant_url": urljoin(page_url, anchor["href"]),
            "registered_club": club_name,
            "status": "registered",
        })
    visible_text = " ".join(soup.stripped_strings)
    shown_match = re.search(r"\bShowing\s+(\d+)\s+of\s+(\d+)\b", visible_text, re.I)
    claimed_total = int(shown_match.group(2)) if shown_match else None
    # Even when "Showing 190 of 190" is written on the page, only 20 DOM rows
    # may be present. Treat this as incomplete rather than zero registrations.
    complete = claimed_total is not None and visible_rows >= claimed_total
    return found, {
        "visible_rows": visible_rows,
        "claimed_total": claimed_total,
        "coverage": "complete_visible_page" if complete else "limited_public_view",
    }
