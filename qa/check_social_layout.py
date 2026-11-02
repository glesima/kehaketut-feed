#!/usr/bin/env python3
"""Optional browser regression check; no network, credentials or site writes.
Run: python qa/check_social_layout.py [--chromium /usr/bin/chromium]
Requires Playwright and Chromium; kept outside the server's unittest discovery.
"""
import argparse
import copy
import json
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (ROOT / 'docs/social-embed.js').read_text()
IG = {'brand_id':7632678,'instagram_username':'kehaketut','synced_at':'2026-11-02','posts':[
    {'date':'2026-10-28','published_at':'2026-10-28T08:55:24Z','title':'Kolme ottelijaa. Yksi seura.', 'excerpt':'Kolmen ottelijan kilpailupäivän tunnelmia ja tapahtumakooste.','url':'https://www.instagram.com/reel/testA/','thumbnail':'assets/instagram/testA.jpg','type':'REEL'},
    {'date':'2026-10-26','title':'Kaksi ottelua, yksi kilpailupäivä!','excerpt':'Ottelijat mukana saman tapahtuman lyhyessä kilpailukoosteessa.','url':'https://www.instagram.com/reel/testB/','type':'REEL'},
    {'date':'2026-10-25','title':'Kehä-Ketut kehässä!','excerpt':'Hetkiä kilpailupäivästä ja tunnelmia kehän laidalta.','url':'https://www.instagram.com/reel/testC/','type':'REEL'}]}
FB = {'brand_id':7632678,'facebook_page_id':'160875127258478','synced_at':'2026-11-02','posts':[
    {'date':'2026-10-29','text':'HARJOITUKSET JATKUVAT PERJANTAINA 30.10.\n\nHarjoitukset jatkuvat tämän jälkeen tavallisen harjoitusaikataulun mukaisesti. Tervetuloa takaisin treeneihin!', 'url':'https://facebook.com/160875127258478/posts/1'},
    {'date':'2026-10-26','text':'HARJOITUKSET PERUTTU 27.–29.10.2026\n\nHarjoitusvuorot on peruttu määräajaksi. Tiedotamme jatkosta erikseen.','url':'https://facebook.com/160875127258478/posts/2'},
    {'date':'2026-09-29','text':'Tänään treeneissä oli hyvä meininki, 18 treenaajaa täysillä mukana.','url':'https://facebook.com/160875127258478/posts/3'}]}
