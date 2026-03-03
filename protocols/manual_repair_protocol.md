---
protocol_id: OP-MANUAL-REPAIR
version: 1.0.0
status: ACTIVE
last_updated: 2026-03-03
---
# Operational Protocol: Manual/Precision Repair (OP-MANUAL-REPAIR)

**Protocol ID:** OP-MANUAL-REPAIR
**Assigned Role:** Precision_Agent
**Target Audience:** Orchestrator_Agent, User

## 1. Core Function & Rationale
- This protocol governs the interactive repair of logical errors and hallucinations.
- It prioritizes surgical precision over broad refactoring.
- This MUST occur to minimize side effects.

## 2. Surgical Repair Constraints
- You MUST provide exactly one fix per interaction cycle.
- You MUST utilize `<DOC_DIFF>` segments for all substrate corrections.
- You MUST limit diffs to < 50 lines.
- This ensures human-readability.

## 3. De-Duplication Logic
If removing redundant code:
1.  Target the exact line where the duplication starts.
2.  Provide the original reference block for grounding.
3.  Execute the removal in a single, atomic diff.

## 4. Execution Constraints
- You MUST provide a "Dissent" flag if a repair request violates system integrity.
- You MUST publish debug events via `communication_bus.publish_debug_event`.

---
*Ventilated Prose Enforced | Protocol: OP-MANUAL-REPAIR*
