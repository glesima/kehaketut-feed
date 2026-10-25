import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from update import parse_club,parse_profile,match_links,parse_match,event_urls_from_index,prefer_alias_stats,parse_event_date,parse_official_outcome

class TestPublicViews(unittest.TestCase):
    def test_club_table(self):
        html='''<table><tr><th>First Name</th><th>Last Name</th><th>Gender</th><th>Matches</th></tr>
        <tr><td><a href="/boxer/U2N_OOYxyFui">Gleb</a></td><td><a href="/boxer/U2N_OOYxyFui">Simanov</a></td><td>Male</td><td>3</td></tr>
        <tr><td><a href="/boxer/vK0bN2sPxnbo">Simo</a></td><td>Pöyry</td><td>Male</td><td>2</td></tr>
        </table>'''
        b=parse_club(html,'https://boxerbase.com/o/1Le8shnOwPIW/boxers')
        self.assertEqual(b[0]['name'],'Gleb Simanov')
        self.assertEqual(b[0]['matches'],3)
        self.assertEqual(b[1]['name'],'Simo Pöyry')

    def test_confirmed_club_not_duplicate(self):
        from update import CONFIG
        self.assertEqual(CONFIG["club_id"], "1Le8shnOwPIW")
        self.assertEqual(CONFIG["club_names"], ["Riihimäen Kehä-Ketut ry"])
    def test_multiword_first_name(self):
        html='''<table><tr><td><a href="/boxer/rLyNGj8sCoF7">Josias Joseph</a></td><td>Ndikumana</td><td>Male</td><td>0</td></tr></table>'''
        parsed=parse_club(html,'https://boxerbase.com/o/1Le8shnOwPIW/boxers')
        self.assertEqual(parsed[0]['name'],'Josias Joseph Ndikumana')
    def test_verified_alias_event_is_allowed(self):
        html='''<html><head><title>Gleb Simanov vs Sampo Paananen results at Event</title></head>
        <body><a href="/boxer/h9XYEbAs3Py4">Gleb Simanov RIIHIMÄEN KEHÄ-KETUT</a>
        <a href="/boxer/xx">Sampo Paananen Oiva Boxing</a><div>Winner Blue Sampo Paananen 5-0</div></body></html>'''
        event={'name':'Hämeenlinna','date':'2026-10-24','url':'https://boxerbase.com/e/abc','allow_alias_club_on_bouts':True,'verified_as_duplicate_label':'RIIHIMÄEN KEHÄ-KETUT'}
        got=parse_match(html,'https://boxerbase.com/e/abc/m/xyz',[{'name':'Gleb Simanov'}],event)
        self.assertEqual(got['result'],'tappio')
    def test_only_more_complete_temporary_alias_used(self):
        self.assertTrue(prefer_alias_stats({"matches":0},{"matches":1}))
        self.assertFalse(prefer_alias_stats({"matches":1},{"matches":1}))
        self.assertFalse(prefer_alias_stats({"matches":5},{"matches":1}))
        self.assertFalse(prefer_alias_stats({"matches":0},{"matches":None}))

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
        <body><a href="/boxer/U2N_OOYxyFui">Gleb Simanov Riihimäen Kehä-Ketut ry</a>
        <a href="/boxer/xx">Sampo Paananen Oiva Boxing</a><div>Winner Blue Sampo Paananen 5-0</div></body></html>'''
        boxers=[{'name':'Gleb Simanov'}]
        event={'name':'Hämeenlinnan juhlakisat','date':'2026-10-24','url':'https://fin.boxerbase.com/e/abc'}
        got=parse_match(html,'https://fin.boxerbase.com/e/abc/m/eqMxgdF-ilSr',boxers,event)
        self.assertEqual(got['result'],'tappio')
        self.assertEqual(got['decision'],'5-0')
        self.assertEqual(got['opponent'],'Sampo Paananen')
    def test_wrong_duplicate_club_is_rejected(self):
        html='''<html><head><title>Gleb Simanov vs Sampo Paananen results at Test</title></head><body>
        <a href="/boxer/h9XYEbAs3Py4">Gleb Simanov RIIHIMÄEN KEHÄ-KETUT</a>
        <a href="/boxer/xx">Sampo Paananen Other club</a><div>Winner Blue Sampo Paananen 5-0</div></body></html>'''
        result=parse_match(html,'https://boxerbase.com/e/abc/m/xyz',[{'name':'Gleb Simanov'}],{'name':'Test','date':'2026-10-24','url':'https://boxerbase.com/e/abc'})
        self.assertIsNone(result)
    def test_parse_result_win(self):
        html='''<html><head><title>Rami Vuori vs Hans Guttorm results at Tampere</title></head>
        <body><a href="/boxer/xx">Rami Vuori Riihimäen Kehä-Ketut ry</a>
        <a href="/boxer/yy">Hans Guttorm Turun Weikot</a><div>Winner Red Rami Vuori 3-0</div></body></html>'''
        got=parse_match(html,'https://boxerbase.com/e/abc/m/m2',[{'name':'Rami Vuori'}],{'name':'Nääsnyrkkeilyt','date':'2026-10-10','url':'https://boxerbase.com/e/abc'})
        self.assertEqual(got['result'],'voitto')
    def test_multiday_event_start(self):
        html='<h1>Nuorten SM-kilpailut</h1><div>Fri, November 6 – Sun, November 8, 2026</div>'
        self.assertEqual(parse_event_date(html),'2026-11-06')
    def test_single_day_event(self):
        html='<h1>Juhlakilpailut</h1><div>Sat, October 24, 2026</div>'
        self.assertEqual(parse_event_date(html),'2026-10-24')
    def test_result_methods_and_sides(self):
        event={'name':'Kisapäivä','date':'2026-10-24','url':'https://boxerbase.com/e/t'}
        for code,expected,round_num in [
            ("RSC R2","RSC",2),("RSC-I R3","RSC-I",3),
            ("KO R1","KO",1),("ABD R2","ABD",2),
            ("WO","WO",None),("DQ R2","DQ",2),
            ("RSC-H R3","RSC-H",3),("RET R1","RET",1),
        ]:
            with self.subTest(code=code):
                html=f'''<html><head><title>Gleb Simanov vs Opponent results at Event</title></head>
                <body><a href="/boxer/U2N_OOYxyFui">Gleb Simanov Riihimäen Kehä-Ketut ry</a>
                <a href="/boxer/xx">Opponent Another Club</a>
                <span>Winner Blue • {code}</span></body></html>'''
                got=parse_match(html,'https://boxerbase.com/e/t/m/abc',
                    [{'name':'Gleb Simanov'}],event)
                self.assertEqual(got['result'],'tappio')
                self.assertEqual(got['method'],expected)
                self.assertEqual(got['round'],round_num)
                self.assertEqual(got['boxer_corner'],'red')
                self.assertEqual(got['red_boxer'],'Gleb Simanov')
                self.assertEqual(got['blue_boxer'],'Opponent')
                self.assertEqual(got['winner_corner'],'blue')
                self.assertEqual(got['bout_contested'],expected!='WO')

    def test_winner_blue_club_boxer_is_a_win(self):
        h='''<html><head><title>Other Fighter vs Rami Vuori results at Cup</title></head>
         <body><a href="/boxer/a">Other Fighter Another Club</a>
         <a href="/boxer/b">Rami Vuori Riihimäen Kehä-Ketut ry</a>
         Winner Blue • 3-0</body></html>'''
        got=parse_match(h,'https://boxerbase.com/e/x/m/y',
              [{'name':'Rami Vuori'}],{'name':'Cup','date':'2026-10-25','url':'https://boxerbase.com/e/x'})
        self.assertEqual(got['result'],'voitto')
        self.assertEqual(got['boxer_corner'],'blue')
        self.assertEqual(got['winner_corner'],'blue')
        self.assertEqual(got['method'],'PTS')

    def test_without_verified_result_not_a_win(self):
        for body in ['Coming soon','Winner Red','A boxer red']:
            with self.subTest(body=body):
                got=parse_official_outcome(body)
                self.assertIsNone(got['winner_corner'])
                self.assertIsNone(got['method'])

    def test_event_index(self):
        html='<a href="/e/abc">Event A</a><a href="/e/abc">Event A</a><a href="/e/def">Event B</a>'
        self.assertEqual(len(event_urls_from_index(html,'https://fin.boxerbase.com/',8)),2)

if __name__=='__main__':unittest.main()
