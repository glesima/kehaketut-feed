"""Reusable RKK TV/Broadcast branding for an offline, review-only boxing video.

Creates static graphics and a cover from *real* source frames. All factual text
comes from the supplied human-checked manifest. No synthetic fight footage.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

W,H=1080,1920
PANEL_Y,PANEL_H=432,930
RED=(190,31,49)
BLUE=(72,127,212)
WHITE=(246,248,250)
MUTED=(170,185,201)


def font(sz:int,bold:bool=True):
    paths=(['/usr/share/fonts/truetype/noto/NotoSans-ExtraBold.ttf',
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
        if bold else ['/usr/share/fonts/truetype/noto/NotoSans-Medium.ttf',
                      '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for p in paths:
        if Path(p).is_file():return ImageFont.truetype(p,sz)
    raise RuntimeError('Install Noto Sans or DejaVu Sans fonts')


def fitted(d:ImageDraw.ImageDraw, txt:str, start:int, available:int, min_size:int=16):
    for n in range(start,min_size-1,-1):
        f=font(n)
        if d.textbbox((0,0),txt,font=f)[2]<=available:return f
    raise ValueError('Text is too long for broadcast graphic: '+txt[:50])


def logo_image(source:Path, width:int, height:int):
    img=Image.open(source).convert('RGBA'); bb=img.getchannel('A').getbbox()
    if not bb:raise ValueError('Logo is fully transparent')
    img=img.crop(bb);img.thumbnail((width,height),Image.Resampling.LANCZOS)
    return img


def preview_frame(src:Path, dest:Path, timestamp:float) -> Image.Image:
    subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-ss',str(timestamp),
                    '-i',str(src),'-frames:v','1',str(dest)],check=True)
    return Image.open(dest).convert('RGB')


def render_assets(m:dict, media:dict, clips:list, source:Path, logo:Path, outdir:Path) -> dict:
    """Return file paths matching build_reel.make_assets' output contract."""
    outdir.mkdir(exist_ok=True,parents=True)
    if not clips:raise ValueError('At least one approved clip required')
    selected=clips[len(clips)//2]
    timestamp=selected.start+selected.duration*.5
    original=preview_frame(source,outdir/'raw_cover_frame.png',timestamp)
    # This original frame is used only as blurred background and cover; no AI
    # generated punches or inaccurate photographic substitutions.
    blur=ImageOps.fit(original,(W,H),method=Image.Resampling.BICUBIC)
    blur=ImageEnhance.Brightness(blur.filter(ImageFilter.GaussianBlur(45))).enhance(.22)
    canvas=blur.convert('RGBA')
    tone=Image.new('RGBA',(W,H));shade=ImageDraw.Draw(tone)
    for y in range(H):
        alpha=132+round(48*abs(y/H-.5)*2)
        shade.line([(0,y),(W,y)],fill=(8,14,22,alpha))
    canvas=Image.alpha_composite(canvas,tone)
    d=ImageDraw.Draw(canvas)
    for j in range(-700,1800,175):
        d.line([(j,0),(j+500,H)],fill=(105,122,143,16),width=2)
    d.rectangle((0,0,W,15),fill=(*RED,255))
    d.rectangle((0,PANEL_Y-11,W,PANEL_Y-4),fill=(*RED,255))
    d.rectangle((0,PANEL_Y+PANEL_H,W,PANEL_Y+PANEL_H+6),fill=(*RED,255))
    d.rounded_rectangle((58,31,300,78),radius=8,fill=(178,31,46,211))
    d.text((72,42),'OTTELUKOOSTE',font=font(23),fill=WHITE)
    place_date=f"{m['place'].upper()}  •  {m['date']}"
    d.text((W-55,46),place_date,font=fitted(d,place_date,23,650),anchor='ra',fill=MUTED)
    mark=logo_image(logo,700,175);canvas.alpha_composite(mark,((W-mark.width)//2,101))
    d=ImageDraw.Draw(canvas)
    d.rounded_rectangle((49,305,1031,405),radius=16,fill=(9,16,23,224),outline=(95,111,128,190),width=2)
    d.rounded_rectangle((65,316,78,391),radius=4,fill=(*RED,255))
    d.rounded_rectangle((1004,316,1017,391),radius=4,fill=(*BLUE,255))
    rn=m['red'].upper();bn=m['blue'].upper()
    d.text((102,330),rn,font=fitted(d,rn,34,340),fill=WHITE)
    d.text((530,336),'VS',font=font(30),anchor='mm',fill=(255,207,210))
    d.text((976,330),bn,font=fitted(d,bn,34,385),anchor='ra',fill=WHITE)
    # The bottom part is deliberately not a caption area: apps draw UI there.
    for j in range(6):
        x=80+j*43
        d.line([(x,1480),(x+122,1880)],fill=(*RED,19+j*3),width=7)
        x=770+j*43
        d.line([(x,1480),(x-122,1880)],fill=(*BLUE,15+j*3),width=7)
    for i in range(10,0,-1):
        alpha=6+4*(10-i)
        d.rectangle((i,PANEL_Y+i,W-i,PANEL_Y+PANEL_H-i),outline=(255,255,255,alpha))
    canvas.save(outdir/'background.png')

    result=Image.new('RGBA',(W,H));dr=ImageDraw.Draw(result)
    dr.rounded_rectangle((37,465,1043,588),radius=16,
                         fill=(6,13,22,240),outline=(210,64,82,245),width=3)
    dr.rectangle((45,476,57,576),fill=(*RED,255))
    dr.text((82,478),'OTTELUN LOPPUTULOS',font=font(23),fill=(255,186,192))
    rs=m['result'].upper()
    dr.text((80,514),rs,font=fitted(dr,rs,43,885),fill=WHITE)
    result.save(outdir/'result.png')

    outro=Image.new('RGBA',(W,H));od=ImageDraw.Draw(outro)
    od.rounded_rectangle((106,710,974,1219),radius=32,
                          fill=(10,17,24,240),outline=(194,43,62,240),width=4)
    od.rectangle((151,750,930,756),fill=(*RED,255))
    outlogo=logo_image(logo,712,202);outro.alpha_composite(outlogo,((W-outlogo.width)//2,812))
    od=ImageDraw.Draw(outro)
    site=m.get('website','KEHAKETUT.FI').upper()
    od.text((W//2,1080),site,font=fitted(od,site,47,805),anchor='mm',fill=WHITE)
    od.text((W//2,1155),'NYRKKEILYÄ  •  RIIHIMÄELLÄ',font=font(22),anchor='mm',fill=MUTED)
    outro.save(outdir/'outro.png')

    cw=min(media['width'],round(media['height']*W/PANEL_H))
    picture=original.crop((selected.crop_x,0,selected.crop_x+cw,media['height']))
    picture=picture.resize((W,PANEL_H),Image.Resampling.LANCZOS)
    cover=canvas.copy();cover.alpha_composite(picture.convert('RGBA'),(0,PANEL_Y))
    cover.convert('RGB').save(outdir/'kansikuva.jpg',quality=91,subsampling=0)
    return {'seconds':sum(c.duration for c in clips), 'background':'background.png',
            'result':'result.png','outro':'outro.png','cover':'kansikuva.jpg'}
