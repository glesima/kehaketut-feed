#!/usr/bin/env python3
"""Offline RKK media inbox inventory: technical checks and mapping only.

This script NEVER uploads, emails, publishes, changes Dropbox or trusts an
uploader claim of consent. The media stays in a private local synced folder.
A separate rights service and verified bout-results source must approve any
future unattended publishing. A field such as `approved: true` is NOT accepted
as publication authorization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
import time
from pathlib import Path
from typing import Any

KINDS = {"full_bout", "vertical_broll", "interview_pre", "interview_post", "coach_interview", "other"}
MAX_BYTES = 3_000_000_000
MAX_DURATION = 3600


def read_json(path: Path | None) -> dict:
    if not path:
        return {}
    v = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(v, dict):
        raise ValueError("JSON root must be object")
    return v


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as inp:
        for chunk in iter(lambda: inp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inspect_mp4(path: Path) -> dict:
    proc = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        text=True, capture_output=True, check=False, timeout=90,
    )
    if proc.returncode:
        raise ValueError("ffprobe failed (invalid or incomplete media)")
    try:
        doc = json.loads(proc.stdout)
        streams = doc.get("streams", [])
        video = next(s for s in streams if s.get("codec_type") == "video")
        rate = video.get("avg_frame_rate", "0/1")
        num, den = (int(x) for x in rate.split("/", 1))
        fps = (num / den) if den else 0
        result = {
            "duration_seconds": round(float(doc["format"]["duration"]), 2),
            "width": int(video["width"]),
            "height": int(video["height"]),
            "fps": round(fps, 2),
            "codec": video.get("codec_name"),
            "audio": any(s.get("codec_type") == "audio" for s in streams),
        }
        if (not math.isfinite(result["duration_seconds"]) or
            result["duration_seconds"] < 3 or result["duration_seconds"] > MAX_DURATION or
            result["width"] <= 0 or result["height"] <= 0 or fps <= 0):
            raise ValueError("invalid duration, resolution or frame rate")
        return result
    except (ValueError, StopIteration, TypeError, KeyError, ZeroDivisionError) as exc:
        raise ValueError("unable to read valid video metadata") from exc


def assignment_for(name: str, assignments: dict) -> tuple[dict | None, list[str]]:
    """Explicit human-provided map; never infer a boxer from frames or filename."""
    if not isinstance(assignments, dict):
        raise ValueError("assignments must be object")
    a = assignments.get(name)
    if a is None:
        return None, ["MISSING_EXPLICIT_EVENT_AND_BOUT_MAPPING"]
    if not isinstance(a, dict):
        return None, ["INVALID_ASSIGNMENT"]
    event = a.get("event_id")
    bout = a.get("bout_id")
    kind = a.get("kind")
    if (not isinstance(event, str) or not re.fullmatch(r"[A-Za-z0-9_-]{4,80}", event)
            or not isinstance(bout, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", bout)
            or kind not in KINDS):
        return a, ["MISSING_OR_INVALID_EVENT_BOUT_KIND"]
    return {"event_id": event, "bout_id": bout, "kind": kind, "provided_by": a.get("provided_by")}, []


def published_keys(ledger: dict) -> set[tuple[str, str]]:
    records = ledger.get("published_bouts", [])
    if not isinstance(records, list):
        raise ValueError("published_bouts must be an array")
    keys = set()
    for x in records:
        if not isinstance(x, dict) or not isinstance(x.get("event_id"), str) or not isinstance(x.get("bout_id"), str):
            raise ValueError("invalid published bout ledger entry")
        keys.add((x["event_id"], x["bout_id"]))
    return keys


def inventory(folder: Path, assignments: dict, ledger: dict,
              *, settle_seconds: int = 60, now: float | None = None) -> dict:
    """Read-only technical intake. Always HOLD until independent rights checks."""
    if not folder.is_dir():
        raise FileNotFoundError("local private intake folder does not exist")
    if settle_seconds < 0:
        raise ValueError("settle_seconds must be nonnegative")
    now = time.time() if now is None else now
    prior = published_keys(ledger)
    files = []
    sha_seen: dict[str, str] = {}
    found: dict[str, int] = {}
    for path in sorted(folder.iterdir(), key=lambda p: p.name.casefold()):
        if path.suffix.casefold() != ".mp4" or not path.is_file() or path.is_symlink():
            continue
        name = path.name
        entry: dict[str, Any] = {"file": name, "status": "HOLD", "reasons": []}
        stat_before = path.stat()
        entry["bytes"] = stat_before.st_size
        mapping, reasons = assignment_for(name, assignments)
        entry["mapping"] = mapping
        entry["reasons"].extend(reasons)
        if stat_before.st_size > MAX_BYTES or stat_before.st_size <= 0:
            entry["reasons"].append("INVALID_FILE_SIZE")
            files.append(entry)
            continue
        if now - stat_before.st_mtime < settle_seconds:
            entry["reasons"].append("WAIT_FOR_UPLOAD_TO_SETTLE")
            files.append(entry)
            continue
        try:
            info = inspect_mp4(path)
            entry["video"] = info
            entry["sha256"] = sha256_file(path)
            stat_after = path.stat()
            if stat_after.st_size != stat_before.st_size or stat_after.st_mtime_ns != stat_before.st_mtime_ns:
                entry["reasons"].append("FILE_CHANGED_DURING_SCAN")
            old = sha_seen.get(entry["sha256"])
            if old:
                entry["reasons"].append("DUPLICATE_MEDIA_SHA256:" + old)
            else:
                sha_seen[entry["sha256"]] = name
            if mapping and not reasons:
                key = (mapping["event_id"], mapping["bout_id"])
                found[mapping["event_id"]] = found.get(mapping["event_id"], 0) + 1
                if key in prior:
                    entry["reasons"].append("ALREADY_HAS_PUBLISHED_BOUT_CONTENT_REVIEW_REUSE")
                if mapping["kind"] == "full_bout" and info["height"] > info["width"]:
                    entry["reasons"].append("PORTRAIT_FULL_BOUT_REQUIRES_FRAMING_REVIEW")
                if mapping["kind"] != "full_bout" and info["width"] > info["height"]:
                    entry["reasons"].append("LANDSCAPE_BROLL_REQUIRES_VERTICAL_CROP_REVIEW")
            # Even a mechanically clean file is NOT approved for unattended publishing.
            entry["reasons"].append("INDEPENDENT_FILMING_AND_PUBLICATION_RIGHTS_CHECK_REQUIRED")
        except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
            entry["reasons"].append("MEDIA_READ_OR_PROBE_FAILED:" + type(exc).__name__)
        files.append(entry)
    return {
        "schema": "RKK_PRIVATE_VIDEO_INTAKE_V1",
        "publication_ready": False,
        "private_local_only": True,
        "file_count": len(files),
        "mapped_event_counts": found,
        "files": files,
        "notes": [
            "This is an offline inventory, not consent and not publication approval.",
            "Filenames, image appearance and uploader assertions never identify athletes automatically.",
            "Use a separate trusted rights/results gate and a channel-specific publication ledger.",
        ],
    }


def cli(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--folder", type=Path, required=True, help="private locally synced folder")
    p.add_argument("--assignments", type=Path, help="private human-verified filename -> event/bout map")
    p.add_argument("--published-ledger", type=Path, help="trusted record of previously published bouts")
    p.add_argument("--output", type=Path, required=True, help="private report.json path")
    p.add_argument("--settle-seconds", type=int, default=60)
    ns = p.parse_args(argv)
    report = inventory(ns.folder, read_json(ns.assignments), read_json(ns.published_ledger),
                       settle_seconds=ns.settle_seconds)
    ns.output.parent.mkdir(parents=True, exist_ok=True)
    ns.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"RKK intake: {report['file_count']} local MP4(s) inventoried, publication NOT triggered")
    print("Private report:", ns.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())

