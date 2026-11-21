"""
Quirk & Quanta - Pure-Python BM25 Lexical Retriever
Standard library implementation of Okapi BM25 with tokenization that preserves
scientific product SKUs (e.g. QQ-0018), component IDs (e.g. COMP-012),
and recall identifiers (e.g. REC-003).
"""

import os
import re
import math
import json
import time
from typing import List, Dict, Any, Optional

DEFAULT_K1 = 1.5
DEFAULT_B = 0.75

STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
    "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
    "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}

def tokenize(text: str) -> List[str]:
    """
    Tokenizes text while strictly preserving identifiers like QQ-0018,
    COMP-012, REC-003, and technical terms.
    """
    if not text:
        return []
    # Match words or hyphenated identifiers like QQ-0018, COMP-012, BATCH-2026-A
    raw_tokens = re.findall(r'[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*', text.lower())
    tokens = []
    for token in raw_tokens:
        # Keep identifiers even if short, filter standard stopwords
        if '-' in token or token.startswith('qq') or token.startswith('comp') or token.startswith('rec') or token.startswith('sup'):
            tokens.append(token)
        elif token not in STOPWORDS and len(token) > 1:
            tokens.append(token)
    return tokens

class BM25Retriever:
    def __init__(self, k1: float = DEFAULT_K1, b: float = DEFAULT_B):
        self.k1 = k1
        self.b = b
        self.chunks: List[Dict[str, Any]] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_count: int = 0
        self.inverted_index: Dict[str, Dict[int, int]] = {}
        self.idf: Dict[str, float] = {}
        self._strategy_loaded: Optional[str] = None

    def build_index(self, chunks: List[Dict[str, Any]], strategy_name: str = "semantic"):
        """
        Builds the BM25 inverted index and precomputes IDF and document statistics.
        """
        self.chunks = chunks
        self.doc_count = len(chunks)
        self.doc_lengths = []
        self.inverted_index = {}
        self.idf = {}
        self._strategy_loaded = strategy_name

        total_tokens = 0
        doc_freq: Dict[str, int] = {}

        for doc_idx, chunk in enumerate(chunks):
            # Include text, title, and metadata keywords for complete lexical recall
            text_to_index = f"{chunk.get('sectionTitle', '')} {chunk.get('text', '')}"
            meta = chunk.get("metadata", {})
            if "sku" in meta:
                text_to_index += f" {meta['sku']}"
            if "sourceId" in chunk:
                text_to_index += f" {chunk['sourceId']}"

            tokens = tokenize(text_to_index)
            length = len(tokens)
            self.doc_lengths.append(length)
            total_tokens += length

            term_counts: Dict[str, int] = {}
            for t in tokens:
                term_counts[t] = term_counts.get(t, 0) + 1

            for t, count in term_counts.items():
                if t not in self.inverted_index:
                    self.inverted_index[t] = {}
                self.inverted_index[t][doc_idx] = count
                doc_freq[t] = doc_freq.get(t, 0) + 1

        self.avg_doc_len = (total_tokens / self.doc_count) if self.doc_count > 0 else 1.0

        # Precompute Robertson-Spärck Jones IDF with smoothing
        for term, df in doc_freq.items():
            self.idf[term] = math.log(1.0 + (self.doc_count - df + 0.5) / (df + 0.5))

    def search(
        self,
        query: str,
        top_k: int = 5,
        role: str = "customer"
    ) -> List[Dict[str, Any]]:
        """
        Scores all matching documents using BM25 and returns the top-k results
        filtered by role access.
        """
        query_tokens = tokenize(query)
        if not query_tokens or self.doc_count == 0:
            return []

        # Find candidate documents containing at least one query term
        scores: Dict[int, float] = {}
        matched_terms_per_doc: Dict[int, List[str]] = {}

        for term in query_tokens:
            if term not in self.inverted_index:
                continue
            idf_val = self.idf.get(term, 0.0)
            postings = self.inverted_index[term]

            for doc_idx, tf in postings.items():
                doc_len = self.doc_lengths[doc_idx]
                denom = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / self.avg_doc_len))
                term_score = idf_val * (tf * (self.k1 + 1.0)) / denom

                scores[doc_idx] = scores.get(doc_idx, 0.0) + term_score
                if doc_idx not in matched_terms_per_doc:
                    matched_terms_per_doc[doc_idx] = []
                matched_terms_per_doc[doc_idx].append(term)

        # RBAC Filtering
        filtered_results = []
        for doc_idx, score in scores.items():
            chunk = self.chunks[doc_idx]
            access = chunk.get("accessLevel", "public")
            allowed_roles = chunk.get("allowedRoles", ["customer", "admin", "procurement"])

            if role.lower() in ["admin", "presenter"]:
                pass  # Admin and presenter roles have full catalog inspection privileges
            else:
                if role.lower() == "customer" and access != "public":
                    continue
                if role.lower() not in [r.lower() for r in allowed_roles]:
                    continue

            filtered_results.append((doc_idx, score))

        # Sort descending by BM25 score
        filtered_results.sort(key=lambda x: x[1], reverse=True)
        top_slice = filtered_results[:top_k]

        output = []
        for rank, (doc_idx, score) in enumerate(top_slice, 1):
            chunk = self.chunks[doc_idx]
            meta = chunk.get("metadata", {})
            citation_info = meta.get("citation", {})

            output.append({
                "rank": rank,
                "score": round(score, 4),
                "bm25Score": round(score, 4),
                "chunkId": chunk["chunkId"],
                "docId": chunk["docId"],
                "sourceId": chunk["sourceId"],
                "accessLevel": chunk.get("accessLevel", "public"),
                "matchedTerms": matched_terms_per_doc.get(doc_idx, []),
                "sectionTitle": chunk.get("sectionTitle", meta.get("section", "General")),
                "text": chunk.get("text", ""),
                "citation": {
                    "label": citation_info.get("label", f"Document {chunk.get('sourceId', '')}"),
                    "url": citation_info.get("url", "#"),
                    "sectionName": citation_info.get("sectionName", "Catalog Dossier")
                }
            })

        return output
