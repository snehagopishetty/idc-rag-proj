# Architecture Specification: Quirk & Quanta (Gate 1)

## 1. Architectural Principles

Quirk & Quanta is architected to satisfy three core requirements:
1. **Zero-Dependency Static Delivery:** Operates without node packages, build steps, or backend servers, served entirely via any static HTTP file server.
2. **Strict Public vs. Internal Data Separation:** Canonical business logic and sensitive procurement metrics are isolated outside the public static deployment surface.
3. **Extensibility for Multi-Stage RAG Modules:** Data schemas and relationship graphs are structured to ingest directly into vector databases, inverted indexes, and Neo4j graph databases in subsequent workshop gates.

---

## 2. System Layout & Data Flow

```text
[ Developer / Workshop Author ]
         │
         ├── scripts/generate_all_canonical_data.py
         │        │
         │        └───> data/internal/ (Canonical Knowledge Base)
         │                   ├── products.full.json
         │                   ├── suppliers.json
         │                   ├── components.json
         │                   ├── collections.json
         │                   ├── recalls.json
         │                   ├── policies.json
         │                   └── graph-relationships.json
         │
         └── scripts/generate-public-data.py (Allowlist Filter)
                  │
                  └───> site/data/products.public.json (Sanitized Public Dataset)
                                │
[ Browser Client / Attendees ]  │
         │                      │
         ├── index.html <───────┤ (Client-side JSON fetch)
         ├── products.html <────┤
         ├── product.html <─────┤
         └── about.html
```

---

## 3. Separation of Public vs. Internal Data

A primary learning objective of Gate 1 is demonstrating that **client-side hiding is not security**.

### 3.1 Canonical Internal Storage (`data/internal/`)
Contains complete, unfiltered business entity models:
- **`costPrice`**: Raw procurement acquisition expense in INR.
- **`marginAmount` & `marginPercent`**: Calculated internal profit margins.
- **`supplierId`, `supplierName`, `supplierCode`**: Direct manufacturing sources.
- **`procurementBatchId` & `warehouseId`**: Logistics tracing keys.
- **`internalNotes`**: Internal engineering observations, QC failure notes, and defect histories.
- **`recallNoticeId`**: Batch-level defect linkages used for multi-hop retrieval failure challenges.

This directory is **never placed within `site/`** and is omitted from public static hosting bundles.

### 3.2 Public Client Dataset (`site/data/products.public.json`)
The browser only ever downloads this pre-sanitized file. It is created using an explicit allowlist in `scripts/generate-public-data.py`. If a field is not on the allowlist, it is stripped.

Field allowlist:
- Identity: `id`, `sku`, `slug`, `name`, `brand`, `categoryId`, `category`, `subcategory`, `collectionId`, `collection`, `currency`
- Public metadata: `shortDescription`, `longDescription`, `features`, `attributes`, `sellingPrice`, `listPrice`, `stockStatus`, `inventoryCount`, `rating`, `reviewCount`, `warrantyMonths`, `shippingDays`, `returnWindowDays`, `tags`, `images`, `reviews`
- Safe public relationships: `relatedProducts` (SKUs), `compatibleWith` (SKUs), `bundleWith` (SKUs)

---

## 4. Client-Side State & Architecture

The frontend is implemented purely in ES6 JavaScript:

- **`js/app.js`**: Global state coordinator (`window.AppState`), localStorage synchronization for the shopping cart and wishlist, toast alerts, modal triggers.
- **`js/cart.js`**: Slide-out cart drawer, quantity stepper adjustments, subtotal calculation, checkout interception modal (educating users that purchasing is disabled).
- **`js/catalog.js`**: Client-side filtering engine executing sub-millisecond filtering across:
  - Free-text search across name, SKU, tags, category, and descriptions.
  - Category filtering via radio controls.
  - Price range min/max bounds.
  - Stock availability boolean filter.
  - Minimum customer rating filter.
  - 7 distinct sorting criteria (Price asc/desc, Rating desc, Name asc/desc, SKU asc, Featured).
  - Browser URL parameter synchronization (`window.history.replaceState`).
- **`js/product-detail.js`**: Validates SKU query parameter, manages tab switching (Full Description, Technical Specifications, Logistics & Guarantees), calculates "Frequently Synergized" bundle pricing, and renders customer reviews.
- **`js/search.js`**: Header live search preview with debounced keyboard listening and dropdown autocomplete suggestions.
- **`js/role-preview.js`**: Interactive demo switcher between `customer` and `admin` roles, previewing how future RBAC permissions will surface in the UI.

---

## 5. Visual System & Typography

- **Color Palette:**
  - Deep Academic Navy: `#18243A` (Headers, active states, typography)
  - Muted Teal: `#158D89` (Badges, accents, highlights, buttons)
  - Theoretical Gold: `#F4C95D` (Badges, tickers, ratings)
  - Crisp White: `#FFFFFF` (Card surfaces, clean backgrounds)
  - Neutral Workspace Gray: `#F7F8FA` (Page canvas)
  - Border Gray: `#E2E8F0`
- **Typography:** Clean system font stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`) with tabular monospace (`ui-monospace, "SF Mono", Menlo, Consolas, monospace`) for SKUs, equations, and code identifiers.
- **Responsive Grid:** Fluid CSS Grid with breakpoints at 768px and 1024px.
