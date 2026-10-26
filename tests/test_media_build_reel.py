"""Conservative tests for the standalone local RKK video builder.

No raw video, official logo or connected service is required.
"""
import importlib.util
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

try:
    from PIL import Image
except ImportError:
    Image = None

if Image is not None:
    path = Path(__file__).resolve().parents[1] / 'scripts' / 'media' / 'build_reel.py'
    spec = importlib.util.spec_from_file_location('rkk_media_builder', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)

@unittest.skipUnless(Image is not None, 'Pillow is an optional media dependency')
class TestRKKMedia(unittest.TestCase):
    def setUp(self):
        self.m = {
            'event': 'Testiottelu', 'date': '24.10.2026', 'place': 'Riihimäki',
            'red': 'Punainen', 'blue': 'Sininen', 'division': 'Testisarja',
            'result': 'Sininen voitti 5–0',
            'clips': [
                {'start': 1.0, 'duration': 3.0, 'crop_x': 0},
                {'start': 10.0, 'duration': 3.0, 'crop_x': 100}
            ]
        }
        self.media = {'width': 848, 'height': 478, 'duration': 60, 'has_audio': True}

    def test_valid_clips(self):
        clips = mod.validate(self.m, self.media)
        self.assertEqual(len(clips), 2)
        self.assertEqual(sum(c.duration for c in clips), 6.)

    def test_out_of_bounds_clip_fails(self):
        self.m['clips'][1]['start'] = 58
        with self.assertRaises(ValueError):
            mod.validate(self.m, self.media)

    def test_crop_out_of_bounds_fails(self):
        self.m['clips'][1]['crop_x'] = 10000
        with self.assertRaises(ValueError):
            mod.validate(self.m, self.media)

    def test_missing_result_fails(self):
        self.m['result'] = ''
        with self.assertRaises(ValueError):
            mod.validate(self.m, self.media)

    def test_logo_and_caption_drafts(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            logo = root / 'logo.png'
            Image.new('RGBA', (500, 160), (255, 0, 0, 255)).save(logo)
            self.assertEqual(mod.draw_background(self.m, logo).size, (1080, 1920))
            self.assertEqual(mod.draw_outro(logo, 'KEHAKETUT.FI').size, (1080, 1920))
            mod.create_caption_drafts(self.m, root)
            self.assertIn('24.10.2026', (root / 'instagram_luonnos.txt').read_text())
            self.assertIn('Sininen voitti 5–0', (root / 'facebook_luonnos.txt').read_text())

    def test_shorts_safe_space_keeps_names_and_result_above_ui(self):
        with TemporaryDirectory() as tmp:
            path_logo=Path(tmp) / 'logo.png'
            Image.new('RGBA',(500,150),(255,0,0,255)).save(path_logo)
            background=mod.draw_background(self.m,path_logo)
            lower=background.crop((0,1390,1080,1920)).convert('RGB')
            self.assertLess(max(high for _,high in lower.getextrema()),70)
            result=mod.draw_result(self.m)
            self.assertLessEqual(result.getchannel('A').getbbox()[3],640)

    def test_no_publish_API_in_builder(self):
        src = path.read_text(encoding='utf-8')
        self.assertNotIn('requests.post(', src)
        self.assertNotIn('MetricoolToken', src)
        self.assertNotIn('publish_post(', src)

if __name__ == '__main__':
    unittest.main()
