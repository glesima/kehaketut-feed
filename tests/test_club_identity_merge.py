import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from club_identity import prepare_identity,participant_matches
class MergeTests(unittest.TestCase):
 def setUp(self):
  self.cfg={"club_id":"new","merged_from_club_ids":["old"],"profile_names_by_slug":{"a":"Fighter A"}}
  self.roster=[{"id":"new1","name":"Fighter A","matches":3},{"id":"new2","name":"Fighter B","matches":1}]
  self.prior={"club_id":"old","boxers":[{"id":"old1","name":"Fighter A"},{"id":"old2","name":"Fighter B"}],
   "matches":[{"id":"bout","url":"https://boxerbase.com/e/evt/m/bout","boxer":"Fighter A","opponent":"Other","result":"voitto","decision":"3-0"}],
   "registrations":[{"event_id":"evt","boxer_id":"old1","boxer":"Fighter A","observed_at":"2026-11-01"}]}
 def test_no_history_loss(self):
  r=prepare_identity(self.prior,self.roster,self.cfg);self.assertEqual(len(r["matches"]),1);self.assertEqual(r["matches"][0]["decision"],"3-0")
 def test_aliases_and_profile(self):
  r=prepare_identity(self.prior,self.roster,self.cfg);self.assertEqual(r["boxer_id_aliases"]["old1"],"new1");self.assertEqual(r["profile_ids_by_slug"]["a"],"new1")
 def test_registrations(self):self.assertEqual(prepare_identity(self.prior,self.roster,self.cfg)["registrations"][0]["boxer_id"],"new1")
 def test_missing_fighter_blocks(self):
  with self.assertRaises(ValueError):prepare_identity(self.prior,self.roster[:1],self.cfg)
 def test_unapproved_change(self):
  self.prior["club_id"]="other"
  with self.assertRaises(ValueError):prepare_identity(self.prior,self.roster,self.cfg)
 def test_exact_participant(self):
  self.assertTrue(participant_matches("Fighter A (RIIHIMÄEN KEHÄ-KETUT)","Fighter A",["RIIHIMÄEN KEHÄ-KETUT"],self.cfg))
  self.assertFalse(participant_matches("Fighter AA (RIIHIMÄEN KEHÄ-KETUT)","Fighter A",["RIIHIMÄEN KEHÄ-KETUT"],self.cfg))
 def test_distinct_bouts_not_deduped(self):
  m=self.prior["matches"][0].copy();m["id"]="different";m["url"]="https://fin.boxerbase.com/e/evt/m/different";self.prior["matches"].append(m)
  self.assertEqual(len(prepare_identity(self.prior,self.roster,self.cfg)["matches"]),2)
 def test_same_bout_other_host_deduped(self):
  m=self.prior["matches"][0].copy();m["url"]="https://fin.boxerbase.com/e/evt/m/bout";self.prior["matches"].append(m)
  self.assertEqual(len(prepare_identity(self.prior,self.roster,self.cfg)["matches"]),1)
if __name__=="__main__":unittest.main()
