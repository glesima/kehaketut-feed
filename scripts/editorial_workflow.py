"""RKK editorial draft model. This module does NOT authorize or publish posts.

Only a private backend may verify OIDC/WebAuthn identities, store the drafts,
send notifications and carry out publishing. Public GitHub contains no
credentials or contributor submissions.
"""
from __future__ import annotations

import hashlib
import json
import re
import secrets
from dataclasses import dataclass
from typing import Any

GROUPS = frozenset({"general", "competitive", "juniors", "fitness", "women"})
CHANNELS = frozenset({"website", "facebook", "instagram", "youtube", "tiktok", "x"})

@dataclass(frozen=True)
class Draft:
    id: str
    revision: int
    title: str
    body: str
    groups: tuple[str, ...]
    channels: tuple[str, ...]
    fingerprint: str
    state: str = "pending_review"
    publication_allowed: bool = False

def fingerprint(title: str, body: str, groups: tuple[str, ...],
                channels: tuple[str, ...], media_hashes: tuple[str, ...] = ()) -> str:
    data = {
        "title": title,
        "body": body,
        "groups": sorted(groups),
        "channels": sorted(channels),
        "media_hashes": sorted(media_hashes),
    }
    return hashlib.sha256(json.dumps(data, sort_keys=True,
                                      ensure_ascii=False).encode("utf-8")).hexdigest()

def prepare_draft(title: str, body: str,
                  groups: list[str] | tuple[str, ...],
                  channels: list[str] | tuple[str, ...] = ("website",),
                  media_hashes: tuple[str, ...] = ()) -> Draft:
    """Prepare a NON-PUBLISHABLE item after source/attachment safety checks.

    The caller must scan attachments, confirm permissions and run factual review.
    A spoofed email From header is never enough for approval rights.
    """
    title = (title or "").strip()
    body = (body or "").strip()
    if not title or not body:
        raise ValueError("A meaningful title and content are required")
    if len(title) > 160 or len(body) > 12000:
        raise ValueError("Content too large")
    if not groups:
        raise ValueError("Select a target group; do not invent one")
    normalized_groups = tuple(sorted(set(groups)))
    normalized_channels = tuple(sorted(set(channels)))
    if not set(normalized_groups).issubset(GROUPS):
        raise ValueError("Unknown target group")
    if not normalized_channels or not set(normalized_channels).issubset(CHANNELS):
        raise ValueError("Unknown publishing channel")
    if any(not re.fullmatch(r"[0-9a-f]{64}", x) for x in media_hashes):
        raise ValueError("Invalid media fingerprint")
    return Draft(
        id=secrets.token_hex(16),
        revision=1,
        title=title,
        body=body,
        groups=normalized_groups,
        channels=normalized_channels,
        fingerprint=fingerprint(title, body, normalized_groups,
                                normalized_channels, media_hashes),
    )

def revise_draft(draft: Draft, *, title: str | None = None,
                 body: str | None = None) -> Draft:
    """Any change invalidates previous approval; issue a new revision/hash."""
    current_title = draft.title if title is None else title
    current_body = draft.body if body is None else body
    replacement = prepare_draft(current_title, current_body,
                                list(draft.groups), list(draft.channels))
    return Draft(
        id=draft.id,
        revision=draft.revision + 1,
        title=replacement.title,
        body=replacement.body,
        groups=replacement.groups,
        channels=replacement.channels,
        fingerprint=replacement.fingerprint,
    )

def select_review_route(*, verified_personal_identity: bool,
                        is_named_reviewer: bool) -> str:
    """Only backend-verified identity may receive its own review queue.

    Never derive either boolean from an email's From address.
    """
    if verified_personal_identity and is_named_reviewer:
        return "verified_submitter_private_queue"
    return "club_reviewers_shared_queue"

def public_post_payload(draft: Draft) -> dict[str, Any]:
    """Deliberately refuse publication without a private authorization service."""
    raise PermissionError(
        "Publishing is disabled until a separate private OIDC/WebAuthn approval "
        "backend verifies reviewer, revision, digest and target channels."
    )
