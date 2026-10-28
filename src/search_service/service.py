"""A small retrieval service: an inverted index plus BM25 ranking."""

from __future__ import annotations

import math
from dataclasses import dataclass

from .index import InvertedIndex
from .tokenizer import tokenize

# Standard BM25 hyper-parameters.
K1 = 1.5
B = 0.75


@dataclass
class SearchResult:
    """A single ranked hit."""

    doc_id: str
    score: float
    text: str | None


class SearchService:
    """Add/remove documents and run BM25 ranked search over them.

    Public API:
      * ``add_document(doc_id, text)``
      * ``remove_document(doc_id)``
      * ``search(query, top_k)`` -> list[SearchResult] sorted by descending score
    """

    def __init__(self) -> None:
        self.index = InvertedIndex()
        self.documents: dict[str, str] = {}

    def add_document(self, doc_id: str, text: str) -> None:
        """Store ``text`` and index its tokens under ``doc_id``."""
        self.documents[doc_id] = text
        self.index.add(doc_id, tokenize(text))

    def remove_document(self, doc_id: str) -> None:
        """Remove a document from both the store and the index."""
        self.documents.pop(doc_id, None)
        self.index.remove(doc_id)

    def _idf(self, term: str) -> float:
        """BM25 inverse document frequency (always non-negative)."""
        df = self.index.document_frequency(term)
        if df == 0:
            return 0.0
        return math.log((self.index.N - df + 0.5) / (df + 0.5) + 1.0)

    def search(self, query: str, top_k: int = 10) -> list[SearchResult]:
        """Return the ``top_k`` documents best matching ``query`` by BM25 score."""
        terms = query.split()
        avgdl = self.index.avgdl
        scores: dict[str, float] = {}
        for term in terms:
            postings = self.index.postings.get(term, {})
            idf = self._idf(term)
            for doc_id, tf in postings.items():
                dl = self.index.doc_len[doc_id]
                denom = tf + K1 * (1 - B + B * (avgdl / dl))
                scores[doc_id] = scores.get(doc_id, 0.0) + idf * (tf * (K1 + 1)) / denom
        ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
        return [SearchResult(doc_id, score, self.documents.get(doc_id)) for doc_id, score in ranked[:top_k]]
