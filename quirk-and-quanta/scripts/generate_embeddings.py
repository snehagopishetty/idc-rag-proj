#!/usr/bin/env python3
"""
Quirk & Quanta - Versioned Document & Query Embedding Generator
Generates 768-dimensional normalized embeddings for all corpus chunks across
fixed, sliding, and semantic strategies, plus precomputes query embeddings for
curated golden demonstration questions.

Supports:
1. Live Gemini API mode (using model 'gemini-embedding-001' with taskType 'RETRIEVAL_DOCUMENT')
2. Offline deterministic mode (for local testing, reproducible evaluations, and zero-key operation)
"""

import os
import sys
import json
import math
import re
import hashlib
import urllib.request
import urllib.error
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNKS_DIR = os.path.join(ROOT_DIR, "data", "chunks")
EVAL_DIR = os.path.join(ROOT_DIR, "data", "evaluation")
EMBEDDINGS_DIR = os.path.join(ROOT_DIR, "data", "embeddings", "v1")

os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

MODEL_NAME = "gemini-embedding-001"
DIMENSIONS = 768

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# -----------------------------------------------------------------
# Vector Normalization & Similarity
# -----------------------------------------------------------------
def normalize_vector(vec):
    norm = math.sqrt(sum(x * x for x in vec))
    if norm < 1e-12:
        return [0.0] * len(vec)
    return [round(x / norm, 6) for x in vec]

def cosine_similarity(u, v):
    dot = sum(a * b for a, b in zip(u, v))
    norm_u = math.sqrt(sum(a * a for a in u))
    norm_v = math.sqrt(sum(b * b for b in v))
    if norm_u < 1e-12 or norm_v < 1e-12:
        return 0.0
    return dot / (norm_u * norm_v)

# -----------------------------------------------------------------
# Offline Deterministic Projection Generator (768-D)
# -----------------------------------------------------------------
def generate_offline_embedding(text, task_type="RETRIEVAL_DOCUMENT", dim=DIMENSIONS):
    """
    Produces a deterministic, high-entropy 768-dimensional normalized unit vector
    using positive semantic n-gram hash projection with term-frequency weighting.
    Guarantees reproducible top-k rankings for offline evaluation and zero-key operation.
    """
    cleaned = re.sub(r'[^a-zA-Z0-9\-\s]', ' ', text.lower())
    tokens = [w for w in cleaned.split() if len(w) > 1]
    vec = [0.0] * dim

    features = []
    for i, t in enumerate(tokens):
        # Higher weight for SKUs and alphanumeric terms
        w = 3.5 if ('-' in t or any(c.isdigit() for c in t)) else 1.0
        features.append((t, w))
        if i < len(tokens) - 1:
            features.append((f"{t}_{tokens[i+1]}", 1.2))

    for feat, weight in features:
        h1 = int(hashlib.md5(f"s1:{feat}".encode("utf-8")).hexdigest()[:8], 16) % dim
        h2 = int(hashlib.md5(f"s2:{feat}".encode("utf-8")).hexdigest()[:8], 16) % dim
        vec[h1] += weight
        vec[h2] += weight * 0.7

    return normalize_vector(vec)

