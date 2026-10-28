"""An in-memory inverted index with the corpus statistics BM25 needs."""

from __future__ import annotations

from collections import defaultdict


class InvertedIndex:
    """Maps terms to the documents that contain them, with term frequencies.

    Also tracks per-document length and corpus-level statistics (number of
    documents and total length) so a ranker can compute average document length.
    """

    def __init__(self) -> None:
        self.postings: dict[str, dict[str, int]] = defaultdict(dict)  # term -> {doc_id: term_freq}
        self.doc_len: dict[str, int] = {}                            # doc_id -> number of tokens
        self.doc_terms: dict[str, set[str]] = {}                     # doc_id -> set of its terms
        self.total_len: int = 0
        self.N: int = 0

    def add(self, doc_id: str, tokens: list[str]) -> None:
        """Index ``tokens`` under ``doc_id`` (re-indexing replaces the old copy)."""
        if doc_id in self.doc_len:
            self.remove(doc_id)
        for term in set(tokens):
            self.postings[term][doc_id] = 1
        self.doc_terms[doc_id] = set(tokens)
        self.doc_len[doc_id] = len(tokens)
        self.total_len += len(tokens)
        self.N += 1

    def remove(self, doc_id: str) -> None:
        """Remove ``doc_id`` from the index."""
        if doc_id not in self.doc_len:
            return
        self.N -= 1
        self.total_len -= self.doc_len[doc_id]

    def term_frequency(self, term: str, doc_id: str) -> int:
        """How many times ``term`` occurs in ``doc_id`` (0 if absent)."""
        return self.postings.get(term, {}).get(doc_id, 0)

    def document_frequency(self, term: str) -> int:
        """In how many documents ``term`` appears."""
        return len(self.postings.get(term, {}))

    @property
    def avgdl(self) -> float:
        """Average document length across the corpus."""
        return self.total_len / self.N if self.N else 0.0
