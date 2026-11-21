# Quirk & Quanta — Precisely Unnecessary. Scientifically Delightful.

> **Gate 1 Storefront & Canonical Dataset**  
> Workshop: *"Beyond Basic RAG: Building Production-Ready AI Systems"*  
> Designed for ~100 engineers and researchers exploring modern AI architectures.

---

## 1. Executive Overview

**Quirk & Quanta** is an eccentric theoretical physicist's dream department store. It is built as a complete, visually polished, fully functional fictional e-commerce application using **plain HTML5, CSS3, and vanilla JavaScript**, with zero third-party packages or npm dependencies.

Gate 1 delivers the foundation for a multi-gate workshop covering advanced RAG topics including vector embeddings, semantic chunking, multi-hop GraphRAG, hybrid retrieval, RBAC authorization, and observability.

### Key Gate 1 Highlights
- **100 Unique Fictional Products** (`QQ-0001` through `QQ-0100`) strictly partitioned across **10 scientific categories** (10 products each).
- **Zero Third-Party Dependencies:** 100% vanilla browser code. No React, Vue, Tailwind, Bootstrap, jQuery, or Node modules.
- **Strict Data Separation:** Canonical internal data (cost prices, margins, suppliers, recall notices) resides strictly in `data/internal/`. The static site consumes only sanitized `site/data/products.public.json`.
- **202 Handcrafted SVG Assets:** Brand logo, 1200x500 hero banner, 100 distinct primary product illustrations, and 100 distinct thumbnails rendered via pure math and vector geometry.
- **Full Graph Relationships:** 1,206 graph edges connecting products, categories, collections, suppliers, components, recalls, and policies.
- **Client-Side E-Commerce Features:** Instant multi-facet filtering (search, categories, price range, stock status, ratings), sorting, URL param synchronization, cart drawer, stepper, "Frequently Synergized" bundles, related apparatus, and demo role preview toggle.

---

## 2. Directory Structure

```text
quirk-and-quanta/
├── site/                               # Deployable static storefront
│   ├── index.html                      # Homepage (hero, categories, trending, collections)
│   ├── products.html                   # Catalog (all 100 items, sidebar filters, sorting)
│   ├── product.html                    # Product Detail (specs, gallery, bundles, reviews)
│   ├── about.html                      # Brand Story & Workshop Context
│   ├── css/
│   │   ├── styles.css                  # Color system, reset, typography, layout grid
│   │   └── components.css              # Cards, badges, buttons, drawers, modals, tables
│   ├── js/
│   │   ├── app.js                      # Global state, cart storage, modals, toasts
│   │   ├── cart.js                     # Slide-out cart drawer, item updates, checkout demo
│   │   ├── catalog.js                  # Catalog filtering, sorting, and URL sync
│   │   ├── product-detail.js           # Detail renderer, specs table, bundles, reviews
│   │   ├── role-preview.js             # Customer vs Admin demo preview toggle
│   │   └── search.js                   # Live autocomplete preview dropdown
│   ├── data/
│   │   └── products.public.json        # Sanitized public product metadata (356 KB)
│   └── assets/
│       ├── logo.svg                    # Vector brand logo with atomic orbitals
│       ├── hero/
│       │   └── hero-banner.svg         # 1200x500 vector hero apparatus illustration
│       └── products/                   # 200 SVG vector files
│           ├── QQ-0001.svg ... QQ-0100.svg          # 100 Primary images (400x400)
│           └── QQ-0001-thumb.svg ... QQ-0100-thumb.svg # 100 Thumbnails (160x160)
├── data/
│   └── internal/                       # Canonical data (NEVER deployed to public site)
│       ├── products.full.json          # 100 complete products with cost prices & margins
│       ├── suppliers.json              # 12 fictional suppliers (SUP-001 - SUP-012)
│       ├── components.json             # 24 materials/components (COMP-001 - COMP-024)
│       ├── collections.json            # 8 curated collections (COL-...)
│       ├── recalls.json                # 5 QC / recall records (REC-001 - REC-005)
│       ├── policies.json               # 8 return, warranty, and shipping policies
│       └── graph-relationships.json    # 1,206 graph edges (Neo4j / GraphRAG ready)
├── scripts/
│   ├── generate_all_canonical_data.py  # Master generator for all internal JSON files
│   ├── generate-public-data.py         # Allowlist sanitizer for public JSON
│   ├── generate_all_assets.py          # Pure Python SVG generator for all 202 assets
│   ├── validate-data.py                # Schema, pricing math & referential validator
│   ├── validate-assets.py              # SVG structure and asset existence validator
│   └── catalog_data/                   # 10 modular category generators + graph builder
├── tests/
│   └── test-data.py                    # Automated unittest suite (8 test cases)
├── docs/
│   ├── architecture.md                 # Static delivery, data separation & security model
│   ├── product-schema.md               # Complete schema specification & pricing rules
│   ├── data-relationships.md           # Graph schema, node types, edge types & multi-hop paths
│   └── future-rag-integration.md       # Roadmap for Workshop Gates 2 through 11
├── package-not-required.txt            # Explicit explanation of zero-package philosophy
└── README.md                           # This document
```

---

## 3. Quick Start: Running Locally

