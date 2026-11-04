#!/usr/bin/env python3
"""Verify candidate public data after a live refresh. No network or writes."""
import argparse,json
from pathlib import Path


def verify(before,after,config):
    assert after['club_id']==config['club_id']=='mZjkT0LW248X'
    assert after['club_url']==config['club_url']
    ids=[b['id'] for b in after['boxers']]
    assert len(ids)==len(set(ids))
    assert set(config['boxer_id_aliases'].values())<=set(ids)
    assert all(not b.get('stats_source_url') and not b.get('stats_source_note') for b in after['boxers'])
    bouts={m['id']:m for m in after['matches']}
    for old in before.get('matches',[]):
        assert old['id'] in bouts,('lost_bout',old['id'])
        new=bouts[old['id']]
        for field in ['decision','result','event_date','opponent']:
            assert old.get(field)==new.get(field),('unexpected_history_change',old['id'],field)
    aliases=config['boxer_id_aliases']
    regs=after.get('registrations',[])
    keys=[(r['event_id'],r['boxer_id']) for r in regs]
    assert len(keys)==len(set(keys))
    for old in before.get('registrations',[]):
        if old.get('event_date','')>='2026-11-04':
            assert (old['event_id'],aliases.get(old['boxer_id'],old['boxer_id'])) in keys
    return {'club_id':after['club_id'],'boxers':len(ids),
        'old_results_preserved':len(before.get('matches',[])),
        'current_results':len(bouts),'registrations':len(regs),
        'inconsistent_summary_profiles':[b['name'] for b in after['boxers'] if b.get('stats_consistency')=='inconsistent'],
        'boxers_checked_at':after.get('boxers_checked_at'),'matches_checked_at':after.get('matches_checked_at')}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('before',type=Path)
    p.add_argument('--after',type=Path,default=Path('docs/data.json'))
    a=p.parse_args()
    print(json.dumps(verify(json.loads(a.before.read_text()),json.loads(a.after.read_text()),json.loads(Path('config.json').read_text())),ensure_ascii=False,indent=2))
