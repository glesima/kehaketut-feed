import tempfile
import unittest
from pathlib import Path
from scripts.cache_instagram_thumbnails import allowed_image_url, jpeg_ok, cache, post_code, MAX_BYTES

# Synthetic byte fixture for the transport boundary, not a JPEG decode test.
JPEG = b'\xff\xd8\xff' + b'x'*90 + b'\xff\xd9'
URL = 'https://scontent-test.cdninstagram.com/photo.jpg?signature=example'

def feed():
    return {'brand_id':7632678,'instagram_username':'kehaketut','posts':[
        {'url':'https://www.instagram.com/reel/Ab_c-1/','thumbnail':'assets/instagram/Ab_c-1.jpg','image_source':URL}]}

class InstagramThumbnailTests(unittest.TestCase):
    def test_allowed_meta_cdn(self): self.assertTrue(allowed_image_url(URL))
    def test_no_arbitrary_hosts(self):
        for url in ['https://evil.example/a','https://cdninstagram.com.evil.example/a','http://scontent-test.cdninstagram.com/a','https://127.0.0.1/a','https://user@x.cdninstagram.com/a','https://x.cdninstagram.com:8080/a']:
            self.assertFalse(allowed_image_url(url))
    def test_non_images_rejected(self): self.assertFalse(jpeg_ok(b'<svg>'+b'x'*100))
    def test_oversize_rejected(self): self.assertFalse(jpeg_ok(b'\xff\xd8\xff'+b'x'*MAX_BYTES+b'\xff\xd9'))
    def test_url_code(self): self.assertEqual(post_code(feed()['posts'][0]),'Ab_c-1')
    def test_path_rejected(self):
        with self.assertRaises(ValueError): post_code({'url':'https://www.instagram.com/reel/../../file/'})
    def test_wrong_account_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            d=feed();d['brand_id']=1
            with self.assertRaises(ValueError): cache(d,Path(td),lambda _: JPEG)
    def test_saves_atomic_image(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);r=cache(feed(),root,lambda _:JPEG)
            self.assertEqual(r['updated'],1)
            self.assertEqual((root/'assets/instagram/Ab_c-1.jpg').read_bytes(),JPEG)
            self.assertFalse(list(root.rglob('*.part')))
    def test_unchanged(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);cache(feed(),root,lambda _:JPEG)
            self.assertEqual(cache(feed(),root,lambda _:JPEG)['unchanged'],1)
    def test_failure_preserves_previous(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);cache(feed(),root,lambda _:JPEG)
            def bad(_): raise OSError('expired')
            self.assertEqual(cache(feed(),root,bad)['failed'],1)
            self.assertEqual((root/'assets/instagram/Ab_c-1.jpg').read_bytes(),JPEG)
    def test_target_cannot_be_selected(self):
        with tempfile.TemporaryDirectory() as td:
            d=feed();d['posts'][0]['thumbnail']='../../outside.jpg'
            self.assertEqual(cache(d,Path(td),lambda _:JPEG)['failed'],1)
    def test_bad_replacement_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);cache(feed(),root,lambda _:JPEG)
            self.assertEqual(cache(feed(),root,lambda _:b'<html>')['failed'],1)
            self.assertEqual((root/'assets/instagram/Ab_c-1.jpg').read_bytes(),JPEG)
if __name__=='__main__': unittest.main()
