---
protocol_id: OP-PRECISION-PRECISE
version: 1.0.0
status: ACTIVE
date_created: 2026-03-03
date_modified: 2026-03-03
---
# Operational Protocol: Precision Surgery (OP-PRECISION-PRECISE)

**Assigned Role:** Precision_Agent
**Target Audience:** Verification_Agent, Orchestrator_Agent

## 1. Core Mandate
- This protocol governs the repair of deep, substrate regressions.
- It operates under a "Slow and Methodical" constraint.
- This ensures zero side effects.

## 2. Surgical Workflow
1.  **Lock State**: Isolate the target delta to exactly one file.
2.  **Pre-Audit**: Run the full regression suite pursuant to `OP-TEST-VALIDATE`.
3.  **Surgical Edit**: Apply the minimal possible patch.
4.  **Post-Audit**: Re-run the regression suite to verify zero side effects.

## 3. Rollback Policy
- You MUST trigger an immediate rollback on any regression detection.
- You MUST execute rollbacks strictly according to `OP-INTEGRATE-MERGE` logic.
- You MUST escalate to human oversight after 3 failed attempts.

## 4. Output Deliverables
- You MUST generate a "Surgical Intervention Log" in ventilated prose.
- You MUST embed this log into the `Exhaustive Gap Report`.

---
*Ventilated Prose Enforced | Protocol: OP-PRECISION-PRECISE*
