"""Offline, no-network checks for the RKK filming intake inventory."""
import importlib.util
import json
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

SRC = Path(__file__).with_name("filming_intake.py")
if not SRC.is_file():
    SRC = Path(__file__).resolve().parents[1] / "scripts" / "media" / "filming_intake.py"
spec = importlib.util.spec_from_file_location("filming_intake", SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
META = {"width": 848, "height": 478, "duration_seconds": 65.0, "fps": 25, "codec": "h264", "audio": True}

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        self.a = self.d / "a.mp4"
        self.a.write_bytes(b"fake-mp4-unique-1")
        os.utime(self.a, (1000, 1000))
    def tearDown(self):
        self.tmp.cleanup()
    def test_missing_assignment_holds(self):
        with patch.object(mod, "inspect_mp4", return_value=META):
            r = mod.inventory(self.d, {}, {}, settle_seconds=0, now=10000)
        self.assertFalse(r["publication_ready"])
        self.assertIn("MISSING_EXPLICIT_EVENT_AND_BOUT_MAPPING", r["files"][0]["reasons"])
    def test_verified_mapping_still_needs_rights(self):
        with patch.object(mod, "inspect_mp4", return_value=META):
            r = mod.inventory(self.d, {"a.mp4":{"event_id":"e2026","bout_id":"16","kind":"full_bout"}}, {}, settle_seconds=0, now=10000)
        self.assertEqual(r["mapped_event_counts"], {"e2026": 1})
        self.assertIn("INDEPENDENT_FILMING_AND_PUBLICATION_RIGHTS_CHECK_REQUIRED", r["files"][0]["reasons"])
    def test_already_published_flags_reuse(self):
        a={"a.mp4":{"event_id":"e2026","bout_id":"16","kind":"full_bout"}}
        l={"published_bouts":[{"event_id":"e2026","bout_id":"16"}]}
        with patch.object(mod, "inspect_mp4", return_value=META):
            r=mod.inventory(self.d,a,l,settle_seconds=0,now=10000)
        self.assertTrue(any("ALREADY_HAS_PUBLISHED" in x for x in r["files"][0]["reasons"]))
    def test_duplicate_content_holds(self):
        b=self.d/"b.mp4";b.write_bytes(self.a.read_bytes());os.utime(b,(1000,1000))
        with patch.object(mod,"inspect_mp4",return_value=META):
            r=mod.inventory(self.d,{}, {}, settle_seconds=0,now=10000)
        self.assertTrue(any("DUPLICATE_MEDIA_SHA256" in x for x in r["files"][1]["reasons"]))
    def test_pending_file_is_not_opened(self):
        os.utime(self.a,(9900,9900))
        with patch.object(mod,"inspect_mp4",side_effect=AssertionError("must not open while writing")):
            r=mod.inventory(self.d,{}, {},settle_seconds=120,now=10000)
        self.assertIn("WAIT_FOR_UPLOAD_TO_SETTLE",r["files"][0]["reasons"])
    def test_reject_uploader_approved_as_authorization(self):
        a={"a.mp4":{"event_id":"e2026","bout_id":"16","kind":"full_bout","approved":True}}
        with patch.object(mod,"inspect_mp4",return_value=META):
            r=mod.inventory(self.d,a,{},settle_seconds=0,now=10000)
        self.assertFalse(r["publication_ready"])
        self.assertIn("INDEPENDENT_FILMING_AND_PUBLICATION_RIGHTS_CHECK_REQUIRED",r["files"][0]["reasons"])
    def test_unsupported_mapping_kind_holds(self):
        a={"a.mp4":{"event_id":"e2026","bout_id":"16","kind":"public_now"}}
        with patch.object(mod,"inspect_mp4",return_value=META):
            r=mod.inventory(self.d,a,{},settle_seconds=0,now=10000)
        self.assertIn("MISSING_OR_INVALID_EVENT_BOUT_KIND",r["files"][0]["reasons"])
    def test_bad_media_probe_holds(self):
        with patch.object(mod,"inspect_mp4",side_effect=ValueError("corrupt")):
            r=mod.inventory(self.d,{}, {},settle_seconds=0,now=10000)
        self.assertTrue(any("MEDIA_READ_OR_PROBE_FAILED" in x for x in r["files"][0]["reasons"]))
    def test_no_transmission_code(self):
        text=SRC.read_text(encoding="utf-8")
        for x in ("requests.post(", "httpx.", "createScheduledPost(", "dropbox.upload"):
            self.assertNotIn(x,text)
    def test_cli_outputs_report(self):
        with patch.object(mod, "inspect_mp4", return_value=META):
            p=self.d / "report.json"
            self.assertEqual(mod.cli(["--folder",str(self.d),"--output",str(p),"--settle-seconds","0"]),0)
            self.assertIn("RKK_PRIVATE_VIDEO_INTAKE_V1",p.read_text())
if __name__ == "__main__": unittest.main()

