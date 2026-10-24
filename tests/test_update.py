import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from update import parse_club,parse_profile,match_links,parse_match,event_urls_from_index

class TestPublicViews(unittest.TestCase):
    def test_club_table(self):
        html='''<table><tr><th>First Name</th><th>Last Name</th><th>Gender</th><th>Matches</th></tr>
        <tr><td><a href="/boxer/h9XYEbAs3Py4">Gleb</a></td><td><a href="/boxer/h9XYEbAs3Py4">Simanov</a></td><td>Male</td><td>3</td></tr>
        <tr><td><a href="/boxer/PxXnRMHDTclP">Simo</a></td><td>Pöyry</td><td>Male</td><td>2</td></tr>
        </table>'''
        b=parse_club(html,'https://boxerbase.com/o/mZjkT0LW248X/boxers')
        self.assertEqual(b[0]['name'],'Gleb Simanov')
        self.assertEqual(b[0]['matches'],3)
        self.assertEqual(b[1]['name'],'Simo Pöyry')
    def test_roster_missing_fails_safe(self):
        with self.assertRaises(ValueError):parse_club('<h2>Not Found</h2>','https://boxerbase.com/o/x/boxers')
    def test_profile(self):
        r=parse_profile('<div>Gleb Simanov 3 Matches 0 Wins 3 Losses</div>')
        self.assertEqual(r,{'matches':3,'wins':0,'losses':3})
    def test_event_link_extraction_and_dedup(self):
        h='<a href="/e/abc/m/one">Gleb Simanov vs Sampo Paananen</a> <a href="/e/abc/m/two">Other vs Player</a>'
        rs=match_links(h,'https://fin.boxerbase.com/e/abc/matches',['Gleb Simanov'])
        self.assertEqual(rs,['https://fin.boxerbase.com/e/abc/m/one'])
    def test_parse_result_loss(self):
        html='''<html><head><title>Gleb Simanov vs Sampo Paananen results at Hämeenlinna</title></head>
        <body><a href="/boxer/h9XYEbAs3Py4">Gleb Simanov RIIHIMÄEN KEHÄ-KETUT</a>
        <a href="/boxer/xx">Sampo Paananen Oiva Boxing</a><div>Winner Blue Sampo Paananen 5-0</div></body></html>'''
        boxers=[{'name':'Gleb Simanov'}]
        event={'name':'Hämeenlinnan juhlakisat','date':'2026-10-24','url':'https://fin.boxerbase.com/e/abc'}
        got=parse_match(html,'https://fin.boxerbase.com/e/abc/m/eqMxgdF-ilSr',boxers,event)
        self.assertEqual(got['result'],'tappio')
        self.assertEqual(got['decision'],'5-0')
        self.assertEqual(got['opponent'],'Sampo Paananen')
    def test_parse_result_win(self):
        html='''<html><head><title>Rami Vuori vs Hans Guttorm results at Tampere</title></head>
        <body><a href="/boxer/xx">Rami Vuori Riihimäen Kehä-Ketut ry</a>
        <a href="/boxer/yy">Hans Guttorm Turun Weikot</a><div>Winner Red Rami Vuori 3-0</div></body></html>'''
        got=parse_match(html,'https://boxerbase.com/e/abc/m/m2',[{'name':'Rami Vuori'}],{'name':'Nääsnyrkkeilyt','date':'2026-10-10','url':'https://boxerbase.com/e/abc'})
        self.assertEqual(got['result'],'voitto')
    def test_event_index(self):
        html='<a href="/e/abc">Event A</a><a href="/e/abc">Event A</a><a href="/e/def">Event B</a>'
        self.assertEqual(len(event_urls_from_index(html,'https://fin.boxerbase.com/',8)),2)

if __name__=='__main__':unittest.main()
