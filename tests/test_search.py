"""Tests for the search service.

Baseline tests describe the normal, correct behavior and should always pass.
The four ``test_level_N_*`` tests each target one defect in the implementation and
can be fixed independently, in any order.
"""

from search_service import SearchService, tokenize

# --------------------------------------------------------------------------- #
# Baseline tests (these should pass out of the box)
# --------------------------------------------------------------------------- #


def test_tokenizer_normalizes():
    assert tokenize("Hello, World!") == ["hello", "world"]
    assert tokenize("BM25 ranking, v2.0") == ["bm25", "ranking", "v2", "0"]


def test_add_and_search_finds_document():
    svc = SearchService()
    svc.add_document("d1", "the quick brown fox")
    results = svc.search("quick")
    assert [r.doc_id for r in results] == ["d1"]
    assert results[0].text == "the quick brown fox"


def test_search_respects_top_k():
    svc = SearchService()
    for i in range(5):
        svc.add_document(f"d{i}", f"common topic number {i}")
    assert len(svc.search("common", top_k=3)) == 3


def test_search_no_match_returns_empty():
    svc = SearchService()
    svc.add_document("d1", "alpha beta")
    assert svc.search("nonexistentterm") == []


def test_search_returns_all_matching_documents():
    svc = SearchService()
    svc.add_document("d1", "cats and dogs")
    svc.add_document("d2", "dogs and birds")
    svc.add_document("d3", "fish only")
    found = {r.doc_id for r in svc.search("dogs")}
    assert found == {"d1", "d2"}


# --------------------------------------------------------------------------- #
# Level tests (each fails until its bug is fixed; fixable in any order)
# --------------------------------------------------------------------------- #


def test_level_1_search_is_case_insensitive():
    """A query should match regardless of case, like the indexed text."""
    svc = SearchService()
    svc.add_document("d1", "Python tutorial for beginners")
    results = svc.search("PYTHON")
    assert [r.doc_id for r in results] == ["d1"]


def test_level_2_term_frequency_counts_duplicates():
    """Repeated terms must be counted, not merely recorded as present."""
    svc = SearchService()
    svc.add_document("d1", "spam spam spam eggs")
    assert svc.index.term_frequency("spam", "d1") == 3
    assert svc.index.term_frequency("eggs", "d1") == 1


def test_level_3_bm25_prefers_shorter_document():
    """With equal term frequency, BM25 length normalization favors the shorter doc."""
    svc = SearchService()
    svc.add_document("short", "machine learning")
    filler = " ".join(f"topic{i}" for i in range(30))
    svc.add_document("long", "learning " + filler)
    results = svc.search("learning")
    assert results[0].doc_id == "short"


def test_level_4_removed_document_disappears():
    """After removal a document must not surface via any of its former terms."""
    svc = SearchService()
    svc.add_document("d1", "alpha beta gamma")
    svc.add_document("d2", "delta zebra epsilon")
    svc.add_document("d3", "eta theta iota")
    svc.remove_document("d2")
    assert svc.search("zebra") == []
    assert all(r.doc_id != "d2" for r in svc.search("delta"))
