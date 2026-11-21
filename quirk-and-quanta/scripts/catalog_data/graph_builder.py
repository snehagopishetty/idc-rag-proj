"""
Graph relationship builder for Quirk & Quanta.
Compiles all relationship records connecting products, categories, suppliers,
collections, components, recalls, and policies.
"""

def build_graph_relationships(products, suppliers, components, collections, recalls, policies):
    relationships = []
    rel_id = 1

    def add_rel(source_id, rel_type, target_id, properties=None):
        nonlocal rel_id
        entry = {
            "id": f"REL-{rel_id:04d}",
            "sourceId": source_id,
            "relationship": rel_type,
            "targetId": target_id
        }
        if properties:
            entry["properties"] = properties
        relationships.append(entry)
        rel_id += 1

    # 1. PRODUCT -> BELONGS_TO -> CATEGORY
    for p in products:
        add_rel(p["sku"], "BELONGS_TO", p["categoryId"], {"categoryName": p["category"]})

    # 2. PRODUCT -> SUPPLIED_BY -> SUPPLIER
    for p in products:
        add_rel(p["sku"], "SUPPLIED_BY", p["relationships"]["supplierId"])

    # 3. PRODUCT -> PART_OF -> COLLECTION
    for p in products:
        add_rel(p["sku"], "PART_OF", p["relationships"]["collectionId"])

    # 4. PRODUCT -> CONTAINS -> COMPONENT / MATERIAL
    for p in products:
        materials = set(p["relationships"].get("materialIds", []) + p["relationships"].get("componentIds", []))
        for m in sorted(materials):
            add_rel(p["sku"], "CONTAINS", m)

    # 5. PRODUCT -> COMPATIBLE_WITH -> PRODUCT
    compat_count = 0
    for p in products:
        for c in p["relationships"].get("compatibleWith", []):
            add_rel(p["sku"], "COMPATIBLE_WITH", c)
            compat_count += 1

    # 6. PRODUCT -> RELATED_TO -> PRODUCT
    related_count = 0
    for p in products:
        for r in p["relationships"].get("relatedProducts", []):
            add_rel(p["sku"], "RELATED_TO", r)
            related_count += 1

    # 7. PRODUCT -> BUNDLED_WITH -> PRODUCT
    bundle_count = 0
    for p in products:
        for b in p["relationships"].get("bundleWith", []):
            add_rel(p["sku"], "BUNDLED_WITH", b)
            bundle_count += 1

    # 8. PRODUCT -> GOVERNED_BY -> POLICY
    for p in products:
        for pol in p["relationships"].get("policyIds", []):
            add_rel(p["sku"], "GOVERNED_BY", pol)

    # 9. SUPPLIER -> SUPPLIES -> COMPONENT
    for comp in components:
        add_rel(comp["supplierId"], "SUPPLIES", comp["id"], {"compliance": comp.get("complianceStandard")})

    # 10. COMPONENT -> AFFECTED_BY -> RECALL
    for rec in recalls:
        add_rel(rec["componentId"], "AFFECTED_BY", rec["id"], {
            "severity": rec["severity"],
            "batch": rec["affectedBatch"]
        })

    # Print summary counts for verification
    print(f"Generated {len(relationships)} total graph relationships.")
    print(f" - Compatibility links: {compat_count} (required >= 15)")
    print(f" - Related product links: {related_count} (required >= 20)")
    print(f" - Bundle links: {bundle_count} (required >= 15)")

    return relationships
