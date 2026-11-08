"""Conservative mapping of provider-merged boxer identities, history and registrations."""
from copy import deepcopy
from urllib.parse import urlsplit
import re,unicodedata

def norm(v):return " ".join(unicodedata.normalize("NFC",str(v or "")).split()).casefold()
def canonical(v,cfg):
    n=norm(v);aliases={norm(k):norm(value) for k,value in cfg.get("boxer_name_aliases",{}).items()};seen=set()
    while n in aliases:
        if n in seen:raise ValueError("Cyclic identity alias")
        seen.add(n);n=aliases[n]
    return n
def same_person_name(a,b,cfg):return bool(norm(a)) and canonical(a,cfg)==canonical(b,cfg)
def participant_matches(label,name,clubs,cfg):
    v=norm(label)
    for club in sorted(clubs,key=len,reverse=True):
        c=norm(club)
        if not c:continue
        for suf in ("("+c+")",c):
            if v.endswith(suf) and same_person_name(v[:-len(suf)].strip(" ()·—–-"),name,cfg):return True
    return False
def index_roster(roster,cfg):
    byname,byid={},{}
    for b in roster:
        i,n=b.get("id"),canonical(b.get("name"),cfg)
        if not isinstance(i,str) or not re.fullmatch(r"[A-Za-z0-9_-]+",i) or not n or i in byid or n in byname:
            raise ValueError("Ambiguous or invalid merged roster")
        byid[i]=b;byname[n]=b
    if not byid:raise ValueError("Empty canonical roster")
    return byname,byid
def match_key(m):
    v=re.search(r"/e/([^/]+)/m/([^/]+)/?$",urlsplit(str(m.get("url") or "")).path)
    if v:return v.group(1),v.group(2)
    e=re.search(r"/e/([^/]+)/?$",urlsplit(str(m.get("event_url") or "")).path)
    if e and m.get("id"):return e.group(1),m["id"]
    return None
def prepare_identity(previous,roster,cfg):
    byname,byid=index_roster(roster,cfg)
    oldclub,newclub=previous.get("club_id"),cfg.get("club_id")
    if oldclub and oldclub!=newclub and oldclub not in cfg.get("merged_from_club_ids",[]):
        raise ValueError("Unapproved club migration")
    moving=bool(oldclub and oldclub!=newclub);direct=dict(previous.get("boxer_id_aliases",{}))
    for old in previous.get("boxers",[]):
        b=byname.get(canonical(old.get("name"),cfg))
        if not b:
            if moving:raise ValueError("Incomplete canonical roster")
            continue
        oid=old.get("id")
        if oid and oid!=b["id"]:
            if oid in byid:raise ValueError("Conflicting boxer ID")
            direct[oid]=b["id"]
    resolved={}
    for oid in direct:
        dest=oid;seen=set()
        while dest in direct:
            if dest in seen:raise ValueError("Cyclic boxer-ID aliases")
            seen.add(dest);dest=direct[dest]
        if dest in byid and dest!=oid and oid not in byid:resolved[oid]=dest
    profile={}
    for slug,name in cfg.get("profile_names_by_slug",{}).items():
        b=byname.get(canonical(name,cfg))
        if b:profile[slug]=b["id"]
    matches=[];seen=set()
    for original in previous.get("matches",[]):
        m=deepcopy(original);b=byname.get(canonical(m.get("boxer"),cfg))
        if b:
            prior=m.get("boxer");m["boxer"],m["boxer_id"]=b["name"],b["id"]
            for field in ("red_boxer","blue_boxer"):
                if same_person_name(m.get(field),prior,cfg):m[field]=b["name"]
        key=match_key(m);facts=tuple(m.get(f) for f in ("boxer","opponent","result","decision","method","round","event_date","winner_corner"))
        if key and (key,facts) in seen:continue
        if key:seen.add((key,facts))
        matches.append(m)
    regs={};unmapped=[]
    for src in previous.get("registrations",[]):
        r=deepcopy(src);b=byid.get(resolved.get(r.get("boxer_id"),r.get("boxer_id")))
        if b and not same_person_name(r.get("boxer"),b["name"],cfg):raise ValueError("Registration identity conflict")
        if not b:
            unmapped.append(r);continue
        r["boxer_id"],r["boxer"]=b["id"],b["name"]
        key=r.get("event_id"),b["id"]
        if key not in regs or str(r.get("observed_at",""))>str(regs[key].get("observed_at","")):regs[key]=r
    if moving and unmapped:raise ValueError("Unmapped registration in canonical migration")
    return {"boxer_id_aliases":resolved,"profile_ids_by_slug":profile,"matches":matches,"registrations":list(regs.values())+unmapped}