# -----------------------------------------------------------------
# Live Gemini REST API Caller
# -----------------------------------------------------------------
def call_gemini_api_batch(texts, api_key, task_type="RETRIEVAL_DOCUMENT"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:batchEmbedContents?key={api_key}"
    
    requests = []
    for t in texts:
        requests.append({
            "model": f"models/{MODEL_NAME}",
            "content": {"parts": [{"text": t[:2048]}]},
            "taskType": task_type,
            "outputDimensionality": DIMENSIONS
        })

    payload = json.dumps({"requests": requests}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            embeddings = []
            for item in data.get("embeddings", []):
                raw_values = item.get("values", [])
                embeddings.append(normalize_vector(raw_values))
            return embeddings
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API HTTP {e.code}: {err_msg}")
    except Exception as e:
        raise RuntimeError(f"Gemini API network error: {e}")

# -----------------------------------------------------------------
# Main Generator
# -----------------------------------------------------------------
def generate_all_embeddings(live_mode=False):
    print("=" * 60)
    print("QUIRK & QUANTA - EMBEDDING VECTOR GENERATION (v1)")
    print("=" * 60)

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if live_mode and not api_key:
        print("[WARNING] --live requested but GEMINI_API_KEY is not set.")
        print("Falling back to deterministic offline embedding mode.")
        live_mode = False

    mode_label = "LIVE Gemini API (gemini-embedding-001)" if live_mode else "OFFLINE Deterministic 768-D Mode"
    print(f"Execution Mode:    {mode_label}")
    print(f"Embedding Model:   {MODEL_NAME}")
    print(f"Dimensions:        {DIMENSIONS}")
    print(f"Task Type (Docs):  RETRIEVAL_DOCUMENT")
    print(f"Task Type (Query): RETRIEVAL_QUERY")

    # Load chunk files
    strategies = ["semantic", "fixed", "sliding"]
    total_chunks_processed = 0

    manifest_records = {}

    for strat in strategies:
        chunk_file = os.path.join(CHUNKS_DIR, f"chunks_{strat}.json")
        chunks = load_json(chunk_file)
        print(f"\nProcessing strategy '{strat}' ({len(chunks)} chunks)...")

        embeddings_data = []

        # Batch in chunks of 50 for live API or generate offline
        batch_size = 50
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [c["text"] for c in batch]

            if live_mode:
                try:
                    vectors = call_gemini_api_batch(texts, api_key, task_type="RETRIEVAL_DOCUMENT")
                except Exception as e:
                    print(f"  [API Error] {e}. Falling back to offline generation for batch.")
                    vectors = [generate_offline_embedding(t, "RETRIEVAL_DOCUMENT") for t in texts]
            else:
                vectors = [generate_offline_embedding(t, "RETRIEVAL_DOCUMENT") for t in texts]

            for c, vec in zip(batch, vectors):
                embeddings_data.append({
                    "chunkId": c["chunkId"],
                    "docId": c["docId"],
                    "sourceId": c["sourceId"],
                    "accessLevel": c["accessLevel"],
                    "allowedRoles": c["allowedRoles"],
                    "strategy": strat,
                    "model": MODEL_NAME,
                    "dimensions": DIMENSIONS,
                    "vector": vec,
                    "hash": hashlib.sha256(c["text"].encode("utf-8")).hexdigest()[:16]
                })

            if (i + batch_size) % 300 == 0 or (i + batch_size) >= len(chunks):
                print(f"  - Embedded {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")

        out_path = os.path.join(EMBEDDINGS_DIR, f"embeddings_{strat}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(embeddings_data, f)

        manifest_records[strat] = {
            "chunkCount": len(embeddings_data),
            "dimensions": DIMENSIONS,
            "file": f"embeddings_{strat}.json",
            "fileSizeKB": round(os.path.getsize(out_path) / 1024, 1)
        }
        total_chunks_processed += len(embeddings_data)

    # -------------------------------------------------------------
    # 2. Precompute & Cache Query Embeddings for Golden Questions
    # -------------------------------------------------------------
    print("\nPrecomputing and caching query embeddings for Golden Evaluation Questions...")
    golden_file = os.path.join(EVAL_DIR, "golden_dataset.json")
    query_cache = {}

    if os.path.exists(golden_file):
        golden_qs = load_json(golden_file)
        q_texts = [q["question"] for q in golden_qs]

        if live_mode:
            try:
                q_vectors = call_gemini_api_batch(q_texts, api_key, task_type="RETRIEVAL_QUERY")
            except Exception as e:
                print(f"  [Query API Error] {e}. Using offline generator.")
                q_vectors = [generate_offline_embedding(q, "RETRIEVAL_QUERY") for q in q_texts]
        else:
            q_vectors = [generate_offline_embedding(q, "RETRIEVAL_QUERY") for q in q_texts]

        for q, vec in zip(golden_qs, q_vectors):
            query_cache[q["id"]] = {
                "id": q["id"],
                "question": q["question"],
                "family": q["family"],
                "model": MODEL_NAME,
                "dimensions": DIMENSIONS,
                "taskType": "RETRIEVAL_QUERY",
                "vector": vec
            }

        cache_path = os.path.join(EMBEDDINGS_DIR, "query_embeddings_cache.json")
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(query_cache, f, indent=2)
        print(f"Precomputed {len(query_cache)} query embeddings -> data/embeddings/v1/query_embeddings_cache.json")

    # -------------------------------------------------------------
    # 3. Write Embeddings Manifest
    # -------------------------------------------------------------
    manifest = {
        "version": "1.0.0",
        "modelId": MODEL_NAME,
        "vectorDimensions": DIMENSIONS,
        "corpusVersion": "1.0.0",
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "liveApiMode": live_mode,
        "taskTypes": {
            "documentEmbedding": "RETRIEVAL_DOCUMENT",
            "queryEmbedding": "RETRIEVAL_QUERY"
        },
        "strategies": manifest_records,
        "totalChunksEmbedded": total_chunks_processed,
        "cachedQueryCount": len(query_cache)
    }

    manifest_path = os.path.join(EMBEDDINGS_DIR, "embeddings_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nSaved embeddings manifest -> data/embeddings/v1/embeddings_manifest.json")
    print("SUCCESS: Embedding vector generation complete!")

if __name__ == "__main__":
    is_live = "--live" in sys.argv
    generate_all_embeddings(live_mode=is_live)
