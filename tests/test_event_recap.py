"""Offline tests. RKK_RUN_VIDEO_SMOKE=1 enables a real two-file mp4 concat."""
from __future__ import annotations
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

try:
 from PIL import Image
except ImportError:
 Image=None

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
modpath=ROOT/'event_recap.py'
spec=importlib.util.spec_from_file_location('rkk_event_recap',modpath)
if Image is not None:
 mod=importlib.util.module_from_spec(spec)
 sys.modules[spec.name]=mod
 spec.loader.exec_module(mod)


def example():
 return {'schema':'RKK_EVENT_RECAP_V1','event_id':'test-20261026',
         'event':'Testitapahtuma','date':'26.10.2026','place':'Riihimäki',
         'channels':['facebook','instagram','youtube'],
         'bouts':[
           {'bout_id':'bout-a','source':'a.mp4','red':'Punainen A','blue':'Sininen A',
            'division':'Miesten eliitti 75','age_group':'adult'},
           {'bout_id':'bout-b','source':'b.mp4','red':'Punainen B','blue':'Sininen B',
            'division':'Miesten eliitti 85','age_group':'adult'}]}


@unittest.skipUnless(Image is not None,'Optional Pillow required')
class EventRecapTests(unittest.TestCase):
 def test_schema_valid(self):
  mod.validate_manifest(example())

 def test_duplicate_bout_not_accepted(self):
  m=example();m['bouts'][1]['bout_id']='bout-a'
  with self.assertRaises(ValueError):mod.validate_manifest(m)

 def test_media_outside_private_dir_rejected(self):
  with TemporaryDirectory() as tmp:
   base=Path(tmp);(base/'a.mp4').write_bytes(b'header')
   with self.assertRaises(ValueError):mod.safe_source(base,'../outside.mp4')

 def test_independent_trust_records_required(self):
  m=example(); reasons=mod.approval_gate(m,{'bout-a':'a','bout-b':'b'},None,None,{})
  self.assertTrue(any('official' in x for x in reasons))
  self.assertTrue(any('rights' in x for x in reasons))

 def test_green_path_with_preapproved_verified_adults(self):
  m=example();hashes={'bout-a':'sha-a','bout-b':'sha-b'}
  official={'event_id':m['event_id'],'bouts':{b['bout_id']:{'red':b['red'],'blue':b['blue'],'result':'Sininen voitti 3–2','source_state':'published'} for b in m['bouts']}}
  rights={'event_id':m['event_id'],'organizer_filming_authorized':True,
          'bouts':{b['bout_id']:{'sha256':hashes[b['bout_id']],
                             'all_visible_people_publication_allowed':True,'age_group':b['age_group'],'audio_rights_cleared':True,'allowed_channels':['facebook','instagram','youtube']} for b in m['bouts']}}
  self.assertEqual(mod.approval_gate(m,hashes,official,rights,{}),[])
  self.assertTrue(any('dedup' in x for x in mod.approval_gate(m,hashes,official,rights,{m['event_id']:'published'})))

 def test_minor_without_explicit_release_held(self):
  m=example();m['bouts'][0]['age_group']='minor'
  hashes={'bout-a':'sha-a','bout-b':'sha-b'}
  official={'event_id':m['event_id'],'bouts':{b['bout_id']:{'red':b['red'],'blue':b['blue'],'result':'Tulos','source_state':'published'} for b in m['bouts']}}
  rights={'event_id':m['event_id'],'organizer_filming_authorized':True,'bouts':{
      b['bout_id']:{'sha256':hashes[b['bout_id']],'all_visible_people_publication_allowed':True,'age_group':b['age_group'],'audio_rights_cleared':True,'allowed_channels':['facebook','instagram','youtube']} for b in m['bouts']}}
  self.assertTrue(any('minor release' in x for x in mod.approval_gate(m,hashes,official,rights,{})))

 def test_captions_never_claim_wins_without_evidence(self):
  c=mod.captions(example(),None)
  self.assertIn('2 ottelusta',c['facebook']);self.assertNotIn('voitti',c['facebook'])
  self.assertTrue(len(c['youtube_title'])<=100)

 def test_no_publication_api_or_secrets_in_tool(self):
  src=modpath.read_text(encoding='utf-8')
  self.assertNotIn('requests.post(',src)
  self.assertNotIn('METRICOOL_API_KEY',src)

 @unittest.skipUnless(os.getenv('RKK_RUN_VIDEO_SMOKE')=='1' and shutil.which('ffmpeg') and shutil.which('ffprobe'),'expensive video integration smoke')
 def test_real_video_two_bouts_renders_offline(self):
  with TemporaryDirectory() as tmp:
   root=Path(tmp); private=root/'private';private.mkdir()
   for name in ['a','b']:
    subprocess.run(['ffmpeg','-nostdin','-loglevel','error','-y',
      '-f','lavfi','-i','testsrc2=size=320x180:rate=25','-t','24',
      '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',str(private/f'{name}.mp4')],check=True)
   logo=root/'logo.png';Image.new('RGBA',(450,100),(255,70,70,255)).save(logo)
   out=root/'out'
   res=mod.run(example(),media_dir=private,logo=logo,output_dir=out,
                clips_per_bout=1,clip_duration=1.2,render=True)
   self.assertFalse(res['auto_publish_ready']) # no trusted external rights/results
   self.assertTrue((out/'RKK_event_recap_draft.mp4').is_file())
   self.assertEqual(mod.probe(out/'RKK_event_recap_draft.mp4')['width'],1080)
   self.assertEqual(len(res['bouts']),2)

if __name__=='__main__':unittest.main()
