"""Test activity proposals; no actual private videos or third-party APIs."""
import importlib.util
import sys
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/'scripts'/'media'/'suggest_clips.py'
spec=importlib.util.spec_from_file_location('rkk_suggest_clips',P)
m=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=m
spec.loader.exec_module(m)

class TestActivityProposals(unittest.TestCase):
    def test_identical_frames_zero_motion(self):
        a=bytes([90])*(112*64)
        self.assertEqual(m.motion_score(a,a),0)

    def test_all_motion_in_roi(self):
        a=bytes([0])*(112*64)
        b=bytes([255])*(112*64)
        self.assertGreater(m.motion_score(a,b),240)

    def test_motion_outside_roi_ignored(self):
        a=bytes([0])*(112*64)
        b=bytearray(a)
        for y in range(0,6):
            for x in range(0,8):b[y*112+x]=255
        self.assertEqual(m.motion_score(a,b),0)

    def test_selects_distinct_high_activity_times(self):
        act=[1.0]*200
        for s in (36,124):
            for i in range(s,s+8):act[i]=15.0
        out=m.propose_windows(act,duration=100,sample_fps=2,
            clip_seconds=4,clip_count=2,head_skip_seconds=0,tail_skip_seconds=0,min_gap_seconds=10)
        self.assertEqual(len(out),2)
        self.assertTrue(any(abs(x.start-18)<5 for x in out))
        self.assertTrue(any(abs(x.start-62)<5 for x in out))

    def test_candidates_are_ordered_and_nonoverlapping(self):
        act=[i%30 for i in range(250)]
        result=m.propose_windows(act,duration=125,sample_fps=2,clip_count=6,min_gap_seconds=9)
        self.assertEqual(result,sorted(result,key=lambda p:p.start))
        for a,b in zip(result,result[1:]):self.assertGreaterEqual(b.start-a.start,13)

    def test_validates_roi(self):
        with self.assertRaises(ValueError):m.ensure_percent_bounds(.7,.2,.6,.4)
        with self.assertRaises(ValueError):m.ensure_percent_bounds(float('nan'),0,.6,.4)

    def test_empty_or_short_video_returns_none(self):
        out=m.propose_windows([0]*7,duration=3,sample_fps=2)
        self.assertEqual(out,[])

    def test_output_has_no_publish_calls(self):
        src=P.read_text(encoding='utf-8')
        self.assertNotIn('requests.post(',src)
        self.assertNotIn('mcp__Metricool__',src)
        self.assertNotIn('publish_post(',src)

if __name__=='__main__':unittest.main()
