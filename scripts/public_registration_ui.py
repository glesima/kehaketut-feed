"""Verify that BoxerBase's public registration table actually applied a search.

A Selenium input field can exist in the SSR markup before Svelte has hydrated;
typing too early gets reset and silently leaves the first 20 rows visible.
Only visible browser UI state is examined: no API/private hydration scraping.
"""
import re


def public_filter_is_applied(visible_text, current_input, expected_query):
    """Return True only when a live visible result count reflects a filter."""
    query = str(expected_query or "").strip().casefold()
    if not query or str(current_input or "").strip().casefold() != query:
        return False
    match = re.search(r"\bShowing\s+(\d+)\s+of\s+(\d+)\b",
                      str(visible_text or ""), re.IGNORECASE)
    if not match:
        return False
    showing, total = int(match.group(1)), int(match.group(2))
    # Initial BoxerBase SSR says "Showing 78 of 78" even while only the
    # first 20 <tr> are rendered. Never mistake that for a completed search.
    return (0 <= showing < total) or total == 0
