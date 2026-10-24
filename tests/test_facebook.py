import json
import unittest
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
class TestFacebookFeed(unittest.TestCase):
    def test_only_correct_brand(self):
        d=json.loads((BASE/"docs"/"facebook.json").read_text(encoding="utf-8"))
        self.assertEqual(d["brand_id"],7632678)
        self.assertEqual(d["facebook_page_id"],"160875127258478")
        self.assertTrue(d["posts"])
        self.assertTrue(all(x["url"].startswith("https://facebook.com/") for x in d["posts"]))
