"""Regression tests for Yhdistysavain news dates embedded in article headlines."""
import sys
import unittest
from datetime import date
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from update_news import extract_news, split_news_record


def anchor(html):
    return BeautifulSoup(html, "html.parser").select_one("a")


class NewsTitleDateTests(unittest.TestCase):
    def test_cancelled_training_title_retained_and_correct_publication_date(self):
        html = """<a href="/uutiset/harjoitukset-peruttu-27-29-10-2026/">
          Harjoitukset peruttu 27.–29.10.2026 26.10.2026
          Riihimäen Kehä-Kettujen harjoitukset Kamppailukeskuksessa peruttu.
        </a>"""
        items = extract_news(html)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Harjoitukset peruttu 27.–29.10.2026")
        self.assertEqual(items[0]["date"], "26.10.2026")
        self.assertIn("Riihimäen", items[0]["excerpt"])

    def test_structured_publish_date_used_when_title_has_same_date(self):
        html = """<a href="/uutiset/ottelut-26102026/">
          <strong>Kilpailut 26.10.2026</strong>
          <time datetime="2026-10-26">26.10.2026</time>
          <span>Kolme ottelua.</span>
        </a>"""
        item = extract_news(html)[0]
        self.assertEqual(item["title"], "Kilpailut 26.10.2026")
        self.assertEqual(item["date"], "26.10.2026")

    def test_original_alkaa_heuristic_preserved(self):
        html = """<a href="/uutiset/nyrkkeilykoulu2026/">
           Nyrkkeilykoulu alkaa tiistaina 13.1.2026 klo 17 30.12.2025
           Tervetuloa harjoittelemaan.
        </a>"""
        result = extract_news(html)[0]
        self.assertEqual(result["date"], "30.12.2025")
        self.assertIn("13.1.2026", result["title"])

    def test_text_body_dates_not_mistaken_for_publish_date(self):
        html = """<a href="/uutiset/raportti-lokakuusta/">
           Kehä-Ketut kilpailivat lokakuussa 25.10.2026
           Riihimäen Kehä-Kettujen nyrkkeilijöitä nähtiin lokakuussa
           kilpailuissa Tampereella 10.10.2026 ja Hämeenlinnassa 24.10.2026.
        </a>"""
        result = extract_news(html)[0]
        self.assertEqual(result["date"], "25.10.2026")
        self.assertEqual(result["title"], "Kehä-Ketut kilpailivat lokakuussa")

    def test_structured_date_node_outweighs_future_date_in_title(self):
        html = """<a href="/uutiset/harjoitukset-peruttu/">
          <h2>Harjoitukset peruttu 27.–29.10.2026</h2>
          <div class="news-date">26.10.2026</div>
          <p>Kaupungin peruuttamat harjoitusvuorot.</p>
        </a>"""
        result = extract_news(html)[0]
        self.assertEqual(result["date"], "26.10.2026")
        self.assertIn("27.–29.10.2026", result["title"])

    def test_single_publication_date_still_ok(self):
        html = """<a href="/uutiset/paivan-uutinen/">Uutta salilla 26.10.2026
          Ohjelma on julkaistu.</a>"""
        result = extract_news(html)[0]
        self.assertEqual(result["title"], "Uutta salilla")
        self.assertEqual(result["date"], "26.10.2026")

    def test_no_date_cannot_be_rendered(self):
        html = """<a href="/uutiset/ilman-paivaa/">Tämä artikkeli ei sisällä julkaisuaikaa</a>"""
        self.assertEqual(extract_news(html), [])

    def test_explicit_today_for_relative_future_date(self):
        node = anchor('<a href="/uutiset/t/">Harjoitukset peruttu 27.–29.10.2026 26.10.2026 Lisää tietoa.</a>')
        record = split_news_record(node.get_text(" ", strip=True), node, today=date(2026, 10, 26))
        self.assertEqual(record[:2], ("Harjoitukset peruttu 27.–29.10.2026", "26.10.2026"))


if __name__ == "__main__":
    unittest.main()
