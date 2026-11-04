"""Merge regression tests: fixtures contain no private personal information."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import update as u
from club_identity import canonical_previous,confirmed_merge,validate_merged_roster,profile_bout_urls,mark_stats_quality

class MergeTests(unittest.TestCase):
    def setUp(self):
        self.config={'club_id':'new','club_url':'https://boxerbase.com/o/new/boxers',
            'club_names':['CLUB','Club ry'],'tracked_events':[],
            'event_index':'https://boxerbase.com/','max_index_events':1,
            'confirmed_club_merge':{'from':'old','to':'new'},
            'boxer_id_aliases':{'oldA':'newA'},'boxer_name_aliases':{'A Short':'A Full'}}
        self.prior={'club_id':'old','boxers':[{'id':'oldA','name':'A Short',
            'boxerbase_url':'https://boxerbase.com/boxer/oldA','matches':3,'wins':1,'losses':2,
            'stats_source_url':'https://boxerbase.com/boxer/other','stats_source_note':'legacy'}],
            'matches':[{'id':'bout1','boxer':'A Short','red_boxer':'A Short','blue_boxer':'Opponent',
                'opponent':'Opponent','result':'tappio','decision':'3-0','event_date':'2026-01-02',
                'event':'Cup','event_url':'https://boxerbase.com/e/cup','url':'https://boxerbase.com/e/cup/m/bout1'}],
            'registrations':[{'event_id':'event','boxer_id':'oldA','boxer':'A Short','status':'registered',
                'observed_at':'2026-10-28T00:00:00Z','registered_club':'Club ry','participant_url':'https://boxerbase.com/e/event/participants/a','event_date':'2026-11-06'}],
            'matches_checked_at':'2026-10-28T00:00:00Z'}
    def test_exact_merge_only(self):
        self.assertTrue(confirmed_merge(self.prior,self.config))
        self.assertFalse(confirmed_merge({'club_id':'stranger'},self.config))
    def test_unchanged_original(self):
        before=copy.deepcopy(self.prior);canonical_previous(self.prior,self.config);self.assertEqual(before,self.prior)
    def test_preserve_results_and_dates(self):
        out=canonical_previous(self.prior,self.config)
        self.assertEqual(out['matches'][0]['id'],'bout1')
        for k in ['decision','result','event_date','url']:
            self.assertEqual(out['matches'][0][k],self.prior['matches'][0][k])
        self.assertEqual(out['matches_checked_at'],self.prior['matches_checked_at'])
        self.assertEqual(out['club_id'],'old')
    def test_no_addition_and_no_temporary_stats(self):
        b=canonical_previous(self.prior,self.config)['boxers'][0]
        self.assertEqual(b['id'],'newA');self.assertEqual(b['matches'],3)
        self.assertNotIn('stats_source_url',b);self.assertNotIn('stats_source_note',b)
    def test_rekeys_registration_without_new_observation(self):
        r=canonical_previous(self.prior,self.config)['registrations'][0]
        self.assertEqual(r['boxer_id'],'newA');self.assertEqual(r['boxer'],'A Full')
        self.assertEqual(r['previous_boxer_id'],'oldA')
        self.assertEqual(r['observed_at'],self.prior['registrations'][0]['observed_at'])
    def test_duplicate_registration_retains_latest(self):
        row={**self.prior['registrations'][0],'boxer_id':'newA','observed_at':'2026-11-01T00:00:00Z'}
        self.prior['registrations'].append(row)
        out=canonical_previous(self.prior,self.config)
        self.assertEqual(len(out['registrations']),1);self.assertEqual(out['registrations'][0]['observed_at'],row['observed_at'])
    def test_unrelated_club_not_migrated(self):
        self.prior['club_id']='stranger';self.assertEqual(canonical_previous(self.prior,self.config),self.prior)
    def test_idempotent(self):
        once=canonical_previous(self.prior,self.config)
        self.assertEqual(once,canonical_previous(once,self.config))
    def test_missing_roster_rejected(self):
        for rows in [[],[{'id':'missing'}],[{'id':'newA'},{'id':'newA'}],[{'id':None}]]:
            with self.subTest(rows=rows),self.assertRaises(ValueError):validate_merged_roster(rows,self.prior,self.config)
    def test_complete_roster_accepted(self):validate_merged_roster([{'id':'newA'}],self.prior,self.config)
    def test_consistency_preserves_source(self):
        row={'matches':6,'wins':4,'losses':4};mark_stats_quality(row)
        self.assertEqual(row,{'matches':6,'wins':4,'losses':4,'stats_consistency':'inconsistent'})
    def test_unknown_draws_not_invented(self):
        row={'matches':7,'wins':3,'losses':3};mark_stats_quality(row);self.assertEqual(row['stats_consistency'],'reported')
    def test_partial_stats(self):self.assertEqual(mark_stats_quality({'matches':0,'wins':None,'losses':None})['stats_consistency'],'partial')
    def test_bout_links_dedup_and_safe(self):
        h='''<a href="/e/a/m/b">match</a><a href="/e/a/m/b">repeat</a><a href="https://evil.test/e/a/m/c">x</a><a href="https://boxerbase.com.evil.test/e/a/m/c">x</a><a href="https://name@boxerbase.com/e/a/m/c">x</a><a href="/api/private">private</a>'''
        self.assertEqual(profile_bout_urls(h,'https://boxerbase.com/boxer/newA'),['https://boxerbase.com/e/a/m/b'])
    def test_failed_migration_does_not_touch_feed(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'data.json';out.write_text(json.dumps(self.prior));before=out.read_bytes()
            with patch.object(u,'OUT',out),patch.object(u,'CONFIG',self.config),patch.object(u,'fetch',side_effect=RuntimeError('source error')):
                with self.assertRaisesRegex(RuntimeError,'previous feed unchanged'):u.update()
            self.assertEqual(out.read_bytes(),before)
    def test_update_preserves_history_when_migration_successful(self):
        def fetch(url):
            if url==self.config['club_url']:
                return '<table><tr><td><a href="/boxer/newA">A</a></td><td>Full</td><td>3</td></tr></table>'
            if '/boxer/' in url:return '<div>3 Matches 1 Wins 2 Losses</div>'
            return '<html></html>'
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'data.json';out.write_text(json.dumps(self.prior))
            with patch.object(u,'OUT',out),patch.object(u,'CONFIG',self.config),patch.object(u,'fetch',side_effect=fetch),patch.object(u,'write_rss'),patch.object(u,'get_instagram',return_value=None):u.update()
            got=json.loads(out.read_text());self.assertEqual(got['club_id'],'new')
            self.assertEqual(got['matches'][0]['id'],'bout1');self.assertEqual(got['registrations'][0]['boxer_id'],'newA')
            self.assertEqual(got['boxers'][0]['id'],'newA')
    def test_verified_short_name_matches_canonical_person(self):
        h='''<title>Josias Ndikumana vs Other Fighter results at Cup</title><a href="/e/c/participants/a">Josias Ndikumana RIIHIMÄEN KEHÄ-KETUT</a>Winner Blue • 3-0'''
        b=u.parse_match(h,'https://boxerbase.com/e/c/m/b',[{'name':'Josias Joseph Ndikumana'}],{'name':'Cup','date':'2026-01-02','url':'https://boxerbase.com/e/c'})
        self.assertIsNotNone(b);self.assertEqual(b['boxer'],'Josias Joseph Ndikumana');self.assertEqual(b['result'],'tappio')
    def test_partial_athlete_name_not_accepted(self):
        h='<title>Gleb Simanov Junior vs Other results at Cup</title><a href="/boxer/x">Gleb Simanov Junior RIIHIMÄEN KEHÄ-KETUT</a>Winner Red • 3-0'
        self.assertIsNone(u.parse_match(h,'https://boxerbase.com/e/c/m/b',[{'name':'Gleb Simanov'}],{'name':'Cup','date':'2026-01-02','url':'https://boxerbase.com/e/c'}))

if __name__=='__main__':unittest.main()
