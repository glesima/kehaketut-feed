"""Public news RSS tests: no cross-posting or duplicate article churn."""
import sys
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from news_rss import build_rss

ART = "https://www.kehaketut.fi/uutiset/keha-ketut-kilpailivat-lokakuussa-t/"
class NewsRssTests(unittest.TestCase):
    def fixture(self, now="2026-10-25T20:00:00Z"):
        return {
            "generated_at":now,
            "items":[
                {"url":ART,"title":"Kehä-Ketut kilpailivat lokakuussa",
                 "date":"25.10.2026","excerpt":"Kaksi kilpailua.",
                 "groups":["competitive"]},
                {"url":ART,"title":"Same duplicate","date":"25.10.2026"},
                {"url":"https://evil.example/uutiset/wrong/",
                 "title":"Outside site","date":"25.10.2026"},
                {"url":"https://www.kehaketut.fi/uutiset/vuosikokous-2026-2/",
                 "title":"Vuosikokous","date":"19.2.2026",
                 "groups":["general","other"]},
            ]
        }

    def test_published_news_only_and_stable_guids(self):
        raw = build_rss(self.fixture())
        root = ET.fromstring(raw)
        items=root.findall("channel/item")
        self.assertEqual(len(items),2)
        self.assertEqual(items[0].findtext("guid"),ART)
        self.assertEqual(items[0].find("guid").get("isPermaLink"),"true")
        self.assertEqual(items[0].findtext("category"),"Kilpanyrkkeily")
        self.assertEqual(items[1].findtext("category"),"Koko seura")
        self.assertNotIn(b"evil.example",raw)

    def test_generated_at_change_does_not_republish_old_post(self):
        a=build_rss(self.fixture("2026-10-25T20:00:00Z"))
        b=build_rss(self.fixture("2026-10-26T08:00:00Z"))
        self.assertEqual(a,b)

    def test_empty_not_overwritten(self):
        with self.assertRaises(ValueError):
            build_rss({"items":[]})
        with self.assertRaises(ValueError):
            build_rss({"items":[{"url":"https://example.com/not-news",
                                 "date":"25.10.2026","title":"Bad"}]})

    def test_escapes_text_and_rejects_invalid_dates(self):
        raw=build_rss({"items":[{"url":ART,"date":"25.10.2026",
            "title":"Test <päivitys> & julkaisu", "excerpt":"Lyhyt <testi>"}]})
        root=ET.fromstring(raw)
        self.assertEqual(root.findtext("channel/item/title"),
                         "Test <päivitys> & julkaisu")
        self.assertIn(b"&lt;",raw)

    def test_no_browser_media_or_app_approval_calls(self):
        content=(ROOT/"scripts/news_rss.py").read_text(encoding="utf-8")
        self.assertNotIn("Metricool",content)
        self.assertNotIn("send_email",content)
        self.assertNotIn("autoPublish",content)

if __name__ == "__main__":
    unittest.main()
