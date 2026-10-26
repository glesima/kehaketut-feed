#!/usr/bin/env python3
"""Offline video *activity* suggestions for a boxing editor, NOT punch scoring.

Reads a local source with ffmpeg, samples low-resolution grayscale frames in
configurable region of interest, ranks 4 s windows for movement, and writes a
review-only JSON file. It neither renders nor uploads, schedules or publishes.

Suggested ranges must be reviewed by a human for content, truth, image rights,
framing, and balance. Never copy candidate windows directly to published reels.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import statistics
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

WIDTH, HEIGHT, FPS = 112, 64, 2


@dataclass(frozen=True)
class Proposal:
    start: float
    duration: float
    activity_score: float
    crop_x: None = None


def ensure_percent_bounds(x: float, y: float, w: float, h: float) -> None:
    if any(not math.isfinite(v) for v in (x, y, w, h)):
        raise ValueError("Non-finite ROI")
    if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > 1 or y + h > 1:
        raise ValueError("ROI must lie inside the frame")


def motion_score(previous: bytes, frame: bytes, *, width: int = WIDTH,
                 height: int = HEIGHT, roi: tuple[float,float,float,float] = (.12, .17, .80, .66)) -> float:
    """Mean absolute luma difference in the ROI on sparse pixel grid.

    This measures generic visual motion/camera movement, not boxing skill.
    """
    if len(previous) != width * height or len(frame) != width * height:
        raise ValueError("Invalid grayscale frame size")
    x,y,w,h=roi
    ensure_percent_bounds(x,y,w,h)
    x0=max(0, math.floor(x*width)); y0=max(0,math.floor(y*height))
    x1=min(width,math.ceil((x+w)*width)); y1=min(height,math.ceil((y+h)*height))
    s=0; n=0
    for row in range(y0,y1,2):
        base=row*width
        for col in range(x0,x1,2):
            idx=base+col
            s+=abs(previous[idx]-frame[idx]);n+=1
    return round(s/max(n,1),4)


def propose_windows(activities: list[float], *, duration: float,
                    sample_fps: int=FPS, clip_seconds: float=4.0,
                    clip_count: int=8, stride_seconds: float=1.0,
                    min_gap_seconds: float=14.0,
                    head_skip_seconds: float=8.0,
                    tail_skip_seconds: float=4.0) -> list[Proposal]:
    if any(not math.isfinite(v) or v < 0 for v in activities):
        raise ValueError("Activity scores must be finite and non-negative")
    if duration<=0 or sample_fps<=0 or clip_seconds<=0 or clip_count<1 or clip_count>20:
        raise ValueError("Invalid duration/sample rate/window/count")
    if stride_seconds<=0 or min_gap_seconds<0 or head_skip_seconds<0 or tail_skip_seconds<0:
        raise ValueError("Invalid sampling/gap/skip")
    sample_count=max(1,int(round(clip_seconds*sample_fps)))
    stride=max(1,int(round(stride_seconds*sample_fps)))
    start_idx=int(math.ceil(head_skip_seconds*sample_fps))
    last_idx=int(math.floor((duration-tail_skip_seconds-clip_seconds)*sample_fps))
    if not activities or last_idx < start_idx or len(activities) < sample_count:
        return []

    # Subtract the typical quiet baseline to reduce scores from compression
    # noise or global illumination flicker. Rank stable by score, then time.
    baseline=statistics.median(activities)
    prefix=[0.0]
    for a in activities:
        prefix.append(prefix[-1]+max(0,a-baseline))
    pool=[]
    for s in range(start_idx,last_idx+1,stride):
        e=s+sample_count
        if e>len(activities):break
        mean=(prefix[e]-prefix[s])/sample_count
        pool.append((mean,s/sample_fps))
    pool.sort(key=lambda p:(-p[0],p[1]))
    selected=[]
    for score,start in pool:
        if any(abs(start-p.start) < clip_seconds+min_gap_seconds for p in selected):continue
        selected.append(Proposal(round(start,2),round(clip_seconds,2),round(score,3)))
        if len(selected)>=clip_count:break
    return sorted(selected,key=lambda p:p.start)


def ffprobe(source:Path) -> dict:
    proc=subprocess.run(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_type,width,height','-of','json',str(source)],
        capture_output=True,text=True,check=True)
    doc=json.loads(proc.stdout)
    streams=[s for s in doc.get('streams',[]) if s.get('codec_type')=='video']
    if not streams:raise ValueError('No video stream')
    return {'duration':float(doc['format']['duration']),
            'width':int(streams[0]['width']),'height':int(streams[0]['height'])}


def analyze_video(source:Path, roi:tuple[float,float,float,float], sample_fps:int=FPS,
                  max_duration_seconds:float=3600) -> tuple[dict,list[float]]:
    if not source.is_file():raise FileNotFoundError(str(source))
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise RuntimeError('ffmpeg and ffprobe required')
    meta=ffprobe(source)
    if not 1<=meta['duration']<=max_duration_seconds:
        raise ValueError('Source duration exceeds bounded analysis limit')
    # Input is a local video file only; no network endpoints or writes.
    cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-i',str(source),
         '-an','-vf',f'fps={sample_fps},scale={WIDTH}:{HEIGHT},format=gray',
         '-f','rawvideo','-pix_fmt','gray','pipe:1']
    proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    frame_bytes=WIDTH*HEIGHT
    prev=None; act=[]
    try:
        while True:
            data=proc.stdout.read(frame_bytes)
            if not data:break
            if len(data)!=frame_bytes:raise ValueError('Truncated grayscale video frame')
            # Each activity element corresponds to a frame timestamp.
            act.append(motion_score(prev,data,roi=roi) if prev is not None else 0.0)
            prev=data
            if len(act)>math.ceil(meta['duration']*sample_fps)+4:
                raise ValueError('Unexpected frame count')
    finally:
        proc.stdout.close()
    err=proc.stderr.read().decode('utf-8','replace')[-1200:]
    if proc.wait()!=0:
        raise RuntimeError('ffmpeg analysis failed: '+err)
    return meta,act


def cli(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--count',type=int,default=8)
    p.add_argument('--clip-seconds',type=float,default=4.)
    p.add_argument('--min-gap',type=float,default=14.)
    p.add_argument('--skip-start',type=float,default=8.)
    p.add_argument('--skip-end',type=float,default=4.)
    p.add_argument('--roi',default='0.12,0.17,0.80,0.66',
                   help='Normalized region x,y,w,h, used only for visual movement')
    ns=p.parse_args(argv)
    roi=tuple(float(x) for x in ns.roi.split(','))
    if len(roi)!=4:raise ValueError('ROI must be four comma-separated values')
    ensure_percent_bounds(*roi)
    meta,acts=analyze_video(ns.source,roi)
    candidates=propose_windows(acts,duration=meta['duration'],
        clip_seconds=ns.clip_seconds,clip_count=ns.count,
        min_gap_seconds=ns.min_gap,head_skip_seconds=ns.skip_start,
        tail_skip_seconds=ns.skip_end)
    doc={'schema':'RKK_ACTIVITY_PROPOSALS_V1',
         'status':'REVIEW_ONLY_NO_AUTOMATIC_HIGHLIGHT_APPROVAL',
         'source_properties':meta,'sample_fps':FPS,
         'roi':list(roi),'candidate_count':len(candidates),
         'candidates':[asdict(p) for p in candidates],
         'warnings':['Movement is not punching accuracy, match score or boxing quality.',
                     'Camera pans, referee movement and cheering can produce false positives.',
                     'Review source video, crop_x, image rights and editorial fairness before editing.',
                     'This file is not a publication manifest. No video is uploaded, scheduled or published.']}
    ns.output.parent.mkdir(parents=True,exist_ok=True)
    ns.output.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Created review-only proposals:',ns.output,'count=',len(candidates))
    return 0

if __name__=='__main__':raise SystemExit(cli())
