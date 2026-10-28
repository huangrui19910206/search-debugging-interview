"""A compact search-retrieval service: inverted index + BM25 ranking."""

from .index import InvertedIndex
from .service import SearchResult, SearchService
from .tokenizer import tokenize

__all__ = ["InvertedIndex", "SearchService", "SearchResult", "tokenize"]
