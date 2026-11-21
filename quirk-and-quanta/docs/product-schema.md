# Canonical Product Schema Specification

This document details the exact JSON schema governing all 100 products in `data/internal/products.full.json`.

---

## 1. Top-Level Entity Structure

Each product record is a JSON object with six top-level sections:

```json
{
  "id": "prod-0001",
  "sku": "QQ-0001",
  "slug": "quantum-uncertainty-hoodie",
  "name": "Quantum Uncertainty Hoodie",
  "brand": "Quirk & Quanta",
  "categoryId": "CAT-APPAREL",
  "category": "Apparel",
  "subcategory": "Hoodies",
  "collectionId": "COL-QUANTUM",
  "collection": "Quantum Living",
  "currency": "INR",
  "public": { ... },
  "internal": { ... },
  "relationships": { ... },
  "metadata": { ... }
}
```

---

## 2. Section Details

### 2.1 Identity Fields
- `id` (string, regex: `prod-[0-9]{4}`): Unique internal product identifier.
- `sku` (string, regex: `QQ-[0-9]{4}`): Public Stock Keeping Unit. Sequence `QQ-0001` through `QQ-0100`.
- `slug` (string): URL-friendly kebab-case name.
- `name` (string): Brand product name.
- `brand` (string): Always `"Quirk & Quanta"`.
- `categoryId` (string): Primary category code (e.g. `CAT-APPAREL`).
- `category` (string): Human-readable category label (e.g. `"Apparel"`).
- `subcategory` (string): Specialized product subtype.
- `collectionId` (string): Curated theme ID (e.g. `COL-QUANTUM`).
- `collection` (string): Human-readable collection name (e.g. `"Quantum Living"`).
- `currency` (string): Currency code (always `"INR"`).

### 2.2 `public` Object (Safe for Client Delivery)
- `shortDescription` (string): Concise summary. Strictly constrained between **15 and 35 words**.
- `longDescription` (string): Comprehensive technical narrative. Strictly constrained between **80 and 150 words**.
- `features` (array of strings, length >= 4): Key functional bullet points.
- `attributes` (object, length >= 6 key-value pairs): Domain-specific technical specifications (e.g. `material`, `voltage`, `dimensions`, `tolerance`, `frequency`, `weight`).
- `sellingPrice` (integer): Actual retail customer price in INR.
- `listPrice` (integer): Original MSRP / list price in INR (`listPrice >= sellingPrice`).
- `stockStatus` (string, enum: `["in_stock", "low_stock"]`): Inventory indicator.
- `inventoryCount` (integer): Units available in warehouse.
- `rating` (float, range: `[4.2, 5.0]`): Composite review rating score.
- `reviewCount` (integer): Total customer reviews received.
- `warrantyMonths` (integer): Hardware defect guarantee period (0, 6, 12, or 24 months).
- `shippingDays` (object): `{"minimum": integer, "maximum": integer}` transit days.
- `returnWindowDays` (integer): Customer return window (7, 14, or 30 days).
- `tags` (array of strings, length >= 5): Search keywords and theoretical terms.
- `images` (object):
  - `thumbnail` (string): Relative path to 160x160 SVG (`assets/products/QQ-XXXX-thumb.svg`).
  - `primary` (string): Relative path to 400x400 SVG (`assets/products/QQ-XXXX.svg`).
  - `alt` (string): Descriptive accessibility text.
- `reviews` (array of 2+ objects):
  - `id` (string): Review identifier (e.g. `REV-0001`).
  - `rating` (integer, range `[4, 5]`): Individual score.
  - `title` (string): Review summary title.
  - `body` (string): Humorous fictional customer commentary.
  - `displayName` (string): Customer alias (e.g. `"Prof. T. Bose"`).
  - `isFictional` (boolean): Always `true`.

### 2.3 `internal` Object (CONFIDENTIAL — Stripped from Public JSON)
- `costPrice` (integer): Manufacturing acquisition cost in INR.
- `marginAmount` (integer): Exact gross profit in INR (`marginAmount = sellingPrice - costPrice`).
- `marginPercent` (float): Gross profit margin percentage rounded to 2 decimal places:
  $$\text{marginPercent} = \text{round}\left(\frac{\text{sellingPrice} - \text{costPrice}}{\text{sellingPrice}} \times 100, 2\right)$$
- `supplierId` (string): Reference to `suppliers.json` (e.g. `SUP-001`).
- `supplierName` (string): Legal vendor name.
- `supplierCode` (string): Vendor SKU / part identifier.
- `procurementBatchId` (string): Manufacturing lot code (e.g. `BATCH-2026-APP01`).
- `warehouseId` (string): Physical facility code (e.g. `WH-BLR-01`).
- `reorderThreshold` (integer): Safety stock trigger limit.
- `internalNotes` (string): Engineering observations and QC defect annotations.
- `recallNoticeId` (string or null): Reference to `recalls.json` if affected by a safety recall.
- `qualityControlStatus` (string, enum: `["approved", "under_review", "conditional"]`).
- `accessLevel` (string): RBAC gate level (e.g. `"admin"`).
- `allowedRoles` (array of strings): Authorized roles (`["admin", "procurement"]`).

### 2.4 `relationships` Object
- `relatedProducts` (array of 2-4 strings): SKUs of similar products in the catalog.
- `compatibleWith` (array of strings): SKUs of mathematically or physically compatible items.
- `bundleWith` (array of 1-3 strings): SKUs frequently acquired together in bundles.
- `supplierId` (string): Foreign key to `suppliers.json`.
- `collectionId` (string): Foreign key to `collections.json`.
- `materialIds` (array of strings): Component IDs used in exterior materials.
- `componentIds` (array of strings): Component IDs used in mechanical/electrical parts.
- `policyIds` (array of strings): Policy IDs governing returns, warranties, and shipping.

### 2.5 `metadata` Object
- `isFictional` (boolean): Always `true`.
- `schemaVersion` (string): `"1.0"`.
- `createdAt` (string, ISO date): `"2026-11-18"`.
- `updatedAt` (string, ISO date): `"2026-11-18"`.

---

## 3. Strict Mathematical Pricing Rules

Every product is verified by `scripts/validate-data.py` to satisfy:
1. $\text{costPrice} < \text{sellingPrice} \le \text{listPrice}$
2. $\text{marginAmount} = \text{sellingPrice} - \text{costPrice}$
3. $\text{marginPercent} = \text{round}\left(\frac{\text{marginAmount}}{\text{sellingPrice}} \times 100, 2\right)$