Because modern web browsers restrict `fetch()` requests on raw `file://` URLs, serve the site using Python's built-in standard library HTTP server:

```bash
# Option 1: Serve directly from site/
cd quirk-and-quanta/site
python3 -m http.server 8000

# Open in browser:
# http://localhost:8000
```

```bash
# Option 2: Serve from repository root
cd quirk-and-quanta
python3 -m http.server 8000

# Open in browser:
# http://localhost:8000/site/
```

No build step, transpilation, or installation of any npm or pip package is required.

---

## 4. Validating the Project

Run the verification scripts and test suites directly using standard Python 3:

```bash
# 1. Validate complete data schema, pricing math, referential integrity & zero leaks
python3 quirk-and-quanta/scripts/validate-data.py

# 2. Validate all 202 SVG assets exist and are well-formed
python3 quirk-and-quanta/scripts/validate-assets.py

# 3. Run the automated unittest suite
python3 -m unittest quirk-and-quanta/tests/test-data.py
```

All commands exit with code `0` on success.

---

## 5. Security & Data Separation Architecture

A fundamental tenet of production RAG systems (and a core theme of this workshop) is:

> **"Client-side hiding is NOT security."**

To demonstrate this during the workshop:
1. **Public Storefront Data (`site/data/products.public.json`):** Generated using an explicit allowlist in `scripts/generate-public-data.py`. Prohibited fields (`costPrice`, `marginAmount`, `marginPercent`, `supplierId`, `internalNotes`, `procurementBatchId`, `recallNoticeId`) are completely omitted from the JSON payload.
2. **Canonical Internal Records (`data/internal/`):** Kept strictly outside the `site/` folder. Contains exact cost calculations, supplier terms, and batch-level recall data.
3. **Role Preview Switcher:** A prominent toggle in the storefront header allows workshop instructors to preview how UI annotations differ between customer and admin perspectives, emphasizing that true authorization requires server-side RBAC (to be built in Gate 9).

---

## 6. The 10 Product Categories

Every category contains **exactly 10 peer-reviewed items**:

| Code | Category | SKU Range | Sample Product |
| :--- | :--- | :--- | :--- |
| `CAT-APPAREL` | Apparel | `QQ-0001` - `QQ-0010` | Quantum Uncertainty Hoodie (`QQ-0001`) |
| `CAT-DESK` | Desk & Office | `QQ-0011` - `QQ-0020` | Atomic Orbit Desk Lamp (`QQ-0011`) |
| `CAT-KITCHEN` | Drinkware & Kitchen | `QQ-0021` - `QQ-0030` | Precision Pizza Cutting Wheel (`QQ-0029`) |
| `CAT-HOME` | Home & Decor | `QQ-0031` - `QQ-0040` | Optimal Seating Position Cushion (`QQ-0031`) |
| `CAT-GADGETS` | Science Gadgets | `QQ-0041` - `QQ-0050` | Desktop Plasma Orb (`QQ-0044`) |
| `CAT-PUZZLES` | Puzzles & Games | `QQ-0051` - `QQ-0060` | Train Routing Strategy Game (`QQ-0059`) |
| `CAT-STATIONERY` | Stationery & Learning | `QQ-0061` - `QQ-0070` | Roommate Protocol Notebook (`QQ-0061`) |
| `CAT-TECH` | Tech Accessories | `QQ-0071` - `QQ-0080` | Molecular Pattern Mechanical Keyboard (`QQ-0073`) |
| `CAT-RAILWAY` | Railway & Engineering | `QQ-0081` - `QQ-0090` | Precision Switching Track Section (`QQ-0087`) |
| `CAT-GIFTS` | Gifts & Collectibles | `QQ-0091` - `QQ-0100` | Roommate Agreement Framed Scroll (`QQ-0092`) |

---

## 7. Future Workshop Gates (Roadmap)

This storefront and canonical dataset provide the grounding foundation for subsequent workshop modules:

- **Gate 2: Embeddings & Vector Stores** — Generating vector embeddings for descriptions and specs using Gemini Embeddings.
- **Gate 3: Chunking Strategies** — Comparing fixed-size, sliding window, and semantic chunking on catalog documents.
- **Gate 4: Multi-Hop Failure Modes** — Demonstrating why vector similarity fails on questions like *"Which products use parts affected by the ceramic defect?"*.
- **Gate 5: BM25 Lexical Search** — Exact SKU and technical keyword matching.
- **Gate 6: Hybrid RAG** — Fusing dense vector and sparse lexical results via Reciprocal Rank Fusion (RRF).
- **Gate 7: GraphRAG with Neo4j AuraDB** — Ingesting `graph-relationships.json` for Cypher-based multi-hop graph queries.
- **Gate 8: Grounding & Abstention** — Guardrails and prompt constraints preventing hallucinated specifications.
- **Gate 9: Role-Based Access Control (RBAC)** — Backend session authentication filtering internal vs public metadata.
- **Gate 10: IDOR Vulnerability Exploits** — Hands-on penetration testing of authorization boundaries.
- **Gate 11: Observability & Evals** — Precision, recall, faithfulness, latency, and token cost telemetry.

---

## 8. Disclaimer

*Quirk & Quanta is an entirely fictional storefront created exclusively for educational demonstrations in the "Beyond Basic RAG" workshop. No products are available for purchase.*
