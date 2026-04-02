---
protocol_id: SEQ-SUBSTRATE-MAINTAIN
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent, Genesis_Agent
assigned_role: System
purpose: Orchestrate the global maintenance cycle (Recon, Hygiene, Assimilation) for documentation and substrate artifacts.
version: 1.0.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Sequential Protocol: Substrate Maintenance Orchestration (SEQ-SUBSTRATE-MAINTAIN)

## 1. Core Function & Rationale
This protocol provides a standardized "Total Clean" workflow for the `docs/` directory and substrate-level artifacts. It ensures that no artifact is modified or purged without diagnostic reconnaissance and empirical verification.

## 2. Universal Logic Frame (USL)

### Phase 1: Stage Initialization
- YOU MUST establish the "Orchestration Frame" by ingesting logic anchors: UOL, USL, and UAL.
- YOU MUST verify the active inventory of the `docs/` and `governance/` directories.
- YOU MUST initialize `MAINTENANCE_MEMORY` to track the state across the three internal sequences.

### Phase 2: Multi-Stage Execution
- **Step 1: Diagnostic Gate (RECON):**
  - YOU MUST execute [SEQ-PREASSIM-RECON](file:///home/jwils/.blueprints/governance/protocols/sequential/SEQ-PREASSIM-RECON.md).
  - IF `RECON` returns `GATE_BLOCKED`, YOU MUST immediately ABORT and notify the Orchestrator.
- **Step 2: Logic Absorption (ABSORB):**
  - YOU MUST execute [SEQ-SUBSTRATE-ABSORB](file:///home/jwils/.blueprints/governance/protocols/sequential/SEQ-SUBSTRATE-ABSORB.md).
  - This cycle proactively moves unique knowledge from `docs/` into permanent Blueprints.
- **Step 3: Lifecycle Purge (HYGIENE):**
  - YOU MUST execute [SEQ-SUBSTRATE-HYGIENE](file:///home/jwils/.blueprints/governance/protocols/sequential/SEQ-SUBSTRATE-HYGIENE.md).
  - This cycle identifies and archives artifacts that have converged with the implementation.
- **Step 4: Structural Hardening (ASSIMILATE):**
  - YOU MUST execute [SEQ-SUBSTRATE-ASSIMILATE](file:///home/jwils/.blueprints/governance/protocols/sequential/SEQ-SUBSTRATE-ASSIMILATE.md).
  - This cycle reformats permanent senior documentation artifacts to UPH/UAL standards.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST execute a "Final Integrity Audit" (via `OPS-RISK-AUDIT`) on the `docs/HYGIENE_SUMMARY.json`.
- YOU MUST update the `Global_Protocol_Inventory.md` if any changes to the maintenance logic were implemented.
- YOU MUST purge temporary state payloads from `MAINTENANCE_MEMORY`.

## 3. Policy Reference
- This protocol implements the "Tiered Maintenance Pattern" established in the `assimilation_effectiveness_report.md`.
- Precedence: Senior artifacts (lowest date_created) are the templates for all reformatting.

---
