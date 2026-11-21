#!/usr/bin/env python3
"""
Quirk & Quanta - OKF (Open Knowledge Format) Validator
Validates manifest.json, entities.jsonl, and relations.jsonl in data/okf/.
Zero external dependencies.
"""

import os
import sys
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OKF_DIR = os.path.join(ROOT_DIR, "data", "okf")

def validate_okf():
    print("=" * 60)
    print("VALIDATING OPEN KNOWLEDGE FORMAT (OKF) BUNDLE")
    print(f"Directory: {OKF_DIR}")
    print("=" * 60)

    # 1. Check Files
    manifest_path = os.path.join(OKF_DIR, "manifest.json")
    entities_path = os.path.join(OKF_DIR, "entities.jsonl")
    relations_path = os.path.join(OKF_DIR, "relations.jsonl")

    assert os.path.exists(manifest_path), "Missing manifest.json"
    assert os.path.exists(entities_path), "Missing entities.jsonl"
    assert os.path.exists(relations_path), "Missing relations.jsonl"

    # 2. Check Manifest
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest.get("format") == "open-knowledge-format", f"Invalid format: {manifest.get('format')}"
    assert manifest.get("formatVersion") == "1.0.0", f"Invalid formatVersion: {manifest.get('formatVersion')}"
    
    schema = manifest.get("schema", {})
    entity_type_names = {t["name"] for t in schema.get("entityTypes", [])}
    relation_type_names = {t["name"] for t in schema.get("relationTypes", [])}

    print(f"✓ Manifest format valid: {manifest['format']} v{manifest['formatVersion']}")
    print(f"✓ Defined entity types: {', '.join(sorted(entity_type_names))}")
    print(f"✓ Defined relation types: {', '.join(sorted(relation_type_names))}")

    # 3. Check Entities
    entities = {}
    with open(entities_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            entity = json.loads(line)
            eid = entity.get("id")
            etype = entity.get("type")
            assert eid, f"Entity at line {idx} missing 'id'"
            assert etype in entity_type_names, f"Entity {eid} has unregistered type: {etype}"
            assert eid not in entities, f"Duplicate entity id: {eid}"
            entities[eid] = entity

    print(f"✓ Validated {len(entities)} entities from entities.jsonl")

    # 4. Check Relations
    relations = []
    with open(relations_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            rel = json.loads(line)
            rid = rel.get("id")
            rtype = rel.get("type")
            src = rel.get("sourceId")
            tgt = rel.get("targetId")

            assert rid, f"Relation at line {idx} missing 'id'"
            assert rtype in relation_type_names, f"Relation {rid} has unregistered type: {rtype}"
            assert src in entities, f"Relation {rid} sourceId {src} not found in entities"
            assert tgt in entities, f"Relation {rid} targetId {tgt} not found in entities"
            relations.append(rel)

    print(f"✓ Validated {len(relations)} relations from relations.jsonl (referential integrity intact)")

    # 5. Check Counts against manifest
    expected_entities = manifest.get("counts", {}).get("entities")
    expected_relations = manifest.get("counts", {}).get("relations")
    assert len(entities) == expected_entities, f"Entity count mismatch: expected {expected_entities}, got {len(entities)}"
    assert len(relations) == expected_relations, f"Relation count mismatch: expected {expected_relations}, got {len(relations)}"

    print(f"✓ Integrity counts match manifest: {len(entities)} entities, {len(relations)} relations")

    # 6. Verify Multi-hop path exists
    # QQ-0011 -> COMP-025 -> REC-VREG-01 -> SUP-008
    qq0011_comp = any(r["sourceId"] == "QQ-0011" and r["targetId"] == "COMP-025" and r["type"] == "CONTAINS" for r in relations)
    comp_recall = any(r["sourceId"] == "COMP-025" and r["targetId"] == "REC-VREG-01" and r["type"] == "AFFECTED_BY" for r in relations)
    comp_sup = any(r["sourceId"] == "COMP-025" and r["targetId"] == "SUP-008" and r["type"] == "SUPPLIED_BY" for r in relations)

    assert qq0011_comp, "Multi-hop link QQ-0011 -> COMP-025 missing"
    assert comp_recall, "Multi-hop link COMP-025 -> REC-VREG-01 missing"
    assert comp_sup, "Multi-hop link COMP-025 -> SUP-008 missing"

    print("✓ Film Defect Multi-Hop Graph Traversal path verified!")
    print("=" * 60)
    print("OKF BUNDLE VALIDATION PASSED (100% CONFORMANT)")
    print("=" * 60)
    return True

if __name__ == "__main__":
    if validate_okf():
        sys.exit(0)
    else:
        sys.exit(1)
