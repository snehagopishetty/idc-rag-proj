# Retrieval API Contract & Data Interchange Specification

This document defines the formal request and response contracts for the Quirk & Quanta RAG API service.

---

## 1. Endpoints Overview

| Method | Path | Description | Access Level |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/rag/retrieve` | Retrieval-only vector search (returns scored evidence and citations without LLM generation). | Public / RBAC filtered |
| `POST` | `/api/rag/ask` | Full RAG pipeline (retrieves evidence, generates grounded answer, maps citations). | Public / RBAC filtered |
| `GET` | `/api/rag/status` | Service health, active embedding model, vector counts, and Gemini credentials status. | Public |
| `GET` | `/api/rag/questions` | Returns the 22 curated golden evaluation questions across all test families. | Public |
| `GET` | `/api/rag/telemetry` | Comparative chunk telemetry across fixed, sliding, and semantic strategies. | Public |

---

## 2. Request Contracts

### 2.1 `POST /api/rag/retrieve` & `POST /api/rag/ask`

#### Request Headers
```http
Content-Type: application/json
```

#### JSON Request Body
```json
{
  "question": "What are the specifications and selling price of QQ-0015?",
  "topK": 5,
  "strategy": "semantic",
  "role": "customer"
}
```

#### Field Specifications
| Field | Type | Required | Default | Allowed Values | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `question` | string | **Yes** | — | Non-empty string | The natural language query, SKU, or concept. |
| `topK` | integer | No | `5` | `1` to `10` | Maximum number of ranked evidence chunks to return. |
| `strategy` | string | No | `"semantic"` | `["semantic", "fixed", "sliding"]` | Chunking dataset to search against. |
| `role` | string | No | `"customer"` | `["customer", "admin", "procurement"]` | User authorization role for RBAC filtering. |

---

## 3. Response Contracts

### 3.1 `POST /api/rag/retrieve` (Retrieval-Only Mode)
```json
{
  "query": "What are the specifications and selling price of QQ-0015?",
  "role": "customer",
  "strategy": "semantic",
  "topK": 3,
  "retrievalOnly": true,
  "embeddingMode": "cached_query_embedding",
  "evidenceCount": 3,
  "answer": null,
  "evidence": [
    {
      "rank": 1,
      "score": 0.4302,
      "chunkId": "CHK-DOC-PROD-QQ-0015-SPEC-SEM-header-information-01",
      "docId": "DOC-PROD-QQ-0015-SPEC",
      "sourceId": "QQ-0015",
      "accessLevel": "public",
      "strategy": "semantic",
      "sectionTitle": "Header Information",
      "text": "[Newton's Cradle Executive Edition - Technical Specifications | Section: Header Information]\n# Technical Specifications: Newton's Cradle Executive Edition (QQ-0015)\n**Category:** Desk & Office > Desk Toys | **SKU:** QQ-0015\n**Selling Price:** ₹2,499 (MSRP List Price: ₹3,499)",
      "citation": {
        "label": "Newton's Cradle Executive Edition Specifications [SKU: QQ-0015]",
        "url": "product.html?sku=QQ-0015#specs",
        "sectionName": "Technical Specifications Table"
      }
    }
  ],
  "latency": {
    "embeddingMs": 0.01,
    "retrievalMs": 57.36,
    "totalMs": 57.37
  }
}
```

### 3.2 `POST /api/rag/ask` (Full RAG Pipeline)
```json
{
  "question": "What are the specifications and selling price of QQ-0015?",
  "role": "customer",
  "strategy": "semantic",
  "topK": 3,
  "retrievalOnly": false,
  "executionMode": "offline_reference",
  "generationModel": "grounded_local_synthesizer",
  "answer": "According to verified catalog records [Newton's Cradle Executive Edition Specifications [SKU: QQ-0015]]: Newton's Cradle Executive Edition is priced at ₹2,499 (MSRP ₹3,499). It features five Grade 5 titanium balls suspended from high-tensile braided tungsten wire on a CNC-milled 6061 aluminum frame with a damping-reduction base.",
  "citations": [
    {
      "index": 1,
      "label": "Newton's Cradle Executive Edition Specifications [SKU: QQ-0015]",
      "url": "product.html?sku=QQ-0015#specs",
      "chunkId": "CHK-DOC-PROD-QQ-0015-SPEC-SEM-header-information-01",
      "score": 0.4302
    }
  ],
  "evidence": [ ... ],
  "latency": {
    "embeddingMs": 0.01,
    "retrievalMs": 57.36,
    "generationMs": 0.01,
    "totalMs": 57.38
  }
}
```

---

## 4. Role-Based Access Control (RBAC) Specification

| Role | Permitted Chunk Access Levels | Action on Confidential Data |
| :--- | :--- | :--- |
| **`customer`** | `["public"]` only | Completely suppressed at vector filtering stage before similarity scoring. Confidential chunks cannot appear in evidence or generated answers. |
| **`admin`** | `["public", "internal_procurement"]` | Included in vector search. Can retrieve unit wholesale costs (`costPrice`), margin amounts, and supplier batch codes. |
| **`procurement`**| `["public", "internal_procurement"]` | Identical to admin privileges for supply-chain documents. |

---

## 5. Error Codes & Handling

| HTTP Code | Error Message | Reason | Resolution |
| :--- | :--- | :--- | :--- |
| `400 Bad Request` | `{"error": "Field 'question' is required"}` | Missing or empty question string in request body. | Supply non-empty `"question": "..."` |
| `400 Bad Request` | `{"error": "Invalid JSON in request body"}` | Malformed JSON payload. | Check syntax, quoting, and JSON formatting. |
| `404 Not Found` | `{"error": "Endpoint not found: /api/invalid"}` | Route does not match registered API endpoints. | Consult the Endpoints Overview above. |
| `500 Server Error` | `{"error": "<details>"}` | Unexpected exception during retrieval or embedding. | Review server logs; check embedding files. |
