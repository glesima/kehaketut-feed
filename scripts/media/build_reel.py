#!/usr/bin/env python3
"""Render a PRIVATE, approval-only Riihimäen Kehä-Ketut boxing highlight draft.

Input: local MP4, local club logo PNG, and a manifest of human-vetted clip timecodes.
Output: vertical MP4, cover JPG, previews, manifest, and render log.

Never uploads, schedules, or publishes. Never stores original private video in GitHub.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
PANEL_Y, PANEL_H = 432, 930
RED = (185,28,43)
BLUE = (41,77,137)
INK = (15,20,26)
WHITE = (245,247,250)
MUTED = (158,174,187)

@dataclass(frozen=True)
class Clip:
    start: float
    duration: float
    crop_x: int


def command(cmd:list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if p.returncode:
        raise RuntimeError(f"Command failed ({p.returncode}): {cmd[0]}\n{p.stderr[-1800:]}")
    return p.stdout


def probe(src:Path) -> dict:
    v=json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(src)]))
    vs=next((s for s in v['streams'] if s['codec_type']=='video'),None)
    if vs is None: raise ValueError('Source file has no video stream')
    return {'width':int(vs['width']),'height':int(vs['height']),
            'duration':float(v['format']['duration']),
            'has_audio':any(s['codec_type']=='audio' for s in v['streams'])}


def validate(m:dict,media:dict) -> list[Clip]:
    required=['event','date','place','red','blue','division','result','clips']
    for key in required:
        if key not in m:raise ValueError(f'Missing manifest key: {key}')
    for key in required[:-1]:
        if not isinstance(m[key],str) or len(m[key])>160 or not m[key].strip():
            raise ValueError(f'Invalid manifest text: {key}')
    if not isinstance(m['clips'],list) or not 1<=len(m['clips'])<=20:
        raise ValueError('Provide 1..20 reviewed clips')
    cw=min(media['width'],round(media['height']*W/PANEL_H))
    clips=[]
    for i, c in enumerate(m['clips']):
        try:
            a=float(c['start']);d=float(c['duration']);x=int(c.get('crop_x',0))
        except (KeyError,TypeError,ValueError) as e:raise ValueError(f'Clip {i+1} has invalid fields') from e
        if not math.isfinite(a) or not math.isfinite(d) or a<0 or not 0.4<=d<=10 or a+d>media['duration']+.05:
            raise ValueError(f'Clip {i+1} lies outside source or has invalid duration')
        if x<0 or x>media['width']-cw:
            raise ValueError(f'Clip {i+1} crop_x must be from 0 to {media["width"]-cw}')
        clips.append(Clip(a,d,x))
    total=sum(c.duration for c in clips)
    if not 5<=total<=60:raise ValueError('Total highlight duration must be 5..60 seconds')
    return clips


def get_font(px:int,bold=True) -> ImageFont.FreeTypeFont:
    paths=([
        '/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    ] if bold else [
        '/usr/share/fonts/truetype/noto/NotoSans-Medium.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    ])
    path=next((p for p in paths if Path(p).is_file()),None)
    if path is None:raise RuntimeError('Install Noto Sans or DejaVu Sans fonts')
    return ImageFont.truetype(path,px)


def text_fit(draw:ImageDraw.ImageDraw,txt:str,maxw:int,start:int=55,minimum:int=17,**kwargs):
    for px in range(start,minimum-1,-1):
        f=get_font(px)
        if draw.textbbox((0,0),txt,font=f,**kwargs)[2]<=maxw:return f
    raise ValueError(f'Text is too long to fit safely: {txt[:45]}')


def resize_logo(path:Path,maxw:int,maxh:int) -> Image.Image:
    im=Image.open(path).convert('RGBA'); box=im.getchannel('A').getbbox()
    if not box:raise ValueError('Logo is empty/transparent')
    im=im.crop(box)
    im.thumbnail((maxw,maxh),Image.Resampling.LANCZOS)
    return im


def draw_background(m:dict, logo:Path) -> Image.Image:
    """Shorts/Reels safe-space layout: all essential facts above platform UI.

    Video platforms overlay title, username, captions and buttons in the
    lower portion of the portrait frame. No names, result or link are written
    to the bottom 28 percent of the frame.
    """
    im=Image.new('RGB',(W,H)); dr=ImageDraw.Draw(im)
    for y in range(H):
        f=y/H
        dr.line([(0,y),(W,y)],fill=(int(14+f*6),int(19+f*6),int(25+f*8)))
    for x in range(-450,1600,118):
        dr.line([(x,0),(x+430,H)],fill=(38,45,54),width=1)
    dr.rectangle((0,0,W,14),fill=RED)
    dr.rectangle((0,426,W,432),fill=RED)
    dr.rectangle((0,1362,W,1366),fill=RED)
    rgb=im.convert('RGBA')
    brand=resize_logo(logo,850,205)
    rgb.alpha_composite(brand,((W-brand.width)//2,23))
    dr=ImageDraw.Draw(rgb)
    dr.text((59,236),'OTTELUKOOSTE',font=get_font(65),fill=WHITE)
    dr.rectangle((60,321,121,327),fill=RED)
    fighters=f'{m["red"].upper()}  VS  {m["blue"].upper()}'
    dr.text((58,333),fighters,font=text_fit(dr,fighters,960,40,25),fill=WHITE)
    dr.text((59,383),m['place'].upper()+' / '+m['date'],
            font=text_fit(dr,m['place'].upper()+' / '+m['date'],910,28,21),fill=MUTED)
    # Do not put any essential content at y>=1366.
    return rgb


def draw_result(m:dict) -> Image.Image:
    """Late result card lives above the Shorts/Reels interface area."""
    im=Image.new('RGBA',(W,H)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((58,461,1018,574),radius=17,
        fill=(17,24,32,236),outline=(188,59,69,255),width=3)
    d.text((90,472),'OTTELUN TULOS',font=get_font(23),fill=(255,181,188))
    result=m['result'].upper()
    d.text((89,507),result,font=text_fit(d,result,885,38,24),fill=WHITE)
    return im


def draw_outro(logo:Path,website:str) -> Image.Image:
    out=Image.new('RGBA',(W,H)); sh=Image.new('RGBA',(W,H));d=ImageDraw.Draw(sh)
    d.rounded_rectangle((76,768,1004,1172),radius=34,fill=(0,0,0,175))
    out=Image.alpha_composite(out,sh.filter(ImageFilter.GaussianBlur(20)))
    d=ImageDraw.Draw(out)
    d.rounded_rectangle((58,740,1022,1154),radius=24,fill=(12,17,23,236),outline=(*RED,245),width=5)
    d.rounded_rectangle((106,1110,974,1118),radius=3,fill=(*RED,230))
    lg=resize_logo(logo,820,211);out.alpha_composite(lg,((W-lg.width)//2,785))
    d=ImageDraw.Draw(out)
    site=website.upper()
    d.text((W//2,1033),site,font=text_fit(d,site,830,43,25),anchor='mt',fill=WHITE)
    return out


def cover_frame(source:Path,output:Path,t:float,cropw:int,height:int,x:int) -> Image.Image:
    f=output/'raw_cover_frame.png'
    command(['ffmpeg','-nostdin','-v','error','-y','-ss',str(t),'-i',str(source),'-frames:v','1',str(f)])
    im=Image.open(f).convert('RGB')
    return im.crop((x,0,x+cropw,height)).resize((W,PANEL_H),Image.Resampling.LANCZOS)


def make_assets(m:dict,media:dict,clips:list[Clip],source:Path,logo:Path,outdir:Path,style:str='standard')->dict:
    if style=='broadcast':
        from broadcast_style import render_assets
        return render_assets(m,media,clips,source,logo,outdir)
    if style!='standard':raise ValueError('Unknown style')
    outdir.mkdir(parents=True,exist_ok=True)
    bg=draw_background(m,logo);bg.convert('RGB').save(outdir/'background.png')
    result=draw_result(m);result.save(outdir/'result.png')
    outro=draw_outro(logo,m.get('website','KEHAKETUT.FI'));outro.save(outdir/'outro.png')
    total=sum(c.duration for c in clips)
    # Pick a frame from the penultimate selected clip to ensure it is actual footage.
    c=clips[-2] if len(clips)>=2 else clips[0]
    cw=min(media['width'],round(media['height']*W/PANEL_H))
    shot=cover_frame(source,outdir,c.start+c.duration*.5,cw,media['height'],c.crop_x)
    cover=bg.copy();cover.alpha_composite(shot.convert('RGBA'),(0,PANEL_Y))
    d=ImageDraw.Draw(cover)
    d.rounded_rectangle((55,1100,1025,1290),radius=19,fill=(10,16,22,236))
    d.text((82,1127),f'{m["red"].upper()}  VS  {m["blue"].upper()}',font=text_fit(d,f'{m["red"].upper()}  VS  {m["blue"].upper()}',920,45,22),fill=WHITE)
    d.text((83,1210),m['place'].upper()+'  '+m['date'][-4:],font=get_font(28),fill=(251,185,190))
    cover.convert('RGB').save(outdir/'kansikuva.jpg',quality=92,subsampling=0)
    return {'seconds':total,'background':'background.png','result':'result.png','outro':'outro.png','cover':'kansikuva.jpg'}


def encode_segments(source:Path, clips:list[Clip], media:dict, outdir:Path)->Path:
    """Sequentially fast-seek and encode 1 clip at a time, avoiding 8 parallel decoders.

    Segment files are PRIVATE intermediates (never uploaded by this script).
    """
    sd=outdir/'private_segments';sd.mkdir(exist_ok=True)
    cw=min(media['width'],round(media['height']*W/PANEL_H))
    paths=[]
    for i,c in enumerate(clips):
        segment=sd/f'clip_{i+1:02d}.mp4'
        args=['ffmpeg','-nostdin','-v','error','-y','-ss',str(c.start),'-t',str(c.duration),'-i',str(source)]
        if not media['has_audio']:
            args.extend(['-f','lavfi','-t',str(c.duration),'-i','anullsrc=channel_layout=stereo:sample_rate=48000'])
        video_filter=f'crop={cw}:{media["height"]}:{c.crop_x}:0,scale={W}:{PANEL_H}:flags=bicubic,eq=contrast=1.035:saturation=1.055,fps=25,setsar=1'
        args.extend(['-map','0:v:0','-map',('0:a:0' if media['has_audio'] else '1:a:0'),'-vf',video_filter,
            '-af',f'aresample=48000,afade=t=in:st=0:d=0.06,afade=t=out:st={max(c.duration-.14,0):.3f}:d=0.14',
            '-r','25','-c:v','libx264','-preset','ultrafast','-crf','18',
            '-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000','-ac','2',
            '-movflags','+faststart',str(segment)])
        command(args)
        paths.append(segment)
    list_path=sd/'concat.txt'
    list_path.write_text(''.join("file '"+str(p).replace("'", "'\\''")+"'\n" for p in paths),encoding='utf-8')
    mont=sd/'montage.mp4'
    command(['ffmpeg','-nostdin','-v','error','-y','-f','concat','-safe','0','-i',str(list_path),'-c','copy','-movflags','+faststart',str(mont)])
    return mont


def build_filters(total:float)->str:
    fs=[
        f'[1:v]scale={W}:{H},fps=25,format=yuv420p[bg];',
        f'[bg][0:v]overlay=x=0:y={PANEL_Y}:shortest=1:format=auto[cv];',
        f'[2:v]format=rgba,fade=t=in:st={max(total-7,0):.3f}:d=0.25:alpha=1[rs];',
        '[cv][rs]overlay=x=0:y=0:shortest=1:format=auto[with_result];',
        f'[3:v]format=rgba,fade=t=in:st={max(total-3,0):.3f}:d=0.5:alpha=1[outro];',
        '[with_result][outro]overlay=x=0:y=0:shortest=1:format=auto[outv];',
        f'[0:a]acompressor=threshold=-18dB:ratio=2.0:attack=20:release=200,alimiter=limit=0.91,afade=t=out:st={max(total-.7,0):.3f}:d=0.7[outa]'
    ]
    return '\n'.join(fs)


def create_caption_drafts(m:dict,outdir:Path)->None:
    """Deterministic drafts from VERIFIED manifest facts, no invented statements."""
    opponent=f'{m["red"]} – {m["blue"]}'
    event=m['event']
    source=m.get('source_url','')
    site=m.get('website','kehaketut.fi').lower()
    ing='\n'.join([
        f'🥊 Kehä-Ketut kehässä – {m["place"]}!',
        '',
        f'Ottelijat: {m["red"]} (punainen) ja {m["blue"]} (sininen). {event}, {m["date"]}.',
        f'{m["division"]}. Ottelun tulos: {m["result"]}.',
        '',
        'Videolla lyhyt kooste kehässä nähdyistä tilanteista. Kiitos kilpailujen järjestäjille ja mukana olleille!',
        '',
        '#KehäKetut #Nyrkkeily #Riihimäki'
    ])
    fb='\n'.join([
        f'🥊 Ottelukooste – {event} ({m["date"]})',
        '',
        f'Ottelu: {m["red"]} (punainen) – {m["blue"]} (sininen). Paikka: {m["place"]}.',
        f'Sarja: {m["division"]}. Tulos: {m["result"]}.',
        '',
        'Tässä lyhyt kooste ottelun tapahtumista. Kiitos ottelijoille, valmentajille ja järjestäjille!',
        '',
        'Lisätietoja seurasta: https://www.kehaketut.fi/',
        *( [f'Virallinen lähde: {source}'] if source else [] ),
    ])
    yt_title=f'{m["red"]} vs {m["blue"]} | {m["place"]} {m["date"]} | Ottelukooste'
    if len(yt_title)>100:
        yt_title=f'{m["red"]} vs {m["blue"]} | {m["date"]} | Shorts'[:100]
    yt='\n'.join([
        f'Otsikko: {yt_title}',
        '',
        f'{event}, {m["place"]}, {m["date"]}.',
        f'{opponent}. Sarja: {m["division"]}. Tulos: {m["result"]}.',
        'Lyhyt autenttinen ottelukooste, ei koko ottelutallenne.',
        '',
        *( [f'Lähde: {source}'] if source else [] ),
        'https://www.kehaketut.fi/',
        '',
        '#KehäKetut #Nyrkkeily #Shorts',
    ])
    for name,body in [('instagram',ing),('facebook',fb),('youtube',yt)]:
        (outdir/f'{name}_luonnos.txt').write_text(body+'\n',encoding='utf-8')
    (outdir/'somejulkaisut_luonnos.md').write_text(
        '# Kehä-Ketut – ihmisen tarkistettavat julkaisuluonnokset\n\n'
        'Nimet, päivämäärät ja tulokset tulevat annetusta JSON-manifestista. '
        'Julkaiseminen edellyttää faktatarkistusta ja kuva-/julkaisuoikeuksia. '
        'Tämä työkalu **ei** julkaise mitään.\n\n'
        + '## Instagram\n\n'+ing+'\n\n## Facebook\n\n'+fb+'\n\n## YouTube Shorts\n\n'+yt+'\n',
        encoding='utf-8'
    )


def main(argv=None)->int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True,help='Local privately stored MP4 file')
    p.add_argument('--logo',type=Path,required=True,help='User-authorized official transparent PNG logo')
    p.add_argument('--manifest',type=Path,required=True,help='JSON with checked names, result and clip timings')
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--style',choices=['standard','broadcast'],default='standard')
    p.add_argument('--dry-run',action='store_true',help='Validate and create stills/filter graph, do not render MP4')
    a=p.parse_args(argv)
    for x in [a.source,a.logo,a.manifest]:
        if not x.is_file():raise SystemExit('Input file not found: '+str(x))
    if shutil.which('ffmpeg') is None or shutil.which('ffprobe') is None:
        raise SystemExit('ffmpeg and ffprobe required')
    m=json.loads(a.manifest.read_text(encoding='utf-8'));media=probe(a.source); clips=validate(m,media)
    desc=make_assets(m,media,clips,a.source,a.logo,a.output_dir,style=a.style)
    create_caption_drafts(m,a.output_dir)
    filters=build_filters(desc['seconds']);(a.output_dir/'filter_complex.txt').write_text(filters,encoding='utf-8')
    (a.output_dir/'render_metadata.json').write_text(json.dumps({'format':'RKK_REEL_DRAFT_V1','style':a.style,'status':'REVIEW_ONLY_NO_PUBLICATION','source_properties':media,'render':desc,'clips': [c.__dict__ for c in clips], 'claim_source':m.get('source_url',''), 'manifest':m},ensure_ascii=False,indent=2),encoding='utf-8')
    if a.dry_run:
        print('DRY RUN OK: no video created and nothing was published'); return 0
    outfile=a.output_dir/(re.sub(r'[^a-zA-Z0-9_-]+','_',m.get('slug','rkk-ottelukooste'))+'_draft.mp4')
    montage=encode_segments(a.source,clips,media,a.output_dir)
    cmd=['ffmpeg','-nostdin','-hide_banner','-y','-i',str(montage)]
    for image_name in ['background.png','result.png','outro.png']:
        cmd.extend(['-loop','1','-framerate','25','-i',str(a.output_dir/image_name)])
    cmd.extend(['-filter_complex_script',str(a.output_dir/'filter_complex.txt'),'-map','[outv]','-map','[outa]','-c:v','libx264','-preset','ultrafast','-crf','23','-pix_fmt','yuv420p','-r','25','-c:a','aac','-b:a','160k','-t',str(round(desc['seconds'],4)),'-movflags','+faststart',str(outfile)])
    print('Rendering:',outfile,flush=True)
    p2=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    (a.output_dir/'ffmpeg.log').write_text(p2.stderr,encoding='utf-8')
    if p2.returncode:raise SystemExit('Failed to render; see ffmpeg.log\n'+p2.stderr[-1200:])
    after=probe(outfile)
    if abs(after['duration']-desc['seconds'])>.15 or after['width']!=W or after['height']!=H:
        raise RuntimeError(f'Unexpected output duration/resolution: {after}')
    print('Draft ready for human approval:',outfile)
    print('Nothing was published or scheduled.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())