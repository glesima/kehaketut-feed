"""Broadcast style renders approved real frames without external publishing."""
import importlib.util
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

try:
    from PIL import Image
except ImportError:
    Image=None

@unittest.skipUnless(Image is not None,"Pillow is an optional media dependency")
class TestBroadcastStyle(unittest.TestCase):
    def test_graphics_are_bounded_and_cover_exists(self):
        P=Path(__file__).resolve().parents[1] / 'scripts' / 'media' / 'broadcast_style.py'
        spec=importlib.util.spec_from_file_location('rkk_broadcast_style',P)
        m=importlib.util.module_from_spec(spec)
        sys.modules[spec.name]=m
        spec.loader.exec_module(m)
        with TemporaryDirectory() as tmp:
            root=Path(tmp)
            logo=root/'logo.png'
            pic=Image.new('RGBA',(900,180),(0,0,0,0))
            for x in range(100,800):
                for y in range(40,140):pic.putpixel((x,y),(255,150,0,255))
            pic.save(logo)
            facts=dict(red='Test Red',blue='Test Blue',place='Hämeenlinna',date='24.10.2026',
                       result='Blue won 5–0',website='kehaketut.fi')
            clip=SimpleNamespace(start=2.0,duration=5.0,crop_x=40)
            with patch.object(m,'preview_frame',return_value=Image.new('RGB',(848,478),'#253445')):
                result=m.render_assets(facts,dict(width=848,height=478),[clip],
                                       root/'source.mp4',logo,root)
            self.assertEqual(result['seconds'],5.0)
            for name in ('background.png','result.png','outro.png','kansikuva.jpg'):
                self.assertTrue((root/name).is_file(),name)
                with Image.open(root/name) as im:self.assertEqual(im.size,(1080,1920))
            with Image.open(root/'result.png') as im:
                self.assertLess(im.getchannel('A').getbbox()[3],650)
            with Image.open(root/'outro.png') as im:
                self.assertLess(im.getchannel('A').getbbox()[3],1250)

if __name__=='__main__':unittest.main()
