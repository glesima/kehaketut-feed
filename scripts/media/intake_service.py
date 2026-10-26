#!/usr/bin/env python3
"""Private local Dropbox-sync inbox watcher. Never uploads or publishes.

Requires a separately configured local sync of /RKK/Uudet_videot; this script
does NOT authenticate to Dropbox. When new MP4s are stable it writes private
machine-readable HANDOFF/HOLD records. Publication rights, result verification,
and any social-media posting are deliberately outside this program.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import time
from pathlib import Path

from filming_intake import (
    MAX_BYTES, assignment_for, inspect_mp4, published_keys, read_json, sha256_file
)

SCHEMA = """CREATE TABLE IF NOT EXISTS files (
 name TEXT PRIMARY KEY,
 size INTEGER NOT NULL,
 mtime_ns INTEGER NOT NULL,
 stable_since REAL NOT NULL,
 last_seen REAL NOT NULL,
 metadata_key TEXT NOT NULL,
 state TEXT NOT NULL,
 sha256 TEXT,
 info_json TEXT
);
CREATE INDEX IF NOT EXISTS files_by_sha ON files(sha256);"""


def private_dir(path: Path) -> Path:
    if path.exists() and path.is_symlink():
        raise ValueError("Private output directory cannot be a symlink")
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name == "posix":
        path.chmod(0o700)
    return path.resolve(strict=True)


def db_connect(database: Path) -> sqlite3.Connection:
    private_dir(database.parent)
    if database.is_symlink():
        raise ValueError("Database cannot be a symlink")
    db = sqlite3.connect(database, timeout=10)
    if os.name == "posix":
        database.chmod(0o600)
    db.executescript(SCHEMA)
    return db


def write_private_json(target: Path, value: dict) -> None:
    tmp = target.with_name(target.name + ".tmp")
    if tmp.is_symlink():
        raise ValueError("Temporary output cannot be a symlink")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as out:
        json.dump(value, out, ensure_ascii=False, indent=2)
        out.write("\n")
        out.flush()
        os.fsync(out.fileno())
    os.replace(tmp, target)


def metadata_key(name: str, assignments: dict, published: set) -> str:
    doc = {"assignment": assignments.get(name), "published":
           sorted([list(x) for x in published])}
    return hashlib.sha256(json.dumps(doc, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def scan_once(folder: Path, db: sqlite3.Connection, outbox: Path,
              assignments: dict, ledger: dict, *,
              stable_seconds: int = 90, now: float | None = None) -> list[dict]:
    """Two observations and enough elapsed time; each new hash is inspected once.

    Reprocesses unchanged file if its trusted assignments/published ledger change.
    Every output is a HOLD and can never authorize posting.
    """
    if not folder.is_dir():
        raise FileNotFoundError("Dropbox-synced private folder is missing")
    if stable_seconds < 0:
        raise ValueError("stable_seconds must be nonnegative")
    now = time.time() if now is None else now
    outbox = private_dir(outbox)
    published = published_keys(ledger)
    results = []
    for path in sorted(folder.iterdir(), key=lambda p: p.name.casefold()):
        if path.suffix.lower() != ".mp4" or not path.is_file() or path.is_symlink():
            continue
        stat = path.stat()
        name = path.name
        key = metadata_key(name, assignments, published)
        row = db.execute(
            "SELECT size,mtime_ns,stable_since,last_seen,metadata_key,state,sha256,info_json "
            "FROM files WHERE name=?", (name,)
        ).fetchone()
        if row is None or row[0] != stat.st_size or row[1] != stat.st_mtime_ns:
            with db:
                db.execute("""INSERT INTO files
                  (name,size,mtime_ns,stable_since,last_seen,metadata_key,state,sha256,info_json)
                  VALUES(?,?,?,?,?,?,?,?,?)
                  ON CONFLICT(name) DO UPDATE SET
                    size=excluded.size,mtime_ns=excluded.mtime_ns,
                    stable_since=excluded.stable_since,last_seen=excluded.last_seen,
                    metadata_key=excluded.metadata_key,state=excluded.state,
                    sha256=NULL,info_json=NULL""",
                    (name, stat.st_size, stat.st_mtime_ns, now, now, key,
                     "OBSERVING", None, None))
            results.append({"name": name, "status": "OBSERVING"})
            continue

        if (now - row[2] < stable_seconds or
            now - stat.st_mtime < stable_seconds or now <= row[3]):
            results.append({"name": name, "status": "WAIT_STABLE"})
            continue

        if row[4] == key and row[5] not in ("OBSERVING", "WAIT_STABLE"):
            results.append({"name": name, "status": row[5]})
            continue

        reasons = []
        info: dict = {}
        digest = None
        if stat.st_size <= 0 or stat.st_size > MAX_BYTES:
            reasons.append("INVALID_FILE_SIZE")
        else:
            try:
                info = inspect_mp4(path)
                digest = sha256_file(path)
                after = path.stat()
                if after.st_size != stat.st_size or after.st_mtime_ns != stat.st_mtime_ns:
                    reasons.append("FILE_CHANGED_DURING_SCAN")
            except (OSError, ValueError, TimeoutError):
                reasons.append("INVALID_OR_INCOMPLETE_MP4")

        assignment, assignment_warnings = assignment_for(name, assignments)
        reasons.extend(assignment_warnings)
        if assignment and not assignment_warnings and (
                assignment["event_id"], assignment["bout_id"]) in published:
            reasons.append("ALREADY_PUBLISHED_BOUT_REVIEW_REUSE")

        if digest:
            duplicate = db.execute(
                "SELECT name FROM files WHERE sha256=? AND name<>? ORDER BY name LIMIT 1",
                (digest, name)
            ).fetchone()
            if duplicate:
                reasons.append("DUPLICATE_MEDIA_SHA256")
        # This watcher never accepts an uploader's "approved" field.
        reasons.append("INDEPENDENT_RIGHTS_AND_OFFICIAL_RESULTS_CHECK_REQUIRED")
        status = "HOLD" if digest else "HOLD_INVALID_MEDIA"
        result = {
            "schema": "RKK_LOCAL_INBOX_HANDOFF_V1", "status": status,
            "publication_ready": False, "source_filename": name,
            "bytes": stat.st_size, "source_sha256": digest,
            "video": info, "assignment": assignment, "blockers": reasons,
            "notes": "Private handoff only; no media upload, AI decision, or publication."
        }
        if digest:
            write_private_json(outbox / (digest + ".json"), result)
        with db:
            db.execute(
                "UPDATE files SET last_seen=?,metadata_key=?,state=?,sha256=?,info_json=? "
                "WHERE name=?", (now, key, status, digest,
                                json.dumps(result, ensure_ascii=False), name))
        results.append({"name": name, "status": status, "blockers": reasons})
    return results


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--folder", type=Path, required=True,
                    help="Private local folder synced separately from Dropbox File Request")
    ap.add_argument("--db", type=Path, required=True)
    ap.add_argument("--outbox", type=Path, required=True)
    ap.add_argument("--assignments", type=Path, help="Trusted filename-to-bout map")
    ap.add_argument("--published-ledger", type=Path)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--interval-seconds", type=int, default=30)
    ap.add_argument("--stable-seconds", type=int, default=90)
    args = ap.parse_args(argv)
    if args.interval_seconds < 1 or args.stable_seconds < 0:
        ap.error("invalid poll interval/stability threshold")
    if not args.once and args.stable_seconds < 30:
        ap.error("continuous mode requires at least 30 seconds stability")
    db = db_connect(args.db)
    try:
        while True:
            scan = scan_once(args.folder, db, args.outbox,
                             read_json(args.assignments), read_json(args.published_ledger),
                             stable_seconds=args.stable_seconds)
            print(json.dumps({"observed": len(scan),
                              "counts": {s: sum(x["status"] == s for x in scan)
                                         for s in sorted(set(x["status"] for x in scan))}},
                             ensure_ascii=False), flush=True)
            if args.once:
                break
            time.sleep(args.interval_seconds)
    except KeyboardInterrupt:
        return 0
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
