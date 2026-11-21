#!/usr/bin/env python3
"""
Quirk & Quanta - Multi-Strategy Chunking Engine
Implements three distinct chunking strategies with deterministic IDs:
1. Fixed-size chunking (configurable size, word-boundary preserved)
2. Sliding-window chunking (configurable size & overlap, word-boundary preserved)
3. Structural / Semantic chunking (Markdown heading & domain section aware)

Outputs versioned chunk datasets for public and internal corpora,
along with comparison telemetry for the workshop lab dashboard.
"""

import os
import sys
import json
import re
import hashlib

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_DIR = os.path.join(ROOT_DIR, "data", "corpus")
CHUNKS_DIR = os.path.join(ROOT_DIR, "data", "chunks")

os.makedirs(CHUNKS_DIR, exist_ok=True)

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text[:30] if text else "section"

# -----------------------------------------------------------------
# 1. Fixed-Size Chunking (Word-boundary aware, zero overlap)
# -----------------------------------------------------------------
def chunk_fixed(text, doc_id, chunk_size=450):
    words = text.split()
    chunks = []
    current_words = []
    current_len = 0

    for word in words:
        # +1 for space
        if current_len + len(word) + 1 > chunk_size and current_words:
            chunk_text = " ".join(current_words)
            chunks.append(chunk_text)
            current_words = [word]
            current_len = len(word)
        else:
            current_words.append(word)
            current_len += len(word) + 1

    if current_words:
        chunks.append(" ".join(current_words))

    result = []
    for idx, c_text in enumerate(chunks, 1):
        result.append({
            "chunkId": f"CHK-{doc_id}-FIX-{idx:03d}",
            "strategy": "fixed",
            "index": idx,
            "totalChunks": len(chunks),
            "charLength": len(c_text),
            "wordCount": len(c_text.split()),
            "text": c_text
        })
    return result

# -----------------------------------------------------------------
# 2. Sliding-Window Chunking (Word-boundary aware, with overlap)
# -----------------------------------------------------------------
def chunk_sliding(text, doc_id, chunk_size=450, overlap=150):
    words = text.split()
    chunks = []
    start_idx = 0
    total_words = len(words)

    # Estimate words per chunk and overlap
    avg_word_len = sum(len(w) for w in words) / max(len(words), 1) + 1
    words_per_chunk = max(int(chunk_size / avg_word_len), 10)
    overlap_words = max(int(overlap / avg_word_len), 3)
    step = max(words_per_chunk - overlap_words, 5)

    idx = 1
    while start_idx < total_words:
        end_idx = min(start_idx + words_per_chunk, total_words)
        chunk_words = words[start_idx:end_idx]
        chunk_text = " ".join(chunk_words)

        chunks.append({
            "chunkId": f"CHK-{doc_id}-SLD-{idx:03d}",
            "strategy": "sliding",
            "index": idx,
            "charLength": len(chunk_text),
            "wordCount": len(chunk_words),
            "text": chunk_text
        })
        idx += 1
        if end_idx >= total_words:
            break
        start_idx += step

    for c in chunks:
        c["totalChunks"] = len(chunks)

    return chunks

# -----------------------------------------------------------------
# 3. Structural / Semantic Chunking (Markdown & Heading Aware)
# -----------------------------------------------------------------
def chunk_semantic(text, doc_id, doc_title, doc_category):
    """
    Parses Markdown into cohesive semantic units.
    Splits by H1/H2 section headers and groups coherent subsections,
    adding contextual breadcrumb prefixes to each semantic chunk.
    """
    lines = text.split("\n")
    sections = []
    current_title = "Header Information"
    current_lines = []

    for line in lines:
        if line.startswith("## "):
            if current_lines:
                sec_text = "\n".join(current_lines).strip()
                if sec_text:
                    sections.append((current_title, sec_text))
            current_title = line.replace("## ", "").strip()
            current_lines = [line]
        elif line.startswith("# ") and not current_lines:
            current_lines.append(line)
        else:
            current_lines.append(line)

    if current_lines:
        sec_text = "\n".join(current_lines).strip()
        if sec_text:
            sections.append((current_title, sec_text))

    # If only 1 section found or no H2 headers, split by paragraphs
    if len(sections) <= 1:
        raw_paras = [p.strip() for p in text.split("\n\n") if p.strip()]
        sections = [(f"Paragraph {i+1}", p) for i, p in enumerate(raw_paras)]

    chunks = []
    for idx, (sec_name, sec_body) in enumerate(sections, 1):
        slug = slugify(sec_name)
        # Contextual prefix ensures top-level grounding
        prefixed_text = f"[{doc_title} | Section: {sec_name}]\n{sec_body}"
        
        chunks.append({
            "chunkId": f"CHK-{doc_id}-SEM-{slug}-{idx:02d}",
            "strategy": "semantic",
            "sectionTitle": sec_name,
            "index": idx,
            "totalChunks": len(sections),
            "charLength": len(prefixed_text),
            "wordCount": len(prefixed_text.split()),
            "text": prefixed_text
        })

    return chunks

