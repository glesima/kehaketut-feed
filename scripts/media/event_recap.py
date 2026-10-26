#!/usr/bin/env python3
"""Private multi-bout boxing recap prototype with preauthorized zero-touch gating.

Builds one vertical MP4 from *local* user-supplied videos and returns a JSON
publication handoff. It does NOT use network, access Metricool, or publish.

The green path is intentionally strict: an independent trusted facts file,
private media-rights receipts tied to actual file hashes, and an unposted event
ledger are required. Without them an edited preview is still possible, but
AUTO_PUBLISH_READY is false. No AI invents a match result or punch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont

W,H=1080,1920
WINDOW_X,WINDOW_Y,WINDOW_W,WINDOW_H=20,454,1040,866
COLORS={"red":(190,30,49),"blue":(68,122,202),"ink":(17,23,30),"white":(246,248,250)}
ALLOWED={"facebook","instagram","youtube"}
MAX_BOUTS=12
MAX_FILE_BYTES=3_000_000_000


def command(args:list[str])->str:
    r=subprocess.run(args,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    if r.returncode:raise RuntimeError(f"{args[0]} failed: {r.stderr[-1100:]}")
    return r.stdout


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()


def probe(path:Path)->dict:
    doc=json.loads(command(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)]))
    video=next((x for x in doc.get('streams',[]) if x.get('codec_type')=='video'),None)
    if not video:raise ValueError('No video in '+path.name)
    return {'duration':float(doc['format']['duration']),'width':int(video['width']),
            'height':int(video['height']),
            'has_audio':any(x.get('codec_type')=='audio' for x in doc['streams'])}


def safe_source(directory:Path,name:str)->Path:
    if not name or Path(name).is_absolute() or '\\' in name or '..' in Path(name).parts:
        raise ValueError('Source name must be a simple relative path below the private media folder')
    source=(directory / name).resolve(strict=True)
    if not source.is_relative_to(directory.resolve(strict=True)) or source.suffix.lower()!='.mp4':
        raise ValueError('Only local MP4 files inside the private media folder are supported')
    if not source.is_file() or source.stat().st_size>MAX_FILE_BYTES:
        raise ValueError('Missing / oversized local MP4')
    return source


def validate_manifest(doc:dict)->None:
    if doc.get('schema')!='RKK_EVENT_RECAP_V1':raise ValueError('Invalid schema')
    required=['event_id','event','date','place','bouts']
    if any(not doc.get(k) for k in required):raise ValueError('Missing event facts')
    if not re.fullmatch(r'[a-zA-Z0-9_-]{4,80}',str(doc['event_id'])):
        raise ValueError('Invalid event ID')
    for k in ['event','date','place']:
        if not isinstance(doc[k],str) or len(doc[k])>120:raise ValueError('Invalid event text')
    bouts=doc['bouts']
    if not isinstance(bouts,list) or not 1<=len(bouts)<=MAX_BOUTS:
        raise ValueError('Provide 1–12 bouts')
    seen=set();sources=set()
    for b in bouts:
        for k in ['bout_id','source','red','blue','division','age_group']:
            if not isinstance(b.get(k),str) or not b[k].strip() or len(b[k])>130:
                raise ValueError('Invalid bout field: '+k)
        if b['bout_id'] in seen or b['source'] in sources:raise ValueError('Duplicate bout or source')
        seen.add(b['bout_id']);sources.add(b['source'])
        if b['age_group'] not in ('adult','minor'):raise ValueError('Unknown age group')
        if b.get('featured_boxer') and b['featured_boxer'] not in (b['red'],b['blue']):
            raise ValueError('Featured boxer must be one of the recorded red/blue participants')
    channels=doc.get('channels',['facebook','instagram','youtube'])
    if not channels or set(channels)!=ALLOWED or len(channels)!=3:
        raise ValueError('Recap must use exactly the three designated RKK channels')


def approval_gate(doc:dict, media_checksums:dict[str,str],
                  verified:dict|None, rights:dict|None, ledger:dict|None)->list[str]:
    """No per-post click is needed for GREEN once external trust checks pass.

    Uploader-provided 'approved' flags are NOT trusted. verified/rights/ledger
    are independent private server-side records. The actual publisher must
    enforce the same checks, not trust a copied output JSON blindly.
    """
    reasons=[]
    if not isinstance(verified,dict) or verified.get('event_id')!=doc['event_id']:
        reasons.append('Missing trusted official event data')
    if not isinstance(rights,dict) or rights.get('event_id')!=doc['event_id'] or not rights.get('organizer_filming_authorized'):
        reasons.append('Missing trusted organizer / video rights record')
    if not isinstance(ledger,dict):reasons.append('Missing durable publication ledger')
    else:
        seen=ledger.get(doc['event_id'])
        if seen in ('published','submitting','queued','partial'):
            reasons.append('Event previously submitted/published: dedup lock')
    official=(verified or {}).get('bouts',{})
    releases=(rights or {}).get('bouts',{})
    for b in doc['bouts']:
        boutid=b['bout_id']
        record=official.get(boutid)
        if not record or record.get('red')!=b['red'] or record.get('blue')!=b['blue'] or not record.get('result') or record.get('source_state')!='published':
            reasons.append(f'Bout {boutid}: no exact official verified names and result')
        grant=releases.get(boutid)
        if not grant or grant.get('sha256')!=media_checksums.get(boutid) or not grant.get('all_visible_people_publication_allowed'):
            reasons.append(f'Bout {boutid}: missing video-hash-bound publication rights')
        elif grant.get('age_group')!=b['age_group']:
            reasons.append(f'Bout {boutid}: conflicting age group in trusted rights record')
        elif not grant.get('audio_rights_cleared') or not ALLOWED.issubset(set(grant.get('allowed_channels',[]))):
            reasons.append(f'Bout {boutid}: audio or channel-specific publication rights not cleared')
        elif grant['age_group']=='minor' and not grant.get('guardian_release_record_id'):
            reasons.append(f'Bout {boutid}: minor release not registered')
    return reasons


def suggest_for_bout(source:Path,meta:dict,*,n:int=2,secs:float=3.0)->list[tuple[float,float,float]]:
    """Use existing repo's motion proposal module (NOT a punch recognizer)."""
    import suggest_clips
    _,act=suggest_clips.analyze_video(source,(.12,.14,.78,.67))
    p=suggest_clips.propose_windows(act,duration=meta['duration'],clip_count=n,
        clip_seconds=secs,min_gap_seconds=7.,head_skip_seconds=min(7.,meta['duration']*.12),
        tail_skip_seconds=min(4.,meta['duration']*.09))
    if len(p)<n or min(x.activity_score for x in p)<.05:
        # Low activity or too-short source: can render nothing automatically.
        return []
    return [(x.start,x.duration,x.activity_score) for x in p]


