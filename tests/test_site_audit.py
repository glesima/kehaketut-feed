import sys
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from site_audit import (
    normalized_public_url, extract_internal_links, inspect_page,
    crawl, markdown_report
)

class FakeResponse:
    def __init__(self,url,html="",code=200,ctype="text/html"):
        self.url=url;self.status_code=code;self.headers={"content-type":ctype}
        self.content=html.encode("utf-8");self.text=html


class SiteAuditTests(unittest.TestCase):
    def test_private_and_external_urls_never_followed(self):
        bad=[
          "https://google.com/", "http://www.kehaketut.fi/",
          "/hallitus/", "/jasenet/", "/admin/", "/login/",
          "/uutiset/?auth=s3cr3t", "/member?password=abc",
          "https://evil.example/uutiset/", "//evil.example/",
          "/files/results.pdf"
        ]
        for url in bad:
            with self.subTest(url=url):
                self.assertIsNone(normalized_public_url(url))
        self.assertEqual(
           normalized_public_url("https://kehaketut.fi/harjoittelu/"),
           "https://www.kehaketut.fi/harjoittelu/"
        )

    def test_links_deduplicate_and_ignore_private(self):
        html='''<a href="/harjoittelu/">Training</a>
        <a href="/harjoittelu/">Repeat</a>
        <a href="/seura/seuran-historia/">History</a>
        <a href="/hallitus/">private</a>
        <a href="https://other.example/"></a>'''
        found=extract_internal_links(html,"https://www.kehaketut.fi/")
        self.assertEqual(len(found),2)

    def test_editorial_audit_flags_without_rewriting_content(self):
        h='''<html><head><title>Etusivu</title></head><body>
         <main><h1>Kehä-Ketut</h1>
          <p>Nyrkkeilykoulu aloitetaan 25.8.2026</p>
          <p>Tulevat ottelut eivät vielä päivity automaattisesti.</p>
         </main></body></html>'''
        rec=inspect_page(h,"https://www.kehaketut.fi/")
        self.assertIn("stale_august_2026_course_on_home",rec["warnings"])
        self.assertIn("outdated_automation_claim_on_home",rec["warnings"])
        self.assertEqual(rec["h1"],"Kehä-Ketut")

    def test_archive_preserved(self):
        html='<main><h1>2002</h1><p>Pasi Silvennoinen 2002</p></main>'
        rec=inspect_page(html,"https://www.kehaketut.fi/harjoittelu/kilpailija-harrastajaryhma/tuloksia/2002/")
        self.assertEqual(rec["kind"],"historialliset_tulokset")
        self.assertFalse(any("stale" in q for q in rec["warnings"]))

    def test_bounded_public_crawl(self):
        base="https://www.kehaketut.fi"
        site={
          "/":'<html><body><main><h1>RKK</h1><a href="/harjoittelu/">Harjoittelu</a><a href="/hallitus/">Salainen</a></main></body></html>',
          "/harjoittelu/":'<html><main><h1>Harjoittelu</h1><a href="/seura/">Seura</a></main></html>',
          "/seura/":'<html><main><h1>Seura</h1></main></html>'
        }
        fetched=[]
        def mock_request(url,**kwargs):
            if url.endswith("/robots.txt"):return FakeResponse(url,code=404)
            path=urlparse(url).path
            fetched.append(path)
            return FakeResponse(url,site[path])
        report=crawl(max_pages=5,sleep=0,request=mock_request)
        self.assertEqual(report["scanned"],3)
        self.assertEqual(report["pending_queued"],0)
        self.assertNotIn("/hallitus/",fetched)
        self.assertIn("## Sivukohtaiset havainnot",markdown_report(report))

if __name__=="__main__":
    unittest.main()
