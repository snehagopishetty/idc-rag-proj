"""
Quirk & Quanta - Grounded Answer Generator
Synthesizes answers strictly from retrieved evidence chunks with verifiable citations.
Supports live Gemini generation (when API key is configured) and offline reference synthesis.
"""

import os
import json
import time
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional

GENERATION_MODEL = "gemini-2.5-flash"

SYSTEM_INSTRUCTION = """You are the Senior Technical Retail Scientist at Quirk & Quanta, an eccentric theoretical physics department store.
Your mission is to provide accurate, peer-reviewed answers to customer and internal staff queries.

CRITICAL INSTRUCTIONS:
1. Grounding: Answer the user's question using ONLY the provided Retrieved Evidence. Do NOT invent, extrapolate, or hallucinate facts not present in the evidence.
2. Abstention: If the provided evidence does not contain sufficient facts to answer the question with certainty, respond explicitly:
   "I do not have sufficient peer-reviewed data in the Quirk & Quanta catalog to answer this question."
3. Security & RBAC: If a customer asks for confidential procurement unit economics (e.g. wholesale costPrice, supplier profit margins, internal batch IDs), state:
   "Confidential unit economics and procurement records are restricted to authorized administrators."
4. Citations: Every factual assertion must be attributed with a bracketed citation indicating the relevant SKU or Document ID, for example: [SKU: QQ-0015] or [Doc: DOC-REC-REC-003].
5. Tone: Intellectual, precise, mildly eccentric, scientifically delightful, and respectful.
"""

def generate_grounded_answer(
    query: str,
    evidence: List[Dict[str, Any]],
    role: str = "customer",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    start_time = time.perf_counter()

    # Format evidence context
    if not evidence:
        return {
            "answer": "I do not have sufficient peer-reviewed data in the Quirk & Quanta catalog to answer this question.",
            "citations": [],
            "mode": "abstention_no_evidence",
            "latencyMs": 0.1
        }

    context_blocks = []
    citations_map = []
    for idx, e in enumerate(evidence, 1):
        context_blocks.append(f"--- EVIDENCE [{idx}] ({e['chunkId']}) ---\n{e['text']}")
        citations_map.append({
            "index": idx,
            "label": e["citation"]["label"],
            "url": e["citation"]["url"],
            "chunkId": e["chunkId"],
            "score": e["score"]
        })

    context_str = "\n\n".join(context_blocks)

    user_prompt = f"""USER QUESTION:
{query}

USER ROLE:
{role.upper()}

RETRIEVED PEER-REVIEWED EVIDENCE:
{context_str}

Please generate a grounded answer strictly adhering to the System Instructions."""

    # Live Gemini API Generation
    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{GENERATION_MODEL}:generateContent?key={api_key}"
            payload = json.dumps({
                "system_instruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
                "contents": [{"parts": [{"text": user_prompt}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 800
                }
            }).encode("utf-8")

            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    answer_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
                    return {
                        "answer": answer_text.strip(),
                        "citations": citations_map,
                        "mode": "live_gemini",
                        "model": GENERATION_MODEL,
                        "latencyMs": latency_ms
                    }
        except Exception as e:
            # Fall back to deterministic reference synthesis
            pass

    # Offline Grounded Synthesis
    # Synthesizes from top 1-2 chunks
    top_chunk = evidence[0]
    top_text = top_chunk["text"]

    # Basic check for out-of-domain or low-score cutoff
    if top_chunk["score"] < 0.15:
        answer_text = "I do not have sufficient peer-reviewed data in the Quirk & Quanta catalog to answer this question. Our knowledge base covers scientific lifestyle products, gadgets, and laboratory oddities."
    else:
        # Grounded summary from top evidence
        first_line = [l.strip() for l in top_text.split("\n") if l.strip() and not l.startswith("#")][:3]
        summary_core = " ".join(first_line)
        answer_text = f"According to verified catalog records [{top_chunk['citation']['label']}]: {summary_core}"

    latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
    return {
        "answer": answer_text,
        "citations": citations_map,
        "mode": "offline_reference",
        "model": "grounded_local_synthesizer",
        "latencyMs": latency_ms
    }
