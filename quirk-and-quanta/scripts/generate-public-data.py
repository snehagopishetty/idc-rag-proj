#!/usr/bin/env python3
"""
Generate sanitized public storefront dataset from canonical internal data.
Uses a strict ALLOWLIST of safe fields.
Guarantees NO sensitive internal pricing, margin, supplier code, or warehouse
fields are leaked into the static site directory.
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERNAL_FILE = os.path.join(BASE_DIR, "data", "internal", "products.full.json")
PUBLIC_DIR = os.path.join(BASE_DIR, "site", "data")
PUBLIC_FILE = os.path.join(PUBLIC_DIR, "products.public.json")

# Strict ALLOWLIST of top-level allowed fields
ALLOWED_TOP_FIELDS = {
    "id",
    "sku",
    "slug",
    "name",
    "brand",
    "categoryId",
    "category",
    "subcategory",
    "collectionId",
    "collection",
    "currency",
    "public",
    "relationships",
    "metadata"
}

# Strict ALLOWLIST of public payload fields
ALLOWED_PUBLIC_FIELDS = {
    "shortDescription",
    "longDescription",
    "features",
    "attributes",
    "sellingPrice",
    "listPrice",
    "stockStatus",
    "inventoryCount",
    "rating",
    "reviewCount",
    "warrantyMonths",
    "shippingDays",
    "returnWindowDays",
    "tags",
    "images",
    "reviews"
}

# Strict ALLOWLIST of relationship fields exposed publicly
ALLOWED_RELATIONSHIPS_FIELDS = {
    "relatedProducts",
    "compatibleWith",
    "bundleWith",
    "collectionId",
    "policyIds"
}

# Blacklist of sensitive fields that MUST NEVER appear anywhere in public JSON
PROHIBITED_SUBSTRINGS = [
    "costPrice",
    "marginAmount",
    "marginPercent",
    "supplierCode",
    "procurementBatchId",
    "warehouseId",
    "internalNotes",
    "qualityControlStatus",
    "allowedRoles",
    "accessLevel"
]

def sanitize_product(raw):
    # Only allow explicit top-level fields
    sanitized = {}
    for key in ALLOWED_TOP_FIELDS:
        if key in raw:
            sanitized[key] = raw[key]

    # Sanitize public block
    pub_raw = raw.get("public", {})
    sanitized_pub = {}
    for key in ALLOWED_PUBLIC_FIELDS:
        if key in pub_raw:
            sanitized_pub[key] = pub_raw[key]
    sanitized["public"] = sanitized_pub

    # Sanitize relationships block (exclude internal supplierId, materialIds, componentIds)
    rel_raw = raw.get("relationships", {})
    sanitized_rel = {}
    for key in ALLOWED_RELATIONSHIPS_FIELDS:
        if key in rel_raw:
            sanitized_rel[key] = rel_raw[key]
    sanitized["relationships"] = sanitized_rel

    # Metadata
    sanitized["metadata"] = {
        "isFictional": True,
        "schemaVersion": "1.0",
        "accessScope": "public_storefront"
    }

    # Ensure "internal" section is completely absent
    if "internal" in sanitized:
        del sanitized["internal"]

    return sanitized

def main():
    if not os.path.exists(INTERNAL_FILE):
        print(f"Error: Internal file not found at {INTERNAL_FILE}")
        sys.exit(1)

    with open(INTERNAL_FILE, "r", encoding="utf-8") as f:
        full_products = json.load(f)

    os.makedirs(PUBLIC_DIR, exist_ok=True)

    sanitized_products = [sanitize_product(p) for p in full_products]

    # Convert to JSON string for verification
    output_json_str = json.dumps(sanitized_products, indent=2, ensure_ascii=False)

    # Perform strict security check on serialized JSON string
    for prohibited in PROHIBITED_SUBSTRINGS:
        if f'"{prohibited}"' in output_json_str:
            raise SecurityError(f"CRITICAL LEAK: Sensitive field '{prohibited}' detected in public output string!")

    with open(PUBLIC_FILE, "w", encoding="utf-8") as f:
        f.write(output_json_str)

    print("==================================================")
    print("QUIRK & QUANTA: Public Data Generation")
    print("==================================================")
    print(f"Input records:  {len(full_products)} from {INTERNAL_FILE}")
    print(f"Output records: {len(sanitized_products)} to {PUBLIC_FILE}")
    print(f"File size:      {len(output_json_str.encode('utf-8')) / 1024:.2f} KB")
    print("Security Check: PASS (Zero internal pricing, margins, or supplier codes leaked)")

if __name__ == "__main__":
    main()
