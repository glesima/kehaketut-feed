import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from update_news import load_approved_groups

class NewsAudienceTests(unittest.TestCase):
    def test_editorial_metadata_has_valid_groups_only(self):
        config = json.loads((ROOT/"config/news_audiences.json").read_text(encoding="utf-8"))
        group_index = json.loads((ROOT/"config/content_groups.json").read_text(encoding="utf-8"))
        allowed = {g["id"] for g in group_index["groups"]}
        for article in config["articles"]:
            with self.subTest(article=article["url"]):
                self.assertTrue(article["url"].startswith("https://www.kehaketut.fi/uutiset/"))
                self.assertTrue(set(article["groups"]).issubset(allowed))
        self.assertIn("competitive", load_approved_groups()[
            "https://www.kehaketut.fi/uutiset/keha-ketut-kilpailivat-lokakuussa-t/"])

    def test_unknown_article_is_not_guessed(self):
        self.assertNotIn("https://www.kehaketut.fi/uutiset/not-tagged/",
                         load_approved_groups())

if __name__ == "__main__":
    unittest.main()
