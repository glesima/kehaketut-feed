import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from editorial_news_triggers import suggest_stories, event_id

POLICY = json.loads((ROOT / "config/editorial_news_policy.json").read_text(encoding="utf-8"))
SM = "zdyYMbmXqIuV"
HAMEENLINNA = "d6jfSSe5nRpe"


def make_snapshot(event_id=SM, registrations=2, match_count=0):
    persons = [{"boxer_id": "ilo", "boxer": "Ilo Grönroos"},
               {"boxer_id": "kosmo", "boxer": "Kosmo Grönroos"},
               {"boxer_id": "another", "boxer": "Kolmas Ottelija"},
               {"boxer_id": "fourth", "boxer": "Neljäs Ottelija"},
               {"boxer_id": "fifth", "boxer": "Viides Ottelija"}]
    records = [
        dict(p, event_id=event_id, status="registered",
             current_visibility="previously_observed")
        for p in persons[:registrations]
    ]
    matches = [
        {"id": "bout-"+str(i), "event_url": "https://fin.boxerbase.com/e/"+event_id,
         "boxer": "Ilo Grönroos", "opponent": "Vastustaja", "result": "voitto",
         "decision": "3-2", "url": "https://fin.boxerbase.com/e/"+event_id+"/m/bout-"+str(i)}
        for i in range(match_count)
    ]
    return {
        "discovered_events": [{
            "id": event_id, "name": "Nuorten SM-kilpailut",
            "url": "https://fin.boxerbase.com/e/"+event_id, "date": "2026-11-06"
        }],
        "registrations": records,
        "matches": matches,
    }


class EditorialNewsPolicyTests(unittest.TestCase):
    def test_two_sm_registrants_yield_single_reviewable_candidate(self):
        result = suggest_stories(make_snapshot(), POLICY, today="2026-10-25")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["key"], SM+":preview")
        self.assertEqual(result[0]["participant_names"], ["Ilo Grönroos", "Kosmo Grönroos"])
        self.assertEqual(result[0]["status"], "needs_coach_confirmation")
        self.assertFalse(result[0]["publication_allowed"])

    def test_coach_confirmation_does_not_publish_or_send(self):
        result = suggest_stories(
            make_snapshot(), POLICY, today="2026-10-25",
            coach_confirmed_events=frozenset({SM}))
        self.assertEqual(result[0]["status"], "needs_editorial_approval")
        self.assertFalse(result[0]["publication_allowed"])

    def test_five_registration_routine_event_does_not_spam_news(self):
        snapshot = make_snapshot(event_id="ordinary_event", registrations=5)
        result = suggest_stories(snapshot, POLICY, today="2026-10-25")
        self.assertEqual(result, [])

    def test_one_registration_not_enough_for_sm_preview(self):
        self.assertEqual(suggest_stories(make_snapshot(registrations=1),
                                         POLICY, today="2026-10-25"), [])

    def test_many_matches_not_one_story_per_bout(self):
        snapshot = make_snapshot(match_count=4)
        result = suggest_stories(
            snapshot, POLICY, today="2026-11-09",
            results_complete_events=frozenset({SM}))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["key"], SM+":recap")
        self.assertEqual(len(result[0]["results"]), 4)
        self.assertFalse(result[0]["publication_allowed"])

    def test_not_closed_event_is_not_recap(self):
        self.assertEqual(suggest_stories(make_snapshot(match_count=2),
                                         POLICY, today="2026-11-09"), [])

    def test_no_result_no_recap(self):
        result = suggest_stories(make_snapshot(match_count=0), POLICY,
                                 today="2026-11-09",
                                 results_complete_events=frozenset({SM}))
        self.assertEqual(result, [])

    def test_published_coverage_prevents_duplicate_recap(self):
        snap = make_snapshot(event_id=HAMEENLINNA, match_count=4)
        # Event curated to test already-published coverage.
        special = dict(POLICY, editorial_events={
            **POLICY["editorial_events"],
            HAMEENLINNA: {"noteworthy": True}
        })
        result = suggest_stories(
            snap, special, today="2026-11-09",
            results_complete_events=frozenset({HAMEENLINNA}))
        self.assertEqual(result, [])

    def test_persistent_history_prevents_repeated_preview(self):
        result = suggest_stories(make_snapshot(), POLICY, today="2026-10-25",
                                 previously_proposed=frozenset({(SM, "preview")}))
        self.assertEqual(result, [])

    def test_bout_id_duplicates_do_not_duplicate_recap_results(self):
        snap = make_snapshot(match_count=2)
        snap["matches"].append(dict(snap["matches"][0]))
        result = suggest_stories(snap, POLICY, today="2026-11-09",
                                 results_complete_events=frozenset({SM}))
        self.assertEqual(len(result[0]["results"]), 2)

    def test_known_bout_without_published_result_is_not_recap(self):
        snap = make_snapshot()
        snap["matches"] = [{"id": "x", "event_url": "https://fin.boxerbase.com/e/"+SM,
                            "result": "vahvistettu ottelu"}]
        result = suggest_stories(snap, POLICY, today="2026-11-09",
                                 results_complete_events=frozenset({SM}))
        self.assertEqual(result, [])

    def test_known_boxerbase_event_id_normalized(self):
        self.assertEqual(event_id("https://fin.boxerbase.com/e/"+SM), SM)
        self.assertEqual(event_id("https://boxerbase.com/fi/e/"+SM+"/m/x"), SM)


if __name__ == "__main__":
    unittest.main()
