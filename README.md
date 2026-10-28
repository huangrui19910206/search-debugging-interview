# Search Service — Debugging Exercise

A compact, in-memory **search retrieval service**: an inverted index with
**BM25** ranking and a small add / remove / search API. The implementation is
complete and runnable, but it contains a handful of **bugs**. Your job is to
find and fix them so the full test suite passes.

You have roughly **45–60 minutes**. Think out loud, use the tests to guide you,
and fix the bugs in whatever order you like.

## Setup (under 2 minutes)

Requires Python 3.11+.

```bash
# from the repo root
python -m venv .venv && source .venv/bin/activate
pip install pytest
python -m pytest -v
```

(or with `uv`: `uv venv && uv pip install pytest && uv run pytest -v`)

You should see the **baseline tests pass** and **four `test_level_*` tests fail**.
Those four failures are the exercise.

## What the service is supposed to do

```python
from search_service import SearchService

svc = SearchService()
svc.add_document("d1", "the quick brown fox")
svc.add_document("d2", "a fast brown fox")

results = svc.search("Brown Fox", top_k=5)
# -> [SearchResult(doc_id=..., score=..., text=...), ...] sorted by descending score

svc.remove_document("d1")   # d1 should no longer appear in any results
```

Intended behavior:

- **Tokenization** is case-insensitive and ignores punctuation; a query matches
  the indexed text regardless of case.
- **Term frequency** reflects how many times a term actually occurs in a document.
- **Ranking** uses BM25, including proper document-length normalization
  (shorter documents are not unfairly penalized or rewarded).
- **Removal** fully deletes a document — it must not resurface in later searches.

## API surface

| Method | Description |
|---|---|
| `SearchService.add_document(doc_id, text)` | Index a document. |
| `SearchService.remove_document(doc_id)` | Remove a document from the index and store. |
| `SearchService.search(query, top_k=10)` | Return up to `top_k` `SearchResult`s, best first. |
| `InvertedIndex.term_frequency(term, doc_id)` | Occurrences of `term` in a document. |
| `InvertedIndex.document_frequency(term)` | Number of documents containing `term`. |

## Layout

```
src/search_service/
  tokenizer.py   # text -> normalized tokens
  index.py       # inverted index + corpus statistics
  service.py     # add/remove/search + BM25 scoring
tests/
  test_search.py # baseline tests + test_level_1..4 (the bugs)
sample_data/
  corpus.json    # a tiny example corpus
```

## The task

1. Run the tests and read the four failing `test_level_*` cases.
2. Form a hypothesis, locate the defect, and fix it.
3. Re-run the tests until everything is green.

Good luck — we care as much about **how** you debug as about finishing all four.