# -----------------------------------------------------------------
# Master Chunking Pipeline
# -----------------------------------------------------------------
def process_corpus():
    print("=" * 60)
    print("EXECUTING MULTI-STRATEGY CHUNKING PIPELINE")
    print("=" * 60)

    public_docs = load_json(os.path.join(CORPUS_DIR, "corpus_public.json"))
    internal_docs = load_json(os.path.join(CORPUS_DIR, "corpus_internal.json"))
    all_docs = public_docs + internal_docs

    fixed_chunks = []
    sliding_chunks = []
    semantic_chunks = []

    for doc in all_docs:
        doc_id = doc["docId"]
        text = doc["content"]
        title = doc["title"]
        cat = doc["category"]
        access = doc["accessLevel"]
        roles = doc["allowedRoles"]
        meta = doc["metadata"]

        # 1. Fixed
        f_list = chunk_fixed(text, doc_id, chunk_size=450)
        for c in f_list:
            c.update({
                "docId": doc_id,
                "sourceId": doc["sourceId"],
                "sourceType": doc["sourceType"],
                "accessLevel": access,
                "allowedRoles": roles,
                "metadata": meta
            })
        fixed_chunks.extend(f_list)

        # 2. Sliding
        s_list = chunk_sliding(text, doc_id, chunk_size=450, overlap=150)
        for c in s_list:
            c.update({
                "docId": doc_id,
                "sourceId": doc["sourceId"],
                "sourceType": doc["sourceType"],
                "accessLevel": access,
                "allowedRoles": roles,
                "metadata": meta
            })
        sliding_chunks.extend(s_list)

        # 3. Semantic
        sem_list = chunk_semantic(text, doc_id, title, cat)
        for c in sem_list:
            c.update({
                "docId": doc_id,
                "sourceId": doc["sourceId"],
                "sourceType": doc["sourceType"],
                "accessLevel": access,
                "allowedRoles": roles,
                "metadata": meta
            })
        semantic_chunks.extend(sem_list)

    # Write separate JSON datasets
    with open(os.path.join(CHUNKS_DIR, "chunks_fixed.json"), "w", encoding="utf-8") as f:
        json.dump(fixed_chunks, f, indent=2)

    with open(os.path.join(CHUNKS_DIR, "chunks_sliding.json"), "w", encoding="utf-8") as f:
        json.dump(sliding_chunks, f, indent=2)

    with open(os.path.join(CHUNKS_DIR, "chunks_semantic.json"), "w", encoding="utf-8") as f:
        json.dump(semantic_chunks, f, indent=2)

    # Compute comparative telemetry
    def get_stats(chunk_list):
        lens = [c["charLength"] for c in chunk_list]
        w_lens = [c["wordCount"] for c in chunk_list]
        return {
            "totalChunks": len(chunk_list),
            "avgCharLength": round(sum(lens) / max(len(lens), 1), 1),
            "minCharLength": min(lens) if lens else 0,
            "maxCharLength": max(lens) if lens else 0,
            "avgWordCount": round(sum(w_lens) / max(len(w_lens), 1), 1),
            "publicChunks": sum(1 for c in chunk_list if c["accessLevel"] == "public"),
            "internalChunks": sum(1 for c in chunk_list if c["accessLevel"] != "public")
        }

    manifest = {
        "corpusVersion": "1.0.0",
        "totalSourceDocuments": len(all_docs),
        "strategies": {
            "fixed": {
                "config": {"chunkSize": 450, "overlap": 0, "boundary": "word"},
                "telemetry": get_stats(fixed_chunks)
            },
            "sliding": {
                "config": {"chunkSize": 450, "overlap": 150, "boundary": "word"},
                "telemetry": get_stats(sliding_chunks)
            },
            "semantic": {
                "config": {"splitRule": "markdown_h2_structural_sections", "contextualPrefix": True},
                "telemetry": get_stats(semantic_chunks)
            }
        }
    }

    with open(os.path.join(CHUNKS_DIR, "chunks_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated Fixed-Size Chunks:     {len(fixed_chunks):4d} chunks (avg {manifest['strategies']['fixed']['telemetry']['avgCharLength']} chars)")
    print(f"Generated Sliding-Window Chunks: {len(sliding_chunks):4d} chunks (avg {manifest['strategies']['sliding']['telemetry']['avgCharLength']} chars)")
    print(f"Generated Semantic Chunks:       {len(semantic_chunks):4d} chunks (avg {manifest['strategies']['semantic']['telemetry']['avgCharLength']} chars)")
    print("Chunks and comparative telemetry saved to data/chunks/")
    print("SUCCESS: Multi-strategy chunking completed.")

if __name__ == "__main__":
    process_corpus()
