---
protocol_id: SEQ-PRECISION-SURGERY
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Govern the repair of deep, substrate regressions under methodical constraints.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Sequential Protocol: Precision Surgery (SEQ-PRECISION-SURGERY)

## 1. Core Function & Rationale
This protocol governs the repair of deep, substrate regressions. It operates under a "Slow and Methodical" constraint to ensure zero side effects.

## 2. Universal Logic Frame (USL)

### Phase 1: Stage Initialization
- YOU MUST isolate the target delta to exactly one artifact.
- YOU MUST establishes the "Orchestration Frame" by running the full regression suite pursuant to `OPS-TEST-VALIDATE`.
- YOU MUST initialize the `SURGERY_MEMORY` with a snapshot of the current established logic.

### Phase 2: Multi-Stage Execution
- **Step 1: Surgical Refactor:** YOU MUST apply the minimal patch defined by `OPS-MANUAL-REPAIR`.
- **Step 2: Regression Audit:** YOU MUST re-run the `OPS-TEST-VALIDATE` suite to verify zero side-effects.
- **Step 3: Integrity Validation:** YOU MUST execute `OPS-RISK-AUDIT` on the modified artifact.
- YOU MUST update `MANIFEST_STATE.json` after successful verification.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST generate and commit the "Surgical Intervention Log" in ventilated prose.
- YOU MUST purge temporary patches and staging snapshots.
- **Rollback Policy:** IF regression is detected, YOU MUST trigger the immediate rollback guarantee via `SEQ-INTEGRATE-MERGE`.

## 3. Escalation
- YOU MUST escalate to human oversight after exactly 3 failed surgical attempts on the same artifact.

---