def font(sz:int):
    for path in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                 '/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf'):
        if Path(path).is_file():return ImageFont.truetype(path,sz)
    raise RuntimeError('DejaVu or Noto Sans font required')


def fitted(draw:ImageDraw.ImageDraw,value:str,maxwidth:int,begin:int=42):
    for sz in range(begin,13,-1):
        f=font(sz)
        if draw.textbbox((0,0),value,font=f)[2]<=maxwidth:return f
    raise ValueError('Text too long for safe graphics')


def logo_alpha(path:Path,size:tuple[int,int]):
    im=Image.open(path).convert('RGBA'); box=im.getchannel('A').getbbox()
    if not box:raise ValueError('Blank club logo')
    im=im.crop(box);im.thumbnail(size,Image.Resampling.LANCZOS)
    return im


def make_card(doc:dict,logo:Path,bout:dict|None=None,result:str|None=None)->Image.Image:
    im=Image.new('RGBA',(W,H),COLORS['ink']+(255,));d=ImageDraw.Draw(im)
    for y in range(H):
        k=int(y/H*12);d.line([(0,y),(W,y)],fill=(16+k,21+k,27+k,255))
    d.rectangle((0,0,W,14),fill=COLORS['red']+(255,))
    d.rectangle((0,WINDOW_Y-9,W,WINDOW_Y-5),fill=COLORS['red']+(255,))
    d.rectangle((0,WINDOW_Y+WINDOW_H+5,W,WINDOW_Y+WINDOW_H+9),fill=COLORS['red']+(255,))
    lg=logo_alpha(logo,(750,165));im.alpha_composite(lg,((W-lg.width)//2,38))
    d=ImageDraw.Draw(im)
    d.text((52,216),doc['event'].upper(),font=fitted(d,doc['event'].upper(),975,39),fill=COLORS['white'])
    d.text((53,279),f"{doc['place']}  •  {doc['date']}",font=font(25),fill=(183,193,208))
    if bout:
        heading=f"{bout['red'].upper()}  vs  {bout['blue'].upper()}"
        d.text((55,341),heading,font=fitted(d,heading,965,36),fill=COLORS['white'])
        d.text((56,396),bout['division'],font=fitted(d,bout['division'],950,24),fill=(199,204,214))
        # Avoid lower third: Shorts overlays appear there.
        if result:
            d.rounded_rectangle((40,1330,1040,1379),radius=10,fill=(33,42,55,240))
            d.text((57,1338),result,font=fitted(d,result,955,28),fill=COLORS['white'])
    else:
        title='KEHÄ-KETTUJEN KILPAILUPÄIVÄ'
        d.text((W//2,750),title,font=fitted(d,title,980,53),anchor='mt',fill=COLORS['white'])
        d.text((W//2,866),'OTTELUKOOSTE',font=font(40),anchor='mt',fill=(239,179,187))
        d.text((W//2,1080),'KEHAKETUT.FI',font=font(40),anchor='mt',fill=COLORS['white'])
    return im


def make_clip(src:Path, card:Path, out:Path, start:float, duration:float, has_audio:bool):
    ff=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y',
        '-ss',str(start),'-t',str(duration),'-i',str(src),
        '-loop','1','-framerate','25','-i',str(card)]
    if not has_audio:ff+=['-f','lavfi','-i','anullsrc=r=48000:cl=stereo']
    filt=(f'[0:v]fps=25,scale={WINDOW_W}:{WINDOW_H}:force_original_aspect_ratio=decrease,'
          f'pad={WINDOW_W}:{WINDOW_H}:(ow-iw)/2:(oh-ih)/2:black,setsar=1[shot];'
          f'[1:v][shot]overlay={WINDOW_X}:{WINDOW_Y}:shortest=1:format=auto[outv]')
    ff+=['-filter_complex',filt,'-map','[outv]','-map',('0:a:0' if has_audio else '2:a:0'),
         '-t',str(duration),'-r','25','-c:v','libx264','-preset','ultrafast','-crf','23',
         '-pix_fmt','yuv420p','-c:a','aac','-ar','48000','-ac','2','-b:a','128k',
         '-movflags','+faststart',str(out)]
    command(ff)


def make_still(image:Path,out:Path,duration:float):
    command(['ffmpeg','-nostdin','-loglevel','error','-y',
             '-loop','1','-framerate','25','-i',str(image),
             '-f','lavfi','-i','anullsrc=r=48000:cl=stereo',
             '-t',str(duration),'-map','0:v:0','-map','1:a:0',
             '-c:v','libx264','-preset','ultrafast','-crf','23','-pix_fmt','yuv420p','-r','25',
             '-c:a','aac','-ar','48000','-ac','2','-b:a','128k','-movflags','+faststart',str(out)])


def captions(doc:dict,official:dict|None)->dict[str,str]:
    bts=doc['bouts']; players=', '.join(b['featured_boxer'] for b in bts if b.get('featured_boxer'))
    # Not all red-corner athletes necessarily belong to RKK. Use a neutral
    # count and do not invent individual performances/club associations.
    n=len(bts)
    base=(f"Riihimäen Kehä-Ketut 🥊 {doc['event']}, {doc['place']} {doc['date']}. "
          f"Yhdessä videossa hetkiä {n} ottelusta. "
          "Katso aitoja kehätilanteita ja seuraa seuramme toimintaa: kehaketut.fi")
    if players:base += f". Mukana: {players}."
    return {
      'facebook':f"🥊 Kilpailupäivän ottelukooste!\n\n{base}\n\n#KehäKetut #Nyrkkeily #Riihimäki",
      'instagram':f"🥊 Kehä-Ketut kehässä!\n\n{doc['place']} · {doc['date']} · {n} ottelua yhdessä koosteessa.\nAitoja tilanteita, urheilua ja tunnelmaa.\n\n#KehäKetut #Nyrkkeily #Riihimäki #Boxing",
      'youtube':f"🥊 Kehä-Ketut – {doc['event']}, {doc['date']}\n\n{base}\n\n#KehäKetut #Boxing #Shorts",
      'youtube_title':f"Kehä-Ketut – {doc['place']} {doc['date']} | {n} ottelua"[:100]
    }


def run(doc:dict, *,media_dir:Path,logo:Path,output_dir:Path,
        official:dict|None=None,rights:dict|None=None,ledger:dict|None=None,
        clip_duration:float=3.0,clips_per_bout:int=2,render:bool=True)->dict:
    validate_manifest(doc)
    if not logo.is_file():raise FileNotFoundError('Club logo missing')
    if not (1<=clips_per_bout<=3 and 1<=clip_duration<=6):raise ValueError('Invalid clip parameters')
    # Prefer a compact event recap and enforce Facebook Reel's 90-second ceiling.
    cap=(85-3.2)/(len(doc['bouts'])*clips_per_bout)
    clip_duration=min(clip_duration,round(cap,2))
    if clip_duration<1:raise ValueError('Too many bouts/clips to fit a readable event recap')
    output_dir.mkdir(parents=True,exist_ok=True)
    output_dir=output_dir.resolve(strict=True)
    records=[];checksums={};warnings=[]
    for b in doc['bouts']:
        src=safe_source(media_dir,b['source']);meta=probe(src)
        if meta['duration']>3600 or meta['duration']<10:raise ValueError('Video duration unsupported')
        hashvalue=sha256(src);checksums[b['bout_id']]=hashvalue
        proposals=suggest_for_bout(src,meta,n=clips_per_bout,secs=clip_duration)
        if len(proposals)!=clips_per_bout:
            warnings.append(f"Bout {b['bout_id']}: insufficient confident motion windows")
        records.append({'bout_id':b['bout_id'],'source':str(src),'meta':meta,
                        'clips':[{'start':a,'duration':d,'activity':sc} for a,d,sc in proposals]})
    failures=approval_gate(doc,checksums,official,rights,ledger)+warnings
    if render and any(not r['clips'] for r in records):
        # Do not guess safe fallback clips. No video rendered if a boxer cannot
        # be fairly included. Emit a clear exception instead.
        render=False
    verified_results=(official or {}).get('bouts',{})
    outcap=captions(doc,official)
    packet={'schema':'RKK_EVENT_RECAP_OUTPUT_V1','event_id':doc['event_id'],
            'auto_publish_ready':not failures,'status':'READY_FOR_PRIVATE_DELIVERY' if not failures else 'HELD_FOR_EXCEPTIONS',
            'blockers':failures,'bouts':records,'channels':doc.get('channels',sorted(ALLOWED)),
            'outbox':{},'publication_note':'Offline package only; an authenticated external publisher must reverify independent rights, results, ledger and stable media URL.'}
    for net in sorted(ALLOWED):
        packet['outbox'][net]={'type':('short' if net=='youtube' else 'REEL'),
            'title':outcap.get('youtube_title') if net=='youtube' else None,
            'text':outcap[net],'autoPublish':True,'draft':False,
            'media_local':None,'published':False}
    if render:
        temp=output_dir/'segments';temp.mkdir(exist_ok=True)
        start_img=temp/'intro.png';make_card(doc,logo).convert('RGB').save(start_img)
        outputs=[];intro=temp/'intro.mp4';make_still(start_img,intro,1.6);outputs.append(intro)
        for n,(b,r) in enumerate(zip(doc['bouts'],records)):
            result=verified_results.get(b['bout_id'],{}).get('result')
            card=temp/f'bout_{n+1:02}.png'
            make_card(doc,logo,b,result).convert('RGB').save(card)
            for k,c in enumerate(r['clips']):
                dest=temp/f'bout_{n+1:02}_clip_{k+1:02}.mp4'
                make_clip(Path(r['source']),card,dest,c['start'],c['duration'],r['meta']['has_audio'])
                outputs.append(dest)
        end_img=temp/'outro.png';make_card(doc,logo).convert('RGB').save(end_img)
        outro=temp/'outro.mp4';make_still(end_img,outro,1.6);outputs.append(outro)
        playlist=temp/'concat.txt'
        playlist.write_text(''.join("file '" + str(p).replace("'", "'\\''") + "'\n" for p in outputs),encoding='utf-8')
        dest=output_dir/'RKK_event_recap_draft.mp4'
        command(['ffmpeg','-nostdin','-loglevel','error','-y','-f','concat','-safe','0',
                 '-i',str(playlist),'-c','copy','-movflags','+faststart',str(dest)])
        video=probe(dest)
        if video['width']!=W or video['height']!=H:raise RuntimeError('Unexpected output dimensions')
        packet['render']={'path':str(dest),'duration':video['duration'],'sha256':sha256(dest)}
        for net in sorted(ALLOWED):packet['outbox'][net]['media_local']=str(dest)
        # Cover: use first bout label screen; no unsourced photos.
        shutil.copyfile(temp/'bout_01.png',output_dir/'kansikuva.png')
    (output_dir/'publication_handoff.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (output_dir/'social_captions.json').write_text(json.dumps(outcap,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return packet


def main(argv=None)->int:
    p=argparse.ArgumentParser(description=__doc__)
    for flag in ('manifest','media-dir','logo','output-dir'):p.add_argument('--'+flag,required=True,type=Path)
    for flag in ('official-results','rights-records','ledger'):p.add_argument('--'+flag,type=Path)
    p.add_argument('--clips-per-bout',type=int,default=2)
    p.add_argument('--clip-seconds',type=float,default=3.0)
    p.add_argument('--preflight-only',action='store_true')
    ns=p.parse_args(argv)
    def read(path):return json.loads(path.read_text(encoding='utf-8')) if path else None
    res=run(read(ns.manifest),media_dir=ns.media_dir,logo=ns.logo,
            output_dir=ns.output_dir,official=read(ns.official_results),
            rights=read(ns.rights_records),ledger=read(ns.ledger),
            clip_duration=ns.clip_seconds,clips_per_bout=ns.clips_per_bout,render=not ns.preflight_only)
    print(res['status'],'\n'+'\n'.join(res['blockers']))
    print('No publication was sent; run in a private environment only.')
    return 0

if __name__=='__main__':raise SystemExit(main())
