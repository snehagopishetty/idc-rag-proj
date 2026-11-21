#!/usr/bin/env python3
"""
Quirk & Quanta - Deterministic Document Corpus Builder
Extracts canonical product, supplier, component, recall, policy, and internal
records into a structured, dual-partitioned document corpus (public vs internal).
"""

import os
import sys
import json
import hashlib
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_INTERNAL = os.path.join(ROOT_DIR, "data", "internal")
CORPUS_DIR = os.path.join(ROOT_DIR, "data", "corpus")

os.makedirs(CORPUS_DIR, exist_ok=True)

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def build_corpus():
    print("=" * 60)
    print("BUILDING DETERMINISTIC RAG DOCUMENT CORPUS")
    print("=" * 60)

    products = load_json(os.path.join(DATA_INTERNAL, "products.full.json"))
    suppliers = load_json(os.path.join(DATA_INTERNAL, "suppliers.json"))
    components = load_json(os.path.join(DATA_INTERNAL, "components.json"))
    recalls = load_json(os.path.join(DATA_INTERNAL, "recalls.json"))
    policies = {p["id"]: p for p in load_json(os.path.join(DATA_INTERNAL, "policies.json"))}

    public_docs = []
    internal_docs = []

    # -------------------------------------------------------------
    # 1. Product Documents (3 public documents per product)
    # -------------------------------------------------------------
    for p in products:
        sku = p["sku"]
        name = p["name"]
        cat = p["category"]
        subcat = p["subcategory"]
        coll = p["collection"]

        # Doc 1: Description & Features (Public)
        features_text = "\n".join([f"- {f}" for f in p["public"].get("features", [])])
        tags_text = ", ".join(p["public"].get("tags", []))
        desc_content = f"""# {name} ({sku})
**Category:** {cat} > {subcat} | **Collection:** {coll}
**Tags:** {tags_text}

## Overview
{p['public']['shortDescription']}

## Theoretical Brief
{p['public']['longDescription']}

## Key Features
{features_text}
""".strip()

        public_docs.append({
            "docId": f"DOC-PROD-{sku}-DESC",
            "sourceId": sku,
            "sourceType": "product",
            "title": f"{name} - Description & Features",
            "category": cat,
            "accessLevel": "public",
            "allowedRoles": ["customer", "admin", "procurement"],
            "metadata": {
                "sku": sku,
                "section": "description",
                "collectionId": p["collectionId"],
                "citation": {
                    "label": f"{name} [SKU: {sku}]",
                    "url": f"product.html?sku={sku}",
                    "sectionName": "Overview & Features"
                }
            },
            "content": desc_content,
            "contentHash": compute_hash(desc_content)
        })

        # Doc 2: Technical Specifications & Attributes (Public)
        attrs = p["public"].get("attributes", {})
        attr_lines = []
        for k, v in attrs.items():
            formatted_k = k.replace("_", " ").title()
            val_str = ", ".join(v) if isinstance(v, list) else str(v)
            attr_lines.append(f"- **{formatted_k}:** {val_str}")
        attr_text = "\n".join(attr_lines)

        spec_content = f"""# Technical Specifications: {name} ({sku})
**Category:** {cat} > {subcat} | **SKU:** {sku}
**Selling Price:** ₹{p['public']['sellingPrice']:,} (MSRP List Price: ₹{p['public']['listPrice']:,})
**Stock Availability:** {p['public']['stockStatus'].replace('_', ' ').title()} ({p['public']['inventoryCount']} units available)
**Customer Rating:** {p['public']['rating']:.1f} / 5.0 ({p['public']['reviewCount']} verified reviews)

## Verified Technical Attributes
{attr_text}

## Dimension & Tolerance Standards
- **Warranty Coverage:** {p['public']['warrantyMonths']} Months Hardware Integrity Guarantee
- **Shipping Logistics:** {p['public']['shippingDays']['minimum']} to {p['public']['shippingDays']['maximum']} business days transit
- **Return Period:** {p['public']['returnWindowDays']} Calendar Days
""".strip()

        public_docs.append({
            "docId": f"DOC-PROD-{sku}-SPEC",
            "sourceId": sku,
            "sourceType": "product",
            "title": f"{name} - Technical Specifications",
            "category": cat,
            "accessLevel": "public",
            "allowedRoles": ["customer", "admin", "procurement"],
            "metadata": {
                "sku": sku,
                "section": "specifications",
                "sellingPrice": p["public"]["sellingPrice"],
                "citation": {
                    "label": f"{name} Specifications [SKU: {sku}]",
                    "url": f"product.html?sku={sku}#specs",
                    "sectionName": "Technical Specifications Table"
                }
            },
            "content": spec_content,
            "contentHash": compute_hash(spec_content)
        })

        # Doc 3: Product Policies & Guarantees (Public)
        ret_pol_id = p["relationships"].get("policyIds", ["POL-RET-14"])[0] if p["relationships"].get("policyIds") else "POL-RET-14"
        ret_pol = policies.get(ret_pol_id, {})
        
        pol_content = f"""# Commercial Policies & Guarantees: {name} ({sku})
**Product:** {name} [{sku}] | **Category:** {cat}

## Return Protocol ({p['public']['returnWindowDays']}-Day Window)
- Policy Identifier: {ret_pol.get('id', 'POL-RET-14')}
- Title: {ret_pol.get('title', 'Standard Return Protocol')}
- Conditions: Returns permitted within {p['public']['returnWindowDays']} days provided original structural integrity and packaging are uncompromised.
- Procedure: Dispatched back to Central Logistics Hub with proof of acquisition.

## Warranty Protocol ({p['public']['warrantyMonths']} Months)
- Coverage: {p['public']['warrantyMonths']} months protection against manufacturing deviation, bearing friction, or micro-component fatigue.
- Exclusions: Intentional disassembly, particle accelerator exposure, or unauthorized quantum alteration.

## Shipping & Logistics
- Transit Velocity: Standard Ground Logistics ({p['public']['shippingDays']['minimum']}-{p['public']['shippingDays']['maximum']} business days across India).
- Packaging: Sealed with shock-absorbing vibration dampening material.
""".strip()

        public_docs.append({
            "docId": f"DOC-PROD-{sku}-POL",
            "sourceId": sku,
            "sourceType": "product",
            "title": f"{name} - Policies & Guarantees",
            "category": cat,
            "accessLevel": "public",
            "allowedRoles": ["customer", "admin", "procurement"],
            "metadata": {
                "sku": sku,
                "section": "policies",
                "citation": {
                    "label": f"{name} Policies [SKU: {sku}]",
                    "url": f"product.html?sku={sku}#policies",
                    "sectionName": "Commercial Guarantees"
                }
            },
            "content": pol_content,
            "contentHash": compute_hash(pol_content)
        })

        # ---------------------------------------------------------
        # Doc 4: Confidential Internal Procurement Record (INTERNAL)
        # ---------------------------------------------------------
        internal_data = p.get("internal", {})
        proc_content = f"""# CONFIDENTIAL PROCUREMENT DOSSIER: {name} ({sku})
**SECURITY CLASSIFICATION: INTERNAL PROCUREMENT ONLY**
**AUTHORIZED ROLES: ADMIN, PROCUREMENT**

## Accounting & Profit Margin Analysis
- **Stock Keeping Unit (SKU):** {sku}
- **Product Title:** {name}
- **Wholesale Procurement Cost (costPrice):** ₹{internal_data.get('costPrice', 0):,} INR
- **Customer Selling Price (sellingPrice):** ₹{p['public']['sellingPrice']:,} INR
- **List Price (listPrice):** ₹{p['public']['listPrice']:,} INR
- **Gross Margin Amount (marginAmount):** ₹{internal_data.get('marginAmount', 0):,} INR
- **Gross Profit Margin Percentage (marginPercent):** {internal_data.get('marginPercent', 0):.2f}%

## Supply Chain & Warehouse Telemetry
- **Primary Supplier Code:** {internal_data.get('supplierId', 'UNKNOWN')} ({internal_data.get('supplierName', 'Direct Vendor')})
- **Vendor Catalog Part Number:** {internal_data.get('supplierCode', 'N/A')}
- **Active Manufacturing Batch ID:** {internal_data.get('procurementBatchId', 'N/A')}
- **Storage Facility ID:** {internal_data.get('warehouseId', 'WH-BLR-01')}
- **Safety Reorder Threshold:** {internal_data.get('reorderThreshold', 10)} units
- **Quality Control Status:** {internal_data.get('qualityControlStatus', 'approved').upper()}
- **Safety Recall Reference:** {internal_data.get('recallNoticeId') or 'None (Compliant)'}

## Engineering & Internal Quality Notes
{internal_data.get('internalNotes', 'No confidential notes recorded.')}
""".strip()

        internal_docs.append({
            "docId": f"DOC-INT-{sku}-PROC",
            "sourceId": sku,
            "sourceType": "internal_procurement",
            "title": f"Confidential Procurement Record - {name} [{sku}]",
            "category": cat,
            "accessLevel": "internal_procurement",
            "allowedRoles": ["admin", "procurement"],
            "metadata": {
                "sku": sku,
                "costPrice": internal_data.get("costPrice"),
                "marginAmount": internal_data.get("marginAmount"),
                "marginPercent": internal_data.get("marginPercent"),
                "supplierId": internal_data.get("supplierId"),
                "procurementBatchId": internal_data.get("procurementBatchId"),
                "citation": {
                    "label": f"Procurement File [SKU: {sku}] (Internal)",
                    "url": "internal/procurement",
                    "sectionName": "Confidential Unit Economics"
                }
            },
            "content": proc_content,
            "contentHash": compute_hash(proc_content)
        })

    # -------------------------------------------------------------
    # 2. Supplier Dossiers (Public B2B)
    # -------------------------------------------------------------
    for s in suppliers:
        sid = s["id"]
        s_content = f"""# Supplier Dossier: {s['name']} ({sid})
**Supplier Identifier:** {sid}
**Headquarters / Facility:** {s.get('location', 'Bengaluru, India')}
**Production Lead Time:** {s.get('leadTimeDays', 14)} Business Days
**Compliance & Quality Certifications:** {', '.join(s.get('certifications', []))}
**Primary Manufacturing Specialty:** {s.get('specialty', 'Scientific Equipment Sourcing')}

## Capabilities & Vendor Profile
{s.get('description', 'Verified vendor providing precision components and finished assemblies for Quirk & Quanta.')}

## Commercial Terms
- Standard Lead Time: {s.get('leadTimeDays', 14)} calendar days
- Quality Assurance Rating: {s.get('rating', 4.8)} / 5.0
""".strip()

        public_docs.append({
            "docId": f"DOC-SUP-{sid}",
            "sourceId": sid,
            "sourceType": "supplier",
            "title": f"Supplier Profile: {s['name']} [{sid}]",
            "category": "Supply Chain",
            "accessLevel": "public",
            "allowedRoles": ["customer", "admin", "procurement"],
            "metadata": {
                "supplierId": sid,
                "citation": {
                    "label": f"Supplier Dossier [{sid}: {s['name']}]",
                    "url": f"suppliers#{sid}",
                    "sectionName": "Vendor Qualifications"
                }
            },
            "content": s_content,
            "contentHash": compute_hash(s_content)
        })

    # -------------------------------------------------------------
    # 3. Component Specifications (Public)
    # -------------------------------------------------------------
    for c in components:
        cid = c["id"]
        c_content = f"""# Component Engineering Specification: {c['name']} ({cid})
**Component Code:** {cid}
**Component Classification:** {c.get('type', 'Standard Material')}
**Primary Supplier:** {c.get('supplierId', 'N/A')}
**Compliance Standards:** {c.get('complianceStandard', 'Industry Standard')}

## Technical Specifications
{c.get('specifications', 'Verified component meeting precision laboratory specifications.')}

## Physical Properties & Description
{c.get('description', 'Precision component utilized in Quirk & Quanta catalog assemblies.')}
""".strip()

        public_docs.append({
            "docId": f"DOC-COMP-{cid}",
            "sourceId": cid,
            "sourceType": "component",
            "title": f"Component Spec: {c['name']} [{cid}]",
            "category": "Components & Materials",
            "accessLevel": "public",
            "allowedRoles": ["customer", "admin", "procurement"],
            "metadata": {
                "componentId": cid,
                "supplierId": c.get("supplierId"),
                "citation": {
                    "label": f"Component Specification [{cid}: {c['name']}]",
                    "url": f"components#{cid}",
                    "sectionName": "Material Specifications"
                }
            },
            "content": c_content,
            "contentHash": compute_hash(c_content)
        })

    # -------------------------------------------------------------
    # 4. Recall Bulletins (Public Compliance)
    # -------------------------------------------------------------
    for r in recalls:
        rid = r["id"]
        r_content = f"""# Quality Control Recall Bulletin: {r['title']} ({rid})
**Bulletin Identifier:** {rid}
**Official QC Code:** {r.get('recallCode', 'QC-GENERIC')}
**Severity Rating:** {r.get('severity', 'low').upper()}
**Current Status:** {r.get('status', 'active').upper()}
**Reported Date:** {r.get('reportedDate', '2026-10-01')}
**Directly Affected Component ID:** {r.get('componentId', 'N/A')}
**Associated Supplier Code:** {r.get('supplierId', 'N/A')}
**Affected Production Lot:** {r.get('affectedBatch', 'N/A')}

## Root Cause Analysis & Defect Reason
{r.get('reason', 'Quality assurance variance detected during lifecycle endurance testing.')}

## Mandatory Remediation Protocol
{r.get('actionRequired', 'Perform recalibration and inspection prior to inventory dispatch.')}
""".strip()

        public_docs.append({
            "docId": f"DOC-REC-{rid}",
            "sourceId": rid,
            "sourceType": "recall",
            "title": f"QC Recall Bulletin: {r['title']} [{rid}]",
            "category": "Quality Assurance",
            "accessLevel": "public",
            "allowedRoles": ["customer", "admin", "procurement"],
            "metadata": {
                "recallId": rid,
                "componentId": r.get("componentId"),
                "supplierId": r.get("supplierId"),
                "citation": {
                    "label": f"Quality Advisory [{rid}: {r.get('recallCode')}]",
                    "url": f"recalls#{rid}",
                    "sectionName": "Quality Control Advisory"
                }
            },
            "content": r_content,
            "contentHash": compute_hash(r_content)
        })

    # -------------------------------------------------------------
    # 5. Write Corpus Files
    # -------------------------------------------------------------
    public_path = os.path.join(CORPUS_DIR, "corpus_public.json")
    internal_path = os.path.join(CORPUS_DIR, "corpus_internal.json")
    manifest_path = os.path.join(CORPUS_DIR, "corpus_manifest.json")

    with open(public_path, "w", encoding="utf-8") as f:
        json.dump(public_docs, f, indent=2)

    with open(internal_path, "w", encoding="utf-8") as f:
        json.dump(internal_docs, f, indent=2)

    manifest = {
        "version": "1.0.0",
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "publicDocumentCount": len(public_docs),
        "internalDocumentCount": len(internal_docs),
        "totalDocumentCount": len(public_docs) + len(internal_docs),
        "countsByType": {
            "product_description": 100,
            "product_specifications": 100,
            "product_policies": 100,
            "supplier_dossier": len(suppliers),
            "component_spec": len(components),
            "recall_bulletin": len(recalls),
            "confidential_procurement": len(internal_docs)
        },
        "accessLevels": {
            "public": len(public_docs),
            "internal_procurement": len(internal_docs)
        },
        "publicCorpusHash": compute_hash(json.dumps(public_docs, sort_keys=True)),
        "internalCorpusHash": compute_hash(json.dumps(internal_docs, sort_keys=True))
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Generated {len(public_docs)} public documents -> data/corpus/corpus_public.json")
    print(f"Generated {len(internal_docs)} internal documents -> data/corpus/corpus_internal.json")
    print(f"Total documents in corpus: {len(public_docs) + len(internal_docs)}")
    print(f"Corpus manifest saved -> data/corpus/corpus_manifest.json")
    print("SUCCESS: Corpus built cleanly with deterministic IDs.")

if __name__ == "__main__":
    build_corpus()
