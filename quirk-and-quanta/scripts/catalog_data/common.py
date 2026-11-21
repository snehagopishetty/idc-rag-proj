# Common product factory and validator helper

def make_product(
    id_num,
    sku,
    slug,
    name,
    category_id,
    category,
    subcategory,
    collection_id,
    collection,
    short_desc,
    long_desc,
    features,
    attributes,
    selling_price,
    cost_price,
    list_price,
    stock_status,
    inventory_count,
    rating,
    review_count,
    warranty_months,
    shipping_days,
    return_window_days,
    tags,
    alt_text,
    reviews,
    supplier_id,
    supplier_name,
    supplier_code,
    procurement_batch,
    warehouse_id,
    reorder_threshold,
    internal_notes,
    qc_status,
    related_products,
    compatible_with,
    bundle_with,
    material_ids,
    component_ids,
    policy_ids
):
    # Word count checks and adjustments if needed
    short_words = short_desc.strip().split()
    if not (15 <= len(short_words) <= 35):
        raise ValueError(f"[{sku}] shortDescription word count {len(short_words)} outside [15, 35]: {short_desc}")

    long_words = long_desc.strip().split()
    if not (80 <= len(long_words) <= 150):
        raise ValueError(f"[{sku}] longDescription word count {len(long_words)} outside [80, 150]: {len(long_words)} words")

    if not (cost_price < selling_price <= list_price):
        raise ValueError(f"[{sku}] Pricing violation: cost ({cost_price}) < selling ({selling_price}) <= list ({list_price})")

    margin_amount = round(selling_price - cost_price, 2)
    margin_percent = round(((selling_price - cost_price) / selling_price) * 100, 2)

    if len(attributes) < 6:
        raise ValueError(f"[{sku}] Attributes count {len(attributes)} < 6")

    return {
        "id": f"prod-{id_num:04d}",
        "sku": sku,
        "slug": slug,
        "name": name,
        "brand": "Quirk & Quanta",
        "categoryId": category_id,
        "category": category,
        "subcategory": subcategory,
        "collectionId": collection_id,
        "collection": collection,
        "currency": "INR",
        "public": {
            "shortDescription": short_desc.strip(),
            "longDescription": long_desc.strip(),
            "features": features,
            "attributes": attributes,
            "sellingPrice": selling_price,
            "listPrice": list_price,
            "stockStatus": stock_status,
            "inventoryCount": inventory_count,
            "rating": rating,
            "reviewCount": review_count,
            "warrantyMonths": warranty_months,
            "shippingDays": shipping_days,
            "returnWindowDays": return_window_days,
            "tags": tags,
            "images": {
                "thumbnail": f"assets/products/{sku}-thumb.svg",
                "primary": f"assets/products/{sku}.svg",
                "alt": alt_text
            },
            "reviews": reviews
        },
        "internal": {
            "costPrice": cost_price,
            "marginAmount": margin_amount,
            "marginPercent": margin_percent,
            "supplierId": supplier_id,
            "supplierName": supplier_name,
            "supplierCode": supplier_code,
            "procurementBatchId": procurement_batch,
            "warehouseId": warehouse_id,
            "reorderThreshold": reorder_threshold,
            "internalNotes": internal_notes,
            "qualityControlStatus": qc_status,
            "accessLevel": "admin",
            "allowedRoles": ["admin", "procurement"]
        },
        "relationships": {
            "relatedProducts": related_products,
            "compatibleWith": compatible_with,
            "bundleWith": bundle_with,
            "supplierId": supplier_id,
            "collectionId": collection_id,
            "materialIds": material_ids,
            "componentIds": component_ids,
            "policyIds": policy_ids
        },
        "metadata": {
            "isFictional": True,
            "schemaVersion": "1.0",
            "createdAt": "2026-11-18",
            "updatedAt": "2026-11-18"
        }
    }
