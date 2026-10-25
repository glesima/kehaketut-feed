"""Conservative competition news suggestion logic.

Live competition cards are primary for registrations, bout pairings and results.
This code only proposes editorial items; it never sends messages or publishes.
"""
from __future__ import annotations
from datetime import date
from urllib.parse import urlparse
from typing import Any


def event_id(url: str) -> str | None:
    parts = urlparse(url or "").path.rstrip("/").split("/")
    for i, part in enumerate(parts):
        if part == "e" and i + 1 < len(parts):
            return parts[i + 1] or None
    return None


def suggest_stories(
    snapshot: dict[str, Any],
    policy: dict[str, Any],
    *,
    today: str,
    coach_confirmed_events: frozenset[str] = frozenset(),
    results_complete_events: frozenset[str] = frozenset(),
    previously_proposed: frozenset[tuple[str, str]] = frozenset(),
) -> list[dict[str, Any]]:
    """Only curated significant event suggestions, never auto-publications.

    Coach confirmation and event completion must come from a separate
    authenticated reviewer, not from a spoofable email sender.
    previously_proposed is a persistent editorial event-stage ledger.
    """
    if not isinstance(snapshot, dict) or not isinstance(policy, dict):
        raise ValueError("Expected structured input")
    now = date.fromisoformat(today)
    noteworthy = policy.get("editorial_events") or {}
    already_covered = {
        (x["event_id"], x["stage"])
        for x in policy.get("covered_event_stages", [])
        if x.get("event_id") and x.get("stage") in ("preview", "recap")
    }
    seen = already_covered | set(previously_proposed)
    registered_by_event: dict[str, dict[str, str]] = {}
    for row in snapshot.get("registrations") or []:
        if row.get("status") != "registered":
            continue
        eid = row.get("event_id") or event_id(row.get("event_url", ""))
        boxer_id, name = row.get("boxer_id"), row.get("boxer")
        if eid and boxer_id and name:
            registered_by_event.setdefault(eid, {})[boxer_id] = name

    results_by_event: dict[str, dict[str, dict[str, Any]]] = {}
    for bout in snapshot.get("matches") or []:
        if bout.get("result") not in ("voitto", "tappio"):
            continue
        eid = event_id(bout.get("event_url", ""))
        bout_id = bout.get("id")
        if eid and bout_id:
            results_by_event.setdefault(eid, {})[bout_id] = bout

    suggestions = []
    for event in snapshot.get("discovered_events") or []:
        eid = event.get("id") or event_id(event.get("url", ""))
        if not eid:
            continue
        special = noteworthy.get(eid)
        if not special or not special.get("noteworthy"):
            continue
        event_date = event.get("date")
        if not event_date:
            continue
        d = date.fromisoformat(event_date)
        name = event.get("name") or special.get("name") or "Kilpailu"
        boxers = sorted(registered_by_event.get(eid, {}).values())
        min_entries = max(1, int(special.get("preview_min_registered", 2)))
        if (eid not in results_complete_events
            and 0 <= (d - now).days <= 21
            and len(boxers) >= min_entries
            and (eid, "preview") not in seen):
            status = ("needs_editorial_approval" if eid in coach_confirmed_events
                      else "needs_coach_confirmation")
            suggestions.append({
                "key": eid + ":preview",
                "event_id": eid,
                "stage": "preview",
                "status": status,
                "publication_allowed": False,
                "title_suggestion": "Kehä-Kettujen nyrkkeilijöitä ilmoittautunut: " + name,
                "participant_names": boxers,
                "official_event_url": event.get("url"),
                "event_date": event_date,
                "fact_note": "Ilmoittautuminen ei takaa ottelua. Varmista osallistuminen valmentajalta.",
            })
        matches = list(results_by_event.get(eid, {}).values())
        if (eid in results_complete_events and matches
            and d <= now and (eid, "recap") not in seen):
            suggestions.append({
                "key": eid + ":recap",
                "event_id": eid,
                "stage": "recap",
                "status": "needs_editorial_approval",
                "publication_allowed": False,
                "title_suggestion": "Kehä-Ketut kilpailivat: " + name,
                "results": [
                    {
                        "boxer": m["boxer"],
                        "opponent": m.get("opponent"),
                        "result": m["result"],
                        "decision": m.get("decision"),
                        "source": m.get("url"),
                    }
                    for m in sorted(matches, key=lambda row: (row.get("boxer") or "", row["id"]))
                ],
                "official_event_url": event.get("url"),
                "event_date": event_date,
            })
    return suggestions
