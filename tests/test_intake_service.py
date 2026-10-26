"""Safety and idempotency tests for local unattended inbox intake."""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "media"))
import intake_service


class IntakeServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.incoming = self.root / "incoming"
        self.incoming.mkdir()
        self.spool = self.root / "private-spool"
        self.dbpath = self.root / "private-db" / "state.sqlite"
        self.db = intake_service.db_connect(self.dbpath)
        self.addCleanup(self.db.close)
        self.t = time.time()
        self.probe = patch.object(intake_service, "inspect_mp4", return_value={
            "duration_seconds": 90, "width": 1920, "height": 1080,
            "fps": 25.0, "codec": "h264", "audio": True
        })
        self.probe.start()
        self.addCleanup(self.probe.stop)

    def media(self, name="bout.mp4", data=b"representative-demo-video"):
        path = self.incoming / name
        path.write_bytes(data)
        os.utime(path, (self.t - 100, self.t - 100))
        return path

    def scan(self, when, assignments=None, ledger=None):
        return intake_service.scan_once(
            self.incoming, self.db, self.spool, assignments or {},
            ledger or {}, stable_seconds=5, now=when)

    def test_one_observation_not_processed(self):
        self.media()
        rows = self.scan(self.t)
        self.assertEqual(rows[0]["status"], "OBSERVING")
        self.assertEqual(list(self.spool.glob("*.json")), [])

    def test_second_observation_after_stability_creates_private_hold(self):
        source = self.media()
        original = source.read_bytes()
        self.scan(self.t)
        result = self.scan(self.t + 6)
        self.assertEqual(result[0]["status"], "HOLD")
        handoff = json.loads(next(self.spool.glob("*.json")).read_text())
        self.assertFalse(handoff["publication_ready"])
        self.assertIn("MISSING_EXPLICIT_EVENT_AND_BOUT_MAPPING", handoff["blockers"])
        self.assertIn("INDEPENDENT_RIGHTS_AND_OFFICIAL_RESULTS_CHECK_REQUIRED", handoff["blockers"])
        self.assertEqual(source.read_bytes(), original)

    def test_immediate_second_pass_still_waits(self):
        self.media()
        self.scan(self.t)
        self.assertEqual(self.scan(self.t + 1)[0]["status"], "WAIT_STABLE")

    def test_assignment_change_updates_handoff_without_reupload(self):
        self.media()
        self.scan(self.t)
        self.scan(self.t + 6)
        doc = {"bout.mp4": {"event_id": "hameenlinna2026", "bout_id": "16",
                             "kind": "full_bout", "approved": True}}
        rows = self.scan(self.t + 7, doc)
        self.assertEqual(rows[0]["status"], "HOLD")
        handoff = json.loads(next(self.spool.glob("*.json")).read_text())
        self.assertEqual(handoff["assignment"]["bout_id"], "16")
        self.assertNotIn("approved", handoff["assignment"])
        self.assertFalse(handoff["publication_ready"])

    def test_published_bout_blocks_reuse(self):
        self.media()
        mapping = {"bout.mp4": {"event_id": "hameenlinna2026",
                                 "bout_id": "33", "kind": "full_bout"}}
        ledger = {"published_bouts": [{"event_id": "hameenlinna2026", "bout_id": "33"}]}
        self.scan(self.t, mapping, ledger)
        rows = self.scan(self.t + 6, mapping, ledger)
        self.assertIn("ALREADY_PUBLISHED_BOUT_REVIEW_REUSE", rows[0]["blockers"])

    def test_identical_media_different_filename_is_deduplicated(self):
        self.media("a.mp4", b"same bytes")
        self.scan(self.t)
        self.scan(self.t + 6)
        self.media("b.mp4", b"same bytes")
        self.scan(self.t + 7)
        rows = self.scan(self.t + 14)
        b = next(x for x in rows if x["name"] == "b.mp4")
        self.assertIn("DUPLICATE_MEDIA_SHA256", b["blockers"])

    def test_modified_file_starts_new_stability_interval(self):
        path = self.media()
        self.scan(self.t)
        self.scan(self.t + 6)
        path.write_bytes(b"changed bytes")
        os.utime(path, (self.t - 100, self.t - 100))
        self.assertEqual(self.scan(self.t + 7)[0]["status"], "OBSERVING")
        self.assertEqual(self.scan(self.t + 8)[0]["status"], "WAIT_STABLE")

    def test_invalid_media_is_held_without_publication(self):
        self.media()
        self.probe.stop()
        with patch.object(intake_service, "inspect_mp4", side_effect=ValueError("bad")):
            self.scan(self.t)
            rows = self.scan(self.t + 6)
        self.assertEqual(rows[0]["status"], "HOLD_INVALID_MEDIA")
        self.assertEqual(list(self.spool.glob("*.json")), [])

    def test_non_mp4_and_symlink_ignored(self):
        (self.incoming / "notes.txt").write_text("ok")
        outside = self.root / "secret.mp4"
        outside.write_bytes(b"secret")
        (self.incoming / "notours.mp4").symlink_to(outside)
        self.assertEqual(self.scan(self.t), [])

    def test_file_permissions_private_posix(self):
        self.media()
        self.scan(self.t)
        self.scan(self.t + 6)
        if os.name == "posix":
            self.assertEqual(self.dbpath.stat().st_mode & 0o777, 0o600)
            self.assertEqual(self.spool.stat().st_mode & 0o777, 0o700)
            self.assertEqual(next(self.spool.glob("*.json")).stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()
