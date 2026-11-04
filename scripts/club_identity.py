"""Reviewed BoxerBase merge migration. Never add the two profiles' totals."""
from copy import deepcopy
from urllib.parse import urlparse


def confirmed_merge(previous, config):
    merge = config.get("confirmed_club_merge", {})
    return (bool(merge.get("from")) and previous.get("club_id") == merge.get("from")
            and config.get("club_id") == merge.get("to"))


def canonical_previous(previous, config):
    """Re-key reviewed identities without changing results or observation times."""
    out = deepcopy(previous)
    if not (confirmed_merge(previous, config)
            or previous.get("club_id") == config.get("club_id")):
        return out
    aliases = config.get("boxer_id_aliases", {})
    names = config.get("boxer_name_aliases", {})
    for boxer in out.get("boxers", []):
        old = boxer.get("id")
        new = aliases.get(old, old)
        boxer["id"] = new
        boxer["name"] = names.get(boxer.get("name"), boxer.get("name"))
        if new:
            boxer["boxerbase_url"] = "https://boxerbase.com/boxer/" + new
        boxer.pop("stats_source_url", None)
        boxer.pop("stats_source_note", None)
    for bout in out.get("matches", []):
        for field in ("boxer", "red_boxer", "blue_boxer"):
            if bout.get(field) in names:
                bout[field] = names[bout[field]]
        if bout.get("boxer_id") in aliases:
            bout["boxer_id"] = aliases[bout["boxer_id"]]
    registrations = {}
    for row in out.get("registrations", []):
        old = row.get("boxer_id")
        if old in aliases:
            row["previous_boxer_id"] = old
            row["boxer_id"] = aliases[old]
        row["boxer"] = names.get(row.get("boxer"), row.get("boxer"))
        key = (row.get("event_id") or row.get("event_url"), row.get("boxer_id"))
        prior = registrations.get(key)
        if prior is None or row.get("observed_at", "") > prior.get("observed_at", ""):
            registrations[key] = row
    if "registrations" in out:
        out["registrations"] = list(registrations.values())
    # Require a successful new roster fetch before updating club_id/freshness.
    return out


def validate_merged_roster(roster, previous, config):
    ids = [b.get("id") for b in roster]
    if not ids or any(not v for v in ids) or len(ids) != len(set(ids)):
        raise ValueError("Empty or duplicate canonical roster")
    if confirmed_merge(previous, config):
        expected = set(config.get("boxer_id_aliases", {}).values())
        if not expected or not expected.issubset(set(ids)):
            raise ValueError("Merged roster incomplete; preserving previous public data")


def profile_bout_urls(html, base_url):
    """Read public match links, never hidden hydration or private APIs."""
    import re
    from urllib.parse import urljoin
    from bs4 import BeautifulSoup
    urls = []
    for a in BeautifulSoup(html, "html.parser").select("a[href]"):
        url = urljoin(base_url, a["href"])
        p = urlparse(url)
        if (p.scheme == "https" and not p.username and not p.password and not p.port
                and (p.hostname == "boxerbase.com" or (p.hostname or "").endswith(".boxerbase.com"))
                and re.fullmatch(r"/(?:[a-z]{2}/)?e/[A-Za-z0-9_-]+/m/[A-Za-z0-9_-]+", p.path)):
            canonical = p.scheme + "://" + p.netloc + p.path
            if canonical not in urls:
                urls.append(canonical)
    return urls


def mark_stats_quality(boxer):
    """Preserve source numbers; flag contradictory totals instead of guessing."""
    values = [boxer.get(k) for k in ("matches", "wins", "losses")]
    if all(type(v) is int and v >= 0 for v in values):
        boxer["stats_consistency"] = "inconsistent" if values[1]+values[2] > values[0] else "reported"
    else:
        boxer["stats_consistency"] = "partial"
    return boxer
