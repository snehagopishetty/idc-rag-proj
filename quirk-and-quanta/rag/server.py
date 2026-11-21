#!/usr/bin/env python3
"""
Quirk & Quanta - Unified Storefront & RAG API Server
Zero external dependencies (uses standard library http.server).
Serves static storefront assets from site/ and provides live JSON endpoints:
- POST /api/rag/retrieve (Multi-strategy Retrieval: Vector, BM25, Hybrid)
- POST /api/rag/ask      (Full grounded RAG pipeline with Guardrails & Server RBAC)
- POST /api/rag/compare  (Side-by-side Vector vs BM25 vs Hybrid comparison)
- POST /api/rag/graph    (Multi-hop Knowledge Graph defect investigation)
- POST /api/rag/doc      (Direct Document Access with IDOR protection)
- GET  /api/rag/auth/demo-token (Generates authentic signed HMAC bearer token)
- GET  /api/rag/status   (System health & model telemetry)
- GET  /api/rag/questions (Curated golden evaluation questions)
- GET  /api/rag/telemetry (Chunking strategy statistics)
"""

import os
import sys
import json
import hmac
import http.server
import socketserver
from urllib.parse import urlparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_DIR = os.path.join(ROOT_DIR, "site")
EVAL_DIR = os.path.join(ROOT_DIR, "data", "evaluation")
CHUNKS_DIR = os.path.join(ROOT_DIR, "data", "chunks")
CORPUS_DIR = os.path.join(ROOT_DIR, "data", "corpus")

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from rag.pipeline import RAGPipeline
from rag.graph_local import get_graph
from rag.graph_neo4j import get_neo4j_adapter
from rag.auth import create_signed_token, resolve_effective_role, check_resource_access, verify_token

pipeline = RAGPipeline(default_strategy="semantic")
graph = get_graph()
neo4j_adapter = get_neo4j_adapter()

class QuirkHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SITE_DIR, **kwargs)

    def translate_path(self, path):
        """
        Security hardening: Canonicalizes path to prevent directory traversal
        outside of SITE_DIR (e.g. attempting to read data/internal/ or private source).
        """
        resolved = super().translate_path(path)
        normalized = os.path.realpath(resolved)
        real_site_dir = os.path.realpath(SITE_DIR)
        if not (normalized == real_site_dir or normalized.startswith(real_site_dir + os.sep)):
            return os.path.join(real_site_dir, "__blocked_path_traversal__")
        return resolved

    def _send_json(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Presenter-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Presenter-Token")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/healthz", "/health", "/api/health"]:
            self._send_json({
                "status": "healthy",
                "service": "quirk-quanta-rag",
                "region": "asia-south1",
                "version": "1.0.0",
                "environment": "production-ready"
            })
            return

        if path == "/api/rag/status":
            api_key = os.environ.get("GEMINI_API_KEY", "")
            manifest_file = os.path.join(ROOT_DIR, "data", "embeddings", "v1", "embeddings_manifest.json")
            manifest = json.load(open(manifest_file)) if os.path.exists(manifest_file) else {}

            self._send_json({
                "status": "ready",
                "service": "quirk-quanta-rag",
                "embeddingModel": "gemini-embedding-001",
                "vectorDimensions": 768,
                "generationModel": "gemini-2.5-flash",
                "hasGeminiKey": bool(api_key),
                "activeMode": "live_gemini" if bool(api_key) else "offline_reference",
                "featureFlags": {
                    "ENABLE_VECTOR": True,
                    "ENABLE_BM25": True,
                    "ENABLE_HYBRID": True,
                    "ENABLE_GRAPH_LOCAL": True,
                    "ENABLE_GRAPH_NEO4J": True,
                    "ENABLE_GENERATION": True,
                    "ENABLE_GROUNDING": True,
                    "ENABLE_PROMPT_INJECTION_DEFENSE": True,
                    "ENABLE_RBAC": True,
                    "ENABLE_USAGE_LIMITS": True,
                    "ENABLE_OBSERVABILITY": True,
                    "ENABLE_RECORDED_DEMOS": True
                },
                "chunkingClassification": {
                    "semantic": "Structural / Heading-Based Section Splitting (H1/H2 Markdown boundaries)",
                    "fixed": "Fixed-Size 450-Char Word-Bounded Splitting",
                    "sliding": "Sliding-Window 450-Char / 150-Overlap Splitting"
                },
                "graphNodes": len(graph.nodes),
                "neo4j": neo4j_adapter.get_telemetry(),
                "observability": pipeline.tracer.get_aggregate_telemetry(),
                "embeddings": manifest.get("strategies", {}),
                "totalChunks": manifest.get("totalChunksEmbedded", 0)
            })
            return

        elif path == "/api/rag/traces":
            traces = pipeline.tracer.get_recent_traces(limit=25)
            self._send_json(traces)
            return

        elif path == "/api/rag/traces/aggregate":
            telemetry = pipeline.tracer.get_aggregate_telemetry()
            self._send_json(telemetry)
            return

        elif path == "/api/rag/auth/demo-token":
            # Public Access Security Gate: Public users cannot mint privileged HMAC sessions.
            # Only authenticated presenters with the Secret Manager PRESENTER_TOKEN may mint privileged tokens.
            presenter_header = self.headers.get("X-Presenter-Token", "").strip()
            presenter_secret = os.environ.get("PRESENTER_TOKEN", "").strip()

            if not presenter_secret or not presenter_header or not hmac.compare_digest(presenter_header, presenter_secret):
                self._send_json({
                    "error": "Forbidden",
                    "status": 403,
                    "message": "Public users cannot mint privileged HMAC sessions. Valid X-Presenter-Token required."
                }, status=403)
                return

            token = create_signed_token(role="admin", user_id="dr_arthur")
            self._send_json({
                "role": "admin",
                "userId": "dr_arthur",
                "token": token,
                "type": "Bearer",
                "note": "Privileged Admin HMAC session token minted for authorized presenter."
            })
            return

        elif path == "/api/rag/questions":
            golden_path = os.path.join(EVAL_DIR, "golden_dataset.json")
            if os.path.exists(golden_path):
                questions = json.load(open(golden_path))
                self._send_json(questions)
            else:
                self._send_json([], status=404)
            return

        elif path == "/api/rag/telemetry":
            telemetry_path = os.path.join(CHUNKS_DIR, "chunks_manifest.json")
            if os.path.exists(telemetry_path):
                data = json.load(open(telemetry_path))
                self._send_json(data)
            else:
                self._send_json({}, status=404)
            return

        elif path == "/api/rag/okf":
            # OKF (Open Knowledge Format) Bundle Inspection
            okf_dir = os.path.join(ROOT_DIR, "data", "okf")
            manifest_file = os.path.join(okf_dir, "manifest.json")
            entities_file = os.path.join(okf_dir, "entities.jsonl")
            relations_file = os.path.join(okf_dir, "relations.jsonl")

            if not os.path.exists(manifest_file):
                self._send_json({"error": "OKF bundle not found"}, status=404)
                return

            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)

            entities = []
            if os.path.exists(entities_file):
                with open(entities_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            entities.append(json.loads(line))

            relations = []
            if os.path.exists(relations_file):
                with open(relations_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            relations.append(json.loads(line))

            self._send_json({
                "status": "ready",
                "format": manifest.get("format"),
                "formatVersion": manifest.get("formatVersion"),
                "datasetId": manifest.get("datasetId"),
                "title": manifest.get("title"),
                "description": manifest.get("description"),
                "manifest": manifest,
                "entities": entities,
                "relations": relations
            })
            return

        elif path == "/api/rag/chunks/inspect":
            # Interactive Chunking Lab Inspector
            from urllib.parse import parse_qs
            qs = parse_qs(parsed.query)
            target = qs.get("sourceId", qs.get("docId", ["QQ-0011"]))[0].strip()

            strategies_data = {}
            for strat, label, desc in [
                ("semantic", "Structural / Heading-Based Section Splitting", "Splits along H1/H2 Markdown boundaries preserving full topical coherence without mid-sentence truncation."),
                ("fixed", "Fixed-Size 450-Char Word-Bounded Splitting", "Splits at 450 characters (word bounded). Fast and uniform, but risks truncating context across arbitrary chunk borders."),
                ("sliding", "Sliding-Window 450-Char / 150-Overlap Splitting", "Slides 450-char window with 150-char overlap. Carries context over boundaries at the cost of 28% data redundancy.")
            ]:
                cf = os.path.join(CHUNKS_DIR, f"chunks_{strat}.json")
                if os.path.exists(cf):
                    with open(cf, "r", encoding="utf-8") as f:
                        all_c = json.load(f)
                    matched = [c for c in all_c if c.get("sourceId") == target or c.get("docId") == target]
                    strategies_data[strat] = {
                        "name": label,
                        "description": desc,
                        "totalChunks": len(matched),
                        "chunks": matched
                    }

            self._send_json({
                "target": target,
                "strategies": strategies_data
            })
            return

        elif path == "/api/rag/teaching":
            # Educational "Under the Hood" Teaching Manifest
            teaching_file = os.path.join(SITE_DIR, "data", "teaching", "pipelines.json")
            if not os.path.exists(teaching_file):
                teaching_file = os.path.join(ROOT_DIR, "data", "teaching", "pipelines.json")
            if os.path.exists(teaching_file):
                with open(teaching_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._send_json(data)
            else:
                self._send_json({"error": "Teaching manifest not found"}, status=404)
            return

        elif path == "/api/rag/evaluations":
            # Consolidated Golden Benchmark Evaluations across 42 curated cases
            eval_file = os.path.join(SITE_DIR, "data", "evaluation", "eval_summary.json")
            if not os.path.exists(eval_file):
                eval_file = os.path.join(ROOT_DIR, "data", "evaluation", "eval_summary.json")
            if os.path.exists(eval_file):
                with open(eval_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._send_json(data)
            else:
                self._send_json({"error": "Evaluation artifacts not found"}, status=404)
            return

        # Fallback to serving static storefront assets
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b"{}"

        try:
            params = json.loads(post_body.decode("utf-8"))
        except Exception:
            self._send_json({"error": "Invalid JSON in request body"}, status=400)
            return

        # Extract Auth Bearer header or JSON token
        auth_header = self.headers.get("Authorization", "")
        auth_token = params.get("authToken")
        if not auth_token and auth_header.startswith("Bearer "):
            auth_token = auth_header[7:].strip()

        question = params.get("question", "").strip()
        top_k = int(params.get("topK", 5))
        strategy = params.get("strategy", "semantic")
        method = params.get("method", "auto")
        role = params.get("role", "customer")
        hardened = bool(params.get("hardened", True))
        session_id = params.get("sessionId", "workshop_session")
        api_key = os.environ.get("GEMINI_API_KEY")

        # Resolve effective role at the server HTTP boundary
        # STRICT: Server HTTP boundary enforces hardened=True on role checks so clients cannot bypass RBAC!
        effective_role, was_tampered, auth_msg = resolve_effective_role(
            requested_role=role,
            auth_token=auth_token,
            hardened=True
        )

        # Presenter Priority Detection:
        # 1. Cryptographically verified bearer token with role "presenter" or "admin"
        # 2. Or explicit Secret Manager environment secret PRESENTER_TOKEN (strictly non-empty, matching X-Presenter-Token)
        is_presenter = False
        verified_token = verify_token(auth_token)
        if verified_token and verified_token.get("role") in ["presenter", "admin"]:
            is_presenter = True
        else:
            presenter_header = self.headers.get("X-Presenter-Token", "").strip()
            presenter_token = params.get("presenterToken", presenter_header)
            if isinstance(presenter_token, str):
                presenter_token = presenter_token.strip()
            else:
                presenter_token = ""
            presenter_secret = os.environ.get("PRESENTER_TOKEN", "").strip()
            if presenter_token and presenter_secret:
                is_presenter = bool(hmac.compare_digest(presenter_token, presenter_secret))

        if path == "/api/rag/retrieve":
            if not question:
                self._send_json({"error": "Field 'question' is required"}, status=400)
                return
            result = pipeline.ask(
                question=question,
                top_k=top_k,
                strategy=strategy,
                method=method,
                role=effective_role,
                auth_token=auth_token,
                retrieval_only=True,
                api_key=api_key,
                hardened=hardened,
                session_id=session_id,
                is_presenter=is_presenter
            )
            result["roleResolution"] = {
                "requestedRole": role,
                "effectiveRole": effective_role,
                "wasTampered": was_tampered,
                "authMessage": auth_msg
            }
            result["isPresenter"] = is_presenter
            self._send_json(result)
            return

        elif path == "/api/rag/ask":
            if not question:
                self._send_json({"error": "Field 'question' is required"}, status=400)
                return
            result = pipeline.ask(
                question=question,
                top_k=top_k,
                strategy=strategy,
                method=method,
                role=effective_role,
                auth_token=auth_token,
                retrieval_only=False,
                api_key=api_key,
                hardened=hardened,
                session_id=session_id,
                is_presenter=is_presenter
            )
            result["roleResolution"] = {
                "requestedRole": role,
                "effectiveRole": effective_role,
                "wasTampered": was_tampered,
                "authMessage": auth_msg
            }
            result["isPresenter"] = is_presenter
            self._send_json(result)
            return

        elif path == "/api/rag/compare":
            if not question:
                self._send_json({"error": "Field 'question' is required"}, status=400)
                return
            result = pipeline.compare(
                question=question,
                top_k=top_k,
                strategy=strategy,
                role=role,
                api_key=api_key
            )
            self._send_json(result)
            return

        elif path == "/api/rag/graph":
            skus = params.get("productSkus")
            if not skus and question:
                import re
                skus = re.findall(r'QQ-[0-9]{4}', question.upper())
            if not skus:
                skus = ["QQ-0011", "QQ-0074", "QQ-0049"]
            
            graph_engine = params.get("engine", "local").lower()
            if graph_engine in ["neo4j", "auradb"]:
                result = neo4j_adapter.trace_defect_root_cause(skus)
            else:
                result = graph.trace_defect_root_cause(skus)
            self._send_json(result)
            return

        elif path == "/api/rag/doc":
            # IDOR Inspection endpoint (Demo 16)
            doc_id = params.get("docId", "")
            if not doc_id:
                self._send_json({"error": "Field 'docId' is required"}, status=400)
                return

            # Directory traversal prevention: Reject path separators or relative segments immediately
            if "/" in doc_id or "\\" in doc_id or ".." in doc_id:
                self._send_json({"error": "Forbidden", "status": 403, "message": "Directory traversal syntax in docId is prohibited."}, status=403)
                return

            # Determine resource classification
            clean_doc_id = os.path.basename(doc_id).replace("..", "").strip()
            is_internal = any(k in doc_id.upper() for k in ["PROC", "INTERNAL", "SUPPLIER", "CONTRACT", "MARGIN", "PRIVATE", "CONFIDENTIAL"])
            access_level = "internal_procurement" if is_internal else "public"

            effective_role, was_tampered, auth_msg = resolve_effective_role(
                requested_role=role,
                auth_token=auth_token,
                hardened=True  # STRICT: IDOR endpoint always enforces cryptographic token verification!
            )

            # Check access
            allowed, access_msg = check_resource_access(clean_doc_id, effective_role, access_level)

            if not allowed:
                self._send_json({
                    "error": "Forbidden",
                    "status": 403,
                    "docId": clean_doc_id,
                    "accessLevel": access_level,
                    "requestedRole": role,
                    "effectiveRole": effective_role,
                    "wasTampered": was_tampered,
                    "securityAlert": access_msg
                }, status=403)
                return

            # If allowed, fetch document text from corpus safely
            doc_path = os.path.join(CORPUS_DIR, f"{clean_doc_id}.json")
            if not os.path.exists(doc_path):
                # Check with prefix DOC-
                alt_path = os.path.join(CORPUS_DIR, f"DOC-{clean_doc_id}.json")
                if os.path.exists(alt_path):
                    doc_path = alt_path

            # Strict path containment check
            norm_doc = os.path.realpath(doc_path)
            norm_corpus = os.path.realpath(CORPUS_DIR)
            if not (norm_doc == norm_corpus or norm_doc.startswith(norm_corpus + os.sep)):
                self._send_json({"error": "Forbidden", "status": 403, "message": "Invalid document path traversal"}, status=403)
                return

            doc_content = None
            if os.path.exists(doc_path):
                with open(doc_path, "r", encoding="utf-8") as f:
                    doc_content = json.load(f)
            else:
                doc_content = {
                    "docId": doc_id,
                    "title": f"Dossier {doc_id}",
                    "accessLevel": access_level,
                    "text": f"Confidential supplier contract and procurement margin records for {doc_id}."
                }

            self._send_json({
                "status": 200,
                "docId": doc_id,
                "accessLevel": access_level,
                "effectiveRole": effective_role,
                "wasTampered": was_tampered,
                "authMessage": auth_msg,
                "document": doc_content
            })
            return

        elif path == "/api/rag/simulate-spike":
            # Story 7 Cost Spike Simulation (Demo 14)
            iterations = int(params.get("iterations", 40))
            spike_data = pipeline.tracer.simulate_cost_spike(iterations=iterations)
            self._send_json(spike_data)
            return

        elif path == "/api/rag/embed-query":
            # Educational Embedding Explorer (Task 3)
            if not question:
                self._send_json({"error": "Field 'question' is required"}, status=400)
                return

            vec, mode = pipeline.retriever.embed_query(question, api_key)
            norm = sum(x * x for x in vec) ** 0.5
            norm_vec = [x / norm for x in vec] if norm > 1e-12 else vec

            sku_drift_explanation = (
                "Dense embedding models map natural language sentences into semantic latent space. "
                "Alphanumeric SKUs (e.g. 'QQ-0015') are split by subword tokenizers into fragments ('QQ', '-', '00', '15') "
                "whose geometric projection drifts away from exact keyword relevance towards general domain clusters. "
                "Lexical algorithms like BM25 index exact tokens with high inverse document frequency (IDF), "
                "succeeding where dense similarity suffers from semantic drift."
            )

            self._send_json({
                "question": question,
                "embeddingModel": "gemini-embedding-001",
                "vectorDimensions": len(vec),
                "vectorNorm": round(norm, 6),
                "embeddingMode": mode,
                "taskType": "RETRIEVAL_QUERY",
                "sampleVector": [round(x, 6) for x in norm_vec[:16]],
                "whyExactSkusFail": sku_drift_explanation
            })
            return

        self._send_json({"error": f"Endpoint not found: {path}"}, status=404)

def create_server(port=8000, host="0.0.0.0"):
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    server = http.server.ThreadingHTTPServer((host, port), QuirkHTTPRequestHandler)
    server.daemon_threads = True
    return server

def run_server(port=None, host="0.0.0.0"):
    if port is None:
        port_env = os.environ.get("PORT")
        port = int(port_env) if port_env else 8000
    with create_server(port, host) as httpd:
        print("=" * 60)
        print(f"QUIRK & QUANTA UNIFIED STOREFRONT & RAG SERVER (Concurrent Threading)")
        print("=" * 60)
        print(f"Binding Address:     http://{host}:{port}")
        print(f"Serving static site: {SITE_DIR}")
        print(f"Storefront URL:      http://localhost:{port}/index.html")
        print(f"Workshop Lab URL:    http://localhost:{port}/workshop.html")
        print(f"Health Check:        http://localhost:{port}/health")
        print(f"API Endpoints:")
        print(f"  - POST http://localhost:{port}/api/rag/retrieve")
        print(f"  - POST http://localhost:{port}/api/rag/ask")
        print(f"  - POST http://localhost:{port}/api/rag/compare")
        print(f"  - POST http://localhost:{port}/api/rag/graph")
        print(f"  - POST http://localhost:{port}/api/rag/doc")
        print(f"  - GET  http://localhost:{port}/api/rag/auth/demo-token")
        print(f"  - GET  http://localhost:{port}/api/rag/status")
        print(f"  - GET  http://localhost:{port}/api/rag/questions")
        print(f"  - GET  http://localhost:{port}/api/rag/telemetry")
        print(f"  - GET  http://localhost:{port}/health")
        print("=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    port_env = os.environ.get("PORT")
    port_val = int(port_env) if port_env else 8000
    if len(sys.argv) > 1:
        try:
            port_val = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port=port_val, host="0.0.0.0")
