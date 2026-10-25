"""Keep last VERIFIED publicly observed registrations during transient UI errors.

A negative/incomplete browser search is not evidence of a withdrawal.
We do not falsely publish that somebody has been removed from a competition.
"""
from datetime import date, timedelta


def reconcile_registrations(previous, found, roster, canonical_names, today):
    if isinstance(today, str):
        today = date.fromisoformat(today)
    first_kept_day = (today - timedelta(days=2)).isoformat()
    canonical = {b.get("name") for b in roster}
    allowed_names = {b.get("id") for b in roster}
    result = {}

    for old in previous:
        if (old.get("status") != "registered" or not old.get("event_id")
                or old.get("boxer_id") not in allowed_names
                or not old.get("participant_url", "").startswith("https://")
                or old.get("event_date", "") < first_kept_day):
            continue
        key = (old["event_id"], old["boxer_id"])
        result[key] = {**old, "current_visibility": "previously_observed"}

    for item in found:
        if (item.get("status") != "registered" or item.get("boxer") not in canonical
                or item.get("boxer_id") not in allowed_names or not item.get("event_id")
                or not item.get("participant_url", "").startswith("https://")):
            continue
        key = (item["event_id"], item["boxer_id"])
        old = result.get(key)
        if (not old or item.get("registered_club") in canonical_names
                or old.get("registered_club") not in canonical_names):
            result[key] = {**item, "current_visibility": "verified_in_latest_public_search"}

    return sorted(result.values(),
                  key=lambda p: (p.get("event_date") or "", p.get("boxer") or ""))