HTML = '''<!doctype html><html lang="fi"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{box-sizing:border-box}body{margin:0;background:#f3f4f6}.site{max-width:880px;margin:0 auto;padding:0 20px}</style><div class="site"><div id="rkk-social-unified"></div></div></html>'''
RECTS = '''() => {
 const h=document.querySelector('#rkk-social-unified');
 const rect=e=>{const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,height:r.height,width:r.width}};
 return {panels:[...h.querySelectorAll('.rkk-channel')].map(rect),
 cards:[...h.querySelectorAll('.rkk-post-list')].map(n=>[...n.querySelectorAll('.rkk-post-card')].map(rect)),
 footers:[...h.querySelectorAll('.rkk-channel-footer')].map(rect),
 status:[...h.querySelectorAll('.rkk-social-status')].map(rect),
 overflow:document.documentElement.scrollWidth>innerWidth,frames:h.querySelectorAll('iframe,video').length,
 links:[...h.querySelectorAll('a')].map(n=>({url:n.href,rel:n.rel,target:n.target})),
 titles:[...h.querySelectorAll('.rkk-post-title')].map(n=>n.textContent)};
}'''

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--chromium');ap.add_argument('--out',type=Path,default=ROOT/'qa/output')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,**({'executable_path':args.chromium} if args.chromium else {}))
        def page_for(width=1200,ig=None,fb=None,fail_network=None,broken_image=False,empty_host=False,delay=False):
            page=browser.new_page(viewport={'width':width,'height':1000},reduced_motion='reduce')
            errors=[];requests=[]
            page.on('pageerror',lambda e:errors.append(str(e)))
            def route(r):
                url=r.request.url;requests.append(url);path=urlsplit(url).path
                if path.endswith('.json'):
                    network='instagram' if path.endswith('instagram.json') else 'facebook'
                    if network==fail_network or fail_network=='both':r.fulfill(status=503,body='Unavailable');return
                    data=(IG if ig is None else ig) if network=='instagram' else (FB if fb is None else fb)
                    r.fulfill(status=200,content_type='application/json',body=json.dumps(data));return
                if path.endswith('.jpg'):
                    if broken_image:r.fulfill(status=404);return
                    # Deterministic placeholder, no external image request.
                    svg='<svg xmlns="http://www.w3.org/2000/svg" width="88" height="96"><rect width="88" height="96" fill="#18212a"/><text x="10" y="48" fill="#fff">RKK</text></svg>'
                    r.fulfill(status=200,content_type='image/svg+xml',body=svg);return
                r.fulfill(status=404)
            page.route('**/*',route)
            page.set_content(HTML.replace('<div id="rkk-social-unified"></div>','') if empty_host else HTML)
            page.add_script_tag(content=SCRIPT)
            if not empty_host:page.wait_for_function("!document.body.innerText.includes('Haetaan seuran julkaisuja')")
            page.wait_for_timeout(100)
            return page,errors,requests
        def passed(name,details=None):results.append({'test':name,'status':'PASS','details':details})
        for width in [1600,1200,900,768,701,700,390,320]:
            page,errs,req=page_for(width)
            d=page.evaluate(RECTS)
            assert not errs,(width,errs)
            assert not d['overflow'],width
            assert d['frames']==0
            assert [len(x) for x in d['cards']]==[3,3]
            assert all(x['target']=='_blank' and 'noopener' in x['rel'] for x in d['links'])
            assert not any('juicer' in x or 'facebook.html' in x for x in req)
            for panel,status in zip(d['panels'],d['status']):
                assert 12 <= panel['bottom']-status['bottom'] <= 21,(width,panel,status)
            if width>700:
                assert abs(d['panels'][0]['height']-d['panels'][1]['height'])<1
                assert abs(d['footers'][0]['top']-d['footers'][1]['top'])<1
                for a,b in zip(*d['cards']):assert abs(a['height']-b['height'])<1,(width,a,b)
            else:assert d['panels'][1]['top']>=d['panels'][0]['bottom']+15
            if width in [1200,390]:page.screenshot(path=str(args.out/f'preview_{width}.png'),full_page=True)
            passed(f'layout_{width}',d['panels']);page.close()
        page,errs,_=page_for(fail_network='both')
        assert page.locator('.rkk-social-empty').count()==2 and not errs
        assert page.locator('.rkk-channel-footer a').count()==2
        passed('both_feeds_fail_keep_profile_links');page.close()
        # Resizing must not accumulate iframe-style padding.
        page,errs,_=page_for()
        first=page.evaluate(RECTS)
        for w in [390,1200,320,900,1200]:
            page.set_viewport_size({'width':w,'height':1000});page.wait_for_timeout(80)
        last=page.evaluate(RECTS)
        assert first['panels']==last['panels'];assert not errs
        passed('repeated_resize_stable');page.close()
        for network in ['instagram','facebook']:
            page,errs,_=page_for(fail_network=network)
            assert page.locator('.rkk-social-empty').count()==1
            assert page.locator('.rkk-post-card').count()==3
            assert not errs;passed(f'{network}_failure_isolated');page.close()
        for network in ['instagram','facebook']:
            data=copy.deepcopy(IG if network=='instagram' else FB);data['brand_id']=1
            page,errs,_=page_for(**{'ig' if network=='instagram' else 'fb':data})
            assert page.locator('.rkk-social-empty').count()==1;assert not errs
            passed(f'{network}_wrong_brand');page.close()
        for network in ['instagram','facebook']:
            data=copy.deepcopy(IG if network=='instagram' else FB)
            data['posts'] += [dict(data['posts'][0]),None,{'url':'javascript:alert(1)','date':'2026-11-02','title':'bad','text':'bad'},
                             {'url':'https://facebook.com.evil.invalid/posts/1','date':'2026-11-02','title':'bad','text':'bad'}]
            data['posts'][0]['title' if network=='instagram' else 'text']='<img src=x onerror=alert(1)>\n\nLiteral text'
            page,errs,_=page_for(**{'ig' if network=='instagram' else 'fb':data})
            assert page.locator('.rkk-post-card').count()==6;assert not errs
            assert page.locator('img[onerror]').count()==0
            assert '<img src=x' in page.locator('.rkk-post-title').all_text_contents()[0 if network=='instagram' else 3]
            passed(f'{network}_unsafe_and_duplicate_rows');page.close()
        page,errs,_=page_for(broken_image=True)
        page.wait_for_timeout(200);assert page.locator('.rkk-ig-image img').count()==0
        assert page.locator('.rkk-ig-card').count()==3;assert not errs
        passed('broken_thumbnail_link_survives');page.close()
        page,errs,_=page_for()
        page.add_script_tag(content=SCRIPT)
        assert page.locator('.rkk-channel').count()==2;assert page.locator('.rkk-post-card').count()==6
        passed('idempotent_initialization');page.close()
        page,errs,req=page_for(empty_host=True)
        assert not errs and not req;passed('missing_mount_no_effect');page.close()
        # Feed lengths and font enlargement may vary; panels must not clip or grow indefinitely.
        for count in [0,1,2,6]:
            fb=copy.deepcopy(FB);fb['posts']=(fb['posts']*2)[:count]
            page,errs,_=page_for(fb=fb)
            d=page.evaluate(RECTS);assert not d['overflow'] and not errs
            assert abs(d['panels'][0]['height']-d['panels'][1]['height'])<1
            passed(f'facebook_row_count_{count}');page.close()
        page,errs,_=page_for()
        page.add_style_tag(content='#rkk-social-unified .rkk-post-title{font-size:24px!important} #rkk-social-unified .rkk-post-excerpt{font-size:20px!important}')
        d=page.evaluate(RECTS);assert not d['overflow'];assert abs(d['panels'][0]['height']-d['panels'][1]['height'])<1
        passed('enlarged_text_no_panel_clipping');page.close()
        browser.close()
    report={'tests':len(results),'failed':0,'results':results,'scope':'Offline Chromium, synthetic feed rows and thumbnail, no live Yhdistysavain assertion'}
    (args.out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
