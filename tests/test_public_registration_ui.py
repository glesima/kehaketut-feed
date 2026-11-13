import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from public_registration_ui import public_filter_is_applied


class PublicRegistrationSearchTests(unittest.TestCase):
    def test_ssr_first_twenty_not_a_search_result(self):
        # Real public Ruskiksen Skabat HTML has only 20 rows despite 78 of 78.
        self.assertFalse(public_filter_is_applied(
            "Participants Showing 78 of 78", "Riihimäen", "Riihimäen"))

    def test_real_live_filtered_five_results(self):
        self.assertTrue(public_filter_is_applied(
            "Participants Showing 5 of 78", "Riihimäen", "Riihimäen"))

    def test_genuine_zero_when_filtered_not_withdrawn(self):
        # No public club rows in current SM qualification tournament.
        self.assertTrue(public_filter_is_applied(
            "Participants Showing 0 of 29", "Riihimäen", "Riihimäen"))

    def test_hydration_can_reset_input(self):
        self.assertFalse(public_filter_is_applied(
            "Participants Showing 5 of 78", "", "Riihimäen"))

    def test_unrelated_query_or_missing_counter_rejected(self):
        self.assertFalse(public_filter_is_applied(
            "Participants Showing 5 of 78", "Hyvinkää", "Riihimäen"))
        self.assertFalse(public_filter_is_applied(
            "Participants. Loading...", "Riihimäen", "Riihimäen"))

    def test_empty_event_and_malformed_counts(self):
        self.assertTrue(public_filter_is_applied(
            "Showing 0 of 0", "Riihimäen", "Riihimäen"))
        self.assertFalse(public_filter_is_applied(
            "Showing 79 of 78", "Riihimäen", "Riihimäen"))


if __name__=="__main__":
    unittest.main()
