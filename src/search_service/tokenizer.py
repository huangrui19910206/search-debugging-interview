"""Text tokenization shared by indexing and (ideally) querying."""

from __future__ import annotations

import re

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    """Normalize ``text`` to a list of lowercase alphanumeric tokens.

    Punctuation is dropped and everything is lowercased so that indexing and
    retrieval operate on the same vocabulary.
    """
    return _TOKEN_RE.findall(text.lower())
