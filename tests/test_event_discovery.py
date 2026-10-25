import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from event_discovery import (
  discover_event_links, event_id_from_url,
  match_public_boxer, parse_public_registrations
)

ROSTER = [
    {"id":"U2N_OOYxyFui","name":"Gleb Simanov"},
    {"id":"rLyNGj8sCoF7","name":"Josias Joseph Ndikumana"},
    {"id":"KyEKnjm-NRp4","name":"Daniela Taskila"}
]
CANONICAL = ["Riihimäen Kehä-Ketut ry","RIIHIMÄEN KEHÄ-KETUT"]


class PublicEventParsing(unittest.TestCase):
    def test_all_visible_event_links_without_duplicate(self):
        h = """<a href="/e/one">One</a><a href="/e/two">Two</a>
         <a href="/e/one">One again</a><a href="/fi/e/three">Third</a>
         <a href="https://wrong.example/e/xx">Blocked</a>"""
        self.assertEqual(
            len(discover_event_links(h,"https://fin.boxerbase.com/events",10)),3
        )
        self.assertEqual(event_id_from_url("https://boxerbase.com/fi/e/three"),"three")

    def test_registration_is_not_a_confirmed_bout(self):
        h = """<div>Showing 190 of 190</div><table><tr><th>Name</th><th>Club</th></tr>
        <tr><td><a href="/e/comp/participants/hello">Gleb Simanov</a></td>
        <td><a href="/o/1Le8shnOwPIW">Riihimäen Kehä-Ketut ry</a></td>
        <td>1988</td></tr></table>"""
        found,meta = parse_public_registrations(h,"https://boxerbase.com/e/comp/participants",ROSTER,CANONICAL)
        self.assertEqual(len(found),1)
        self.assertEqual(found[0]["status"],"registered")
        self.assertEqual(found[0]["boxer_id"],"U2N_OOYxyFui")
        self.assertNotIn("born",str(found))
        self.assertEqual(meta["coverage"],"limited_public_view")

    def test_wrong_club_does_not_count(self):
        h = """<table><tr><td><a href="/e/comp/participants/person">Gleb Simanov</a></td>
        <td>Other Boxing Club</td></tr></table>"""
        found,meta = parse_public_registrations(h,"https://boxerbase.com/e/comp/participants",ROSTER,CANONICAL)
        self.assertEqual(found,[])

    def test_known_duplicate_label_with_full_name_alias(self):
        h = """<table>
        <tr><td><a href="/e/comp/participants/p2">Josias Ndikumana</a></td><td>RIIHIMÄEN KEHÄ-KETUT</td></tr>
        </table>"""
        found,meta = parse_public_registrations(h,"https://boxerbase.com/e/comp/participants",ROSTER,CANONICAL)
        self.assertEqual(len(found),1)
        self.assertEqual(found[0]["boxer"],"Josias Joseph Ndikumana")

    def test_hidden_or_partial_list_never_claimed_complete(self):
        found,meta = parse_public_registrations("<p>Names are not yet published</p>","https://boxerbase.com/e/comp/participants",ROSTER,CANONICAL)
        self.assertEqual(found,[])
        self.assertEqual(meta["coverage"],"limited_public_view")


if __name__ == "__main__": unittest.main()
