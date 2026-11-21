# Beyond Basic RAG: Building Production-Ready AI Systems
## Workshop Demonstration Project: Quirk & Quanta

Welcome to the technical repository for **Gate 1** of the masterclass workshop *"Beyond Basic RAG: Building Production-Ready AI Systems"*.

### Project Location
The complete fictional storefront application, canonical datasets, asset generators, verification tools, and technical documentation are located in:
👉 **[`quirk-and-quanta/`](quirk-and-quanta/)**

### Quick Launch
To run the static storefront locally:
```bash
cd quirk-and-quanta/site
python3 -m http.server 8000
```
Then navigate to: **`http://localhost:8000`**

### Verification
```bash
# Validate complete data schema, pricing invariants, and zero leakage
python3 quirk-and-quanta/scripts/validate-data.py

# Validate all 202 SVG assets
python3 quirk-and-quanta/scripts/validate-assets.py

# Run automated unit test suite
python3 -m unittest quirk-and-quanta/tests/test-data.py
```

For complete details, please see the [Quirk & Quanta README](quirk-and-quanta/README.md).
