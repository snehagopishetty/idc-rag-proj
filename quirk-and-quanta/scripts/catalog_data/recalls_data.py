# 5 Fictional Quality Control & Recall Records
RECALLS = [
    {
        "id": "REC-001",
        "recallCode": "QC-2026-MAG-01",
        "componentId": "COMP-004",
        "title": "Neodymium Magnet Array Flux Variance Advisory",
        "severity": "low",
        "status": "investigation_active",
        "affectedBatch": "BATCH-2026-MAG44",
        "reportedDate": "2026-10-12",
        "reason": "Flux measurement revealed a 0.08 Tesla deviation from theoretical dipole expectations in batch 44.",
        "actionRequired": "Re-meter all levitation kits using magnetometer calibration before warehouse dispatch.",
        "supplierId": "SUP-002"
    },
    {
        "id": "REC-002",
        "recallCode": "QC-2026-GAN-02",
        "componentId": "COMP-020",
        "title": "GaN Fast-Charging Power IC Thermal Drift Bulletin",
        "severity": "medium",
        "status": "contained",
        "affectedBatch": "BATCH-2026-GAN09",
        "reportedDate": "2026-09-04",
        "reason": "Thermal dissipation sensor logged a 4.2 deg C spike during continuous 65W charging cycles.",
        "actionRequired": "Updated firmware thermal-throttle threshold to 62W across affected wireless charger units.",
        "supplierId": "SUP-008"
    },
    {
        "id": "REC-003",
        "recallCode": "QC-2026-GEAR-03",
        "componentId": "COMP-012",
        "title": "Precision Brass Bevel Gear Backlash Micro-Jitter",
        "severity": "low",
        "status": "resolved",
        "affectedBatch": "BATCH-2026-BRS18",
        "reportedDate": "2026-08-19",
        "reason": "Microscopic tooth backlash measured at 0.045mm instead of the specified 0.020mm in early production run.",
        "actionRequired": "Re-milled tooth profile on 4th axis CNC; all inventory retrofitted with shims.",
        "supplierId": "SUP-002"
    },
    {
        "id": "REC-004",
        "recallCode": "QC-2026-SEAL-04",
        "componentId": "COMP-017",
        "title": "Silicone Micro-Gasket Thermal Rating Warning",
        "severity": "low",
        "status": "monitoring",
        "affectedBatch": "BATCH-2026-SIL99",
        "reportedDate": "2026-11-01",
        "reason": "Long-term exposure testing showed minor elasticity reduction above 135 deg C after 400 continuous steam cycles.",
        "actionRequired": "Updated care manual documentation recommending hand-washing rather than autoclave sanitation.",
        "supplierId": "SUP-011"
    },
    {
        "id": "REC-005",
        "recallCode": "QC-2026-OPT-05",
        "componentId": "COMP-009",
        "title": "Achromatic Lens Peripheral Dispersion Advisory",
        "severity": "medium",
        "status": "investigation_active",
        "affectedBatch": "BATCH-2026-OPT12",
        "reportedDate": "2026-10-28",
        "reason": "Edge refraction index variance detected in secondary flint glass element causing subtle purple fringing.",
        "actionRequired": "Optical re-alignment required during microscope assembly QA step.",
        "supplierId": "SUP-012"
    }
]
