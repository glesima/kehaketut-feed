import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"scripts"))
from registration_retention import reconcile_registrations

BASE={
 "event_id":"zdyYMbmXqIuV",
 "event_date":"2026-11-06",
 "status":"registered",
 "participant_url":"https://fin.boxerbase.com/e/zdyYMbmXqIuV/participants/a",
 "registered_club":"Riihimäen Kehä-Ketut ry",
 "observed_at":"2026-10-25T19:30:41Z",
}
ROSTER=[{"id":"ilo","name":"Ilo Grönroos"},{"id":"kosmo","name":"Kosmo Grönroos"}]
CANONICAL=["Riihimäen Kehä-Ketut ry"]

class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.old=[
            dict(BASE, boxer="Ilo Grönroos",boxer_id="ilo"),
            dict(BASE, boxer="Kosmo Grönroos",boxer_id="kosmo")
        ]

    def test_zero_from_incomplete_page_keeps_verified_entries(self):
        result=reconcile_registrations(self.old,[],ROSTER,CANONICAL,"2026-10-25")
        self.assertEqual(len(result),2)
        self.assertTrue(all(r["current_visibility"]=="previously_observed" for r in result))

    def test_refound_entries_are_marked_current(self):
        result=reconcile_registrations(self.old,[self.old[0]],ROSTER,CANONICAL,"2026-10-25")
        self.assertEqual(len(result),2)
        self.assertEqual(next(x for x in result if x["boxer_id"]=="ilo")["current_visibility"],
                         "verified_in_latest_public_search")
        self.assertEqual(next(x for x in result if x["boxer_id"]=="kosmo")["current_visibility"],
                         "previously_observed")

    def test_stale_event_expires(self):
        result=reconcile_registrations(self.old,[],ROSTER,CANONICAL,"2026-11-11")
        self.assertEqual(result,[])

    def test_unknown_club_fighter_is_not_accepted(self):
        bad=dict(BASE, boxer="Unknown",boxer_id="not-on-roster")
        result=reconcile_registrations([], [bad],ROSTER,CANONICAL,"2026-10-25")
        self.assertEqual(result,[])

if __name__=="__main__":
    unittest.main()
