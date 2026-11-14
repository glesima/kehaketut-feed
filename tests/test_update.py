import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from update import parse_club,parse_profile,match_links,parse_match,event_urls_from_index,prefer_alias_stats,parse_event_date,parse_official_outcome,suppress_conflicting_totals,public_match_session_urls

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
        self.assertEqual(CONFIG["club_id"], "mZjkT0LW248X")
        self.assertEqual(CONFIG["club_names"], ["RIIHIMÄEN KEHÄ-KETUT", "Riihimäen Kehä-Ketut ry"])
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
    def test_profile_totals_conflict_hidden(self):
        b=suppress_conflicting_totals({"matches":4,"wins":0,"losses":5})
        self.assertIsNone(b["wins"])
        self.assertIsNone(b["losses"])
        self.assertEqual(b["matches"],4)
        self.assertEqual(b["stats_quality"],"provider_counts_conflict")

    def test_conflicting_zero_matches_is_not_a_zero_win_loss(self):
        boxer=suppress_conflicting_totals({"matches":0,"wins":1,"losses":0})
        self.assertEqual(boxer["matches"],0)
        self.assertIsNone(boxer["wins"])
        self.assertIsNone(boxer["losses"])
        self.assertEqual(boxer["stats_quality"],"provider_counts_conflict")
        clean=suppress_conflicting_totals({"matches":0,"wins":None,"losses":None})
        self.assertNotIn("stats_quality",clean)

    def test_fallback_club_suffix_matches_without_weakening_identity(self):
        event={"name":"Test","date":"2026-10-24","url":"https://fin.boxerbase.com/e/abc"}
        roster=[{"name":"Gleb Simanov"}]
        prefix='<html><head><title>Event results overview</title></head><body>'
        suffix='<div>Winner Blue • 5-0</div></body></html>'
        approved=prefix+(
            '<a href="/boxer/a">Gleb Simanov (Riihimäen Kehä-Ketut ry)</a>'
            '<a href="/boxer/b">Sampo Paananen Oiva Boxing</a>'
        )+suffix
        got=parse_match(approved,"https://fin.boxerbase.com/e/abc/m/abc",roster,event)
        self.assertIsNotNone(got)
        self.assertEqual(got["boxer"],"Gleb Simanov")
        self.assertEqual(got["result"],"tappio")
        # A similar-name club must never provide identity verification.
        wrong=prefix+(
            '<a href="/boxer/a">Gleb Simanov Riihimäen Kehä-Ketut Juniorit</a>'
            '<a href="/boxer/b">Sampo Paananen Oiva Boxing</a>'
        )+suffix
        self.assertIsNone(parse_match(wrong,"https://fin.boxerbase.com/e/abc/m/wrong",roster,event))
        # Another athlete must not match by a substring.
        other=prefix+(
            '<a href="/boxer/a">Gleb Simanovinen Riihimäen Kehä-Ketut ry</a>'
            '<a href="/boxer/b">Sampo Paananen Oiva Boxing</a>'
        )+suffix
        self.assertIsNone(parse_match(other,"https://fin.boxerbase.com/e/abc/m/other",roster,event))

    def test_2026_kempele_sm_verified_results_retained(self):
        """Provider-published semifinal and final must survive subsequent refreshes."""
        import json
        from update import ROOT
        feed=json.loads((ROOT/"docs"/"data.json").read_text(encoding="utf-8"))
        bouts={m["id"]:m for m in feed["matches"]}
        expected={
            "nrAXlpdEXsze":("Ilo Grönroos","Kevin-Kristjan Veskus","voitto","5-0"),
            "T8SUpZo9ejpR":("Kosmo Grönroos","Otto Elias Mielonen","tappio","5-0"),
        }
        for match_id,facts in expected.items():
            with self.subTest(match=match_id):
                self.assertIn(match_id,bouts)
                m=bouts[match_id]
                self.assertEqual((m["boxer"],m["opponent"],m["result"],m["decision"]),facts)
                self.assertEqual(m["event_date"],"2026-11-07")
                self.assertEqual(m["event_url"],"https://fin.boxerbase.com/e/zdyYMbmXqIuV")
                self.assertEqual(m["boxer_id"],next(b["id"] for b in feed["boxers"] if b["name"]==facts[0]))
                self.assertTrue(m["url"].startswith("https://fin.boxerbase.com/fi/e/zdyYMbmXqIuV/m/"))
        self.assertEqual(sum(m["id"]=="nrAXlpdEXsze" for m in feed["matches"]),1)

    def test_profile_totals_consistent_kept(self):
        b=suppress_conflicting_totals({"matches":11,"wins":6,"losses":5})
        self.assertEqual((b["matches"],b["wins"],b["losses"]),(11,6,5))
        self.assertNotIn("stats_quality",b)

    def test_profile(self):
        r=parse_profile('<div>Gleb Simanov 3 Matches 0 Wins 3 Losses</div>')
        self.assertEqual(r,{'matches':3,'wins':0,'losses':3})
    def test_public_multisession_links_from_default_sunday_page(self):
        base="https://fin.boxerbase.com/e/pqlPYS5YEfAR/matches"
        current='''<h1>Ruskiksen Skabat</h1>
        <a href="/e/pqlPYS5YEfAR/matches?t=pRj18GNRKmds">Saturday 11:00</a>
        <a href="/e/pqlPYS5YEfAR/matches?t=JD9uNvLGV2cq">Sunday 11:00</a>
        <a href="/e/pqlPYS5YEfAR/m/other">Sampo Paananen vs Aksa Mäkelä</a>'''
        saturday='''<a href="/e/pqlPYS5YEfAR/m/zoBIpK4vq9fH">
                      Amir Elyasi vs Otso Västilä</a>
                     <a href="/e/pqlPYS5YEfAR/m/K0Qn14-9VOz7">
                      Daniela Taskila vs Wilma Yliluoma</a>'''
        names=["Otso Västilä","Daniela Taskila"]
        self.assertEqual(match_links(current,base,names),[],
                         "Plain URL's next-session-only SSR must not hide finished bouts")
        links=public_match_session_urls(current,base)
        self.assertEqual(links,[
            base+"?t=pRj18GNRKmds",base+"?t=JD9uNvLGV2cq"
        ])
        self.assertEqual(match_links(saturday,links[0],names),[
            "https://fin.boxerbase.com/e/pqlPYS5YEfAR/m/zoBIpK4vq9fH",
            "https://fin.boxerbase.com/e/pqlPYS5YEfAR/m/K0Qn14-9VOz7"
        ])

    def test_public_session_links_reject_cross_event_malicious_and_duplicate(self):
        base="https://fin.boxerbase.com/e/pqlPYS5YEfAR/matches"
        h='''<a href="?t=pRj18GNRKmds">Saturday</a>
        <a href="?t=pRj18GNRKmds">same again</a>
        <a href="?t=JD9uNvLGV2cq">Sunday</a>
        <a href="https://evil.example/e/pqlPYS5YEfAR/matches?t=evil">evil</a>
        <a href="/e/unrelated/matches?t=another">other event</a>
        <a href="?t=good%26bad=x">injected</a>
        <a href="?t=abc">too short</a>
        <a href="?t=legit&t=second">multiple</a>
        <a href="?t=legit&auth=secret">extra query</a>
        <a href="?t=legit#fragment">fragment</a>'''
        self.assertEqual(public_match_session_urls(h,base),[
            base+"?t=pRj18GNRKmds",base+"?t=JD9uNvLGV2cq"
        ])
        self.assertEqual(public_match_session_urls(h,base,limit=1),[base+"?t=pRj18GNRKmds"])
        self.assertEqual(public_match_session_urls("<div>No sessions</div>",base),[])

    def test_two_ruskis_official_results_are_parsed_when_public(self):
        event={"name":"Ruskiksen Skabat","date":"2026-11-14",
               "url":"https://fin.boxerbase.com/e/pqlPYS5YEfAR"}
        cases=[
            ("Amir Elyasi vs Otso Västilä", "Amir Elyasi","Otso Västilä",
             "Winner Red Amir Elyasi 3-0","Otso Västilä","3-0",None),
            ("Daniela Taskila vs Wilma Yliluoma","Daniela Taskila","Wilma Yliluoma",
             "Winner Blue Wilma Yliluoma RSC R2","Daniela Taskila","RSC R2",2)
        ]
        for i,(title,red,blue,result,athlete,decision,rnd) in enumerate(cases):
            with self.subTest(bout=i):
                html=(f"<html><head><title>{title} results at Ruskiksen Skabat</title></head><body>"
                      f"<a href='/e/pqlPYS5YEfAR/participants/red'>{red} "
                      f"{'RIIHIMÄEN KEHÄ-KETUT' if athlete==red else 'Turun Teräs'}</a>"
                      f"<a href='/e/pqlPYS5YEfAR/participants/blue'>{blue} "
                      f"{'RIIHIMÄEN KEHÄ-KETUT' if athlete==blue else 'Savate Club Helsinki'}</a>"
                      f"<div>{result}</div></body></html>")
                got=parse_match(
                    html,"https://fin.boxerbase.com/e/pqlPYS5YEfAR/m/"+str(i),
                    [{"name":"Otso Västilä"},{"name":"Daniela Taskila"}],event)
                self.assertIsNotNone(got)
                self.assertEqual((got["boxer"],got["result"],got["decision"],got["round"]),
                                 (athlete,"tappio",decision,rnd))

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
    def test_merged_legacy_club_label_is_accepted(self):
        html='''<html><head><title>Gleb Simanov vs Sampo Paananen results at Test</title></head><body>
        <a href="/boxer/h9XYEbAs3Py4">Gleb Simanov RIIHIMÄEN KEHÄ-KETUT</a>
        <a href="/boxer/xx">Sampo Paananen Other club</a><div>Winner Blue Sampo Paananen 5-0</div></body></html>'''
        result=parse_match(html,'https://boxerbase.com/e/abc/m/xyz',[{'name':'Gleb Simanov'}],{'name':'Test','date':'2026-10-24','url':'https://boxerbase.com/e/abc'})
        self.assertIsNotNone(result)
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
