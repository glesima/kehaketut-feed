"""Cache already-public club Instagram JPEG thumbnails; no API credentials.
Only allowlisted Meta CDN and published Metricool media hosts, bounded downloads, atomic writes. A failed
refresh retains the last image; new missing images use the UI's neutral tile.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener

MAX_BYTES = 3 * 1024 * 1024

def allowed_image_url(value: str) -> bool:
    try:
        u = urlsplit(value)
        host = u.hostname or ''
        meta = (host.endswith('.cdninstagram.com') or host.endswith('.fbcdn.net'))
        # Metricool copies photos into a public media CDN only once the post
        # is published. Exact host and bounded media path, not arbitrary URLs.
        published_metricool = (host == 'static.metricool.com'
            and not u.query and not u.fragment
            and bool(re.fullmatch(r'/planner/[0-9]{6}/[0-9]+-file-[0-9]+\\.jpe?g', u.path)))
        return (u.scheme == 'https' and not u.username and not u.password
                and u.port in (None, 443) and bool(host)
                and (meta or published_metricool))
    except (ValueError, TypeError, AttributeError):
        return False

class RestrictedRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed_image_url(newurl):
            raise ValueError('Unexpected thumbnail redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def jpeg_ok(raw: bytes) -> bool:
    return 64 <= len(raw) <= MAX_BYTES and raw.startswith(b'\xff\xd8\xff') and raw.rstrip().endswith(b'\xff\xd9')

def fetch_jpeg(url: str) -> bytes:
    if not allowed_image_url(url):
        raise ValueError('Thumbnail host rejected')
    opener = build_opener(RestrictedRedirects())
    request = Request(url, headers={'User-Agent':'RKK-Public-Thumbnail-Cache/1.0', 'Accept':'image/jpeg'})
    with opener.open(request, timeout=15) as response:
        if not allowed_image_url(response.url):
            raise ValueError('Thumbnail host changed')
        if response.headers.get_content_type() != 'image/jpeg':
            raise ValueError('Expected JPEG')
        raw = response.read(MAX_BYTES + 1)
    if not jpeg_ok(raw):
        raise ValueError('Invalid or oversized JPEG')
    return raw

def post_code(post: dict) -> str:
    u = urlsplit(post.get('url',''))
    m = re.fullmatch(r'/(?:reel|p|tv)/([A-Za-z0-9_-]+)/', u.path)
    if (u.scheme != 'https' or u.hostname not in ('instagram.com','www.instagram.com')
        or u.username or u.password or u.port or not m):
        raise ValueError('Invalid Instagram post')
    return m.group(1)

def cache(feed: dict, root: Path, fetcher=fetch_jpeg) -> dict:
    if (feed.get('brand_id') != 7632678 or feed.get('instagram_username') != 'kehaketut'
        or not isinstance(feed.get('posts'),list)):
        raise ValueError('Wrong Instagram feed')
    out = root / 'assets' / 'instagram'
    out.mkdir(parents=True, exist_ok=True)
    counts = {'updated':0,'unchanged':0,'failed':0}
    for post in feed['posts'][:6]:
        try:
            code = post_code(post)
            if post.get('thumbnail') != 'assets/instagram/' + code + '.jpg':
                raise ValueError('Unexpected image destination')
            url = post.get('image_source','')
            if not allowed_image_url(url):
                raise ValueError('Unexpected image source')
            target = out / (code + '.jpg')
            if target.is_symlink():
                raise ValueError('Symlink rejected')
            raw = fetcher(url)
            if not jpeg_ok(raw):
                raise ValueError('Invalid image bytes')
            if target.exists() and target.read_bytes() == raw:
                counts['unchanged'] += 1
            else:
                temp = out / (code + '.part')
                if temp.is_symlink():
                    raise ValueError('Symlink rejected')
                temp.write_bytes(raw)
                temp.replace(target)
                counts['updated'] += 1
        except (ValueError, OSError, TypeError, AttributeError):
            counts['failed'] += 1
            # Never log signed CDN URLs or remove an existing last-good image.
    return counts

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--docs',type=Path,default=Path(__file__).resolve().parents[1]/'docs')
    args = parser.parse_args()
    feed = json.loads((args.docs/'instagram.json').read_text(encoding='utf-8'))
    result = cache(feed, args.docs)
    print(json.dumps(result))
    if result['failed']:
        print('::warning::Some Instagram thumbnails could not be refreshed; previous images and post links retained.')

if __name__ == '__main__':
    main()
