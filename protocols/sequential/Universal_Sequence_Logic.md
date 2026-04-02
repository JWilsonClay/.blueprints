---
protocol_id: N/A (Standard Anchor)
structure_status: CANONICAL
target_audience: All Agent Roles
assigned_role: System Architecture
purpose: Define the universal frontmatter and structural metadata standards for 
  sequential workflows.
behavior_dependencies:
  - "[BEH-UAL-PHASES-01](file:///home/jwils/.blueprints/governance/behaviors/BEH-UAL-PHASES-01.yaml)
    -- Purpose: Operating phase compliance."
protocol_dependencies:
  - "[UAL](file:///home/jwils/.blueprints/governance/roles/Universal_Agent_Logic.md)"
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Standard: Universal Sequence Logic (USL)

---

## 1. Definition of a Sequence (SEQ-XX-XX)

A **Sequential Protocol** is a multi-stage workflow that orchestrates multiple Agent Roles and Operational Protocols to achieve a complex, systemic objective.

### 1.1 workflow Orchestration
- A Sequence MUST coordinate at least two (2) distinct Operations or Decision Gates.
- **Behavioral Ingestion:** Sequences MUST derive their operating phases from [BEH-UAL-PHASES-01](file:///home/jwils/.blueprints/governance/behaviors/BEH-UAL-PHASES-01.yaml) to maintain architectural synchronization.
- It manages the long-term persistence of the `MANIFEST_STATE.json` throughout the pipeline.

## 2. Structural Requirements

Every `SEQ-` protocol MUST adhere to the following workflow hierarchy:

### Phase 1: Stage Initialization
- YOU MUST establish the "Orchestration Frame" by ingesting all senior protocols (UOL, UAL, USL).
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the target anchor.
- YOU MUST initialize the `SEQUENCE_MEMORY` buffer to track state across stages.

### Phase 2: Multi-Stage Execution
- **Atomic Calls:** Every action step in the sequence MUST be an explicit call to a hardened protocol in the `atomic/` directory.
- **Purpose-Mapping Mandate:** Every call MUST be accompanied by a concise summary item derived from the target's YAML `purpose` header to ensure human readability and semantic traceability.
- **Decision Gates:** YOU MUST implement mandatory conditional gates (IF/ELSE) based on `atomic/` output results.
- **Stateful Phase Separation Mandate:** Any logical `Plan/Propose` node MUST hit a deterministic `approval_node` (interrupt) before an `execute_node` can proceed. No read-only agent can pass an execution boundary in the same continuous cycle without an explicit HITL Execution Key.
- **Parallism:** Multi-file operations SHOULD be parallelized where dependency graphs allow.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST execute a "Final Integrity Audit" (via `OPS-RISK-AUDIT`) on all generated outputs.
- YOU MUST perform "Substrate Hygiene" by purging temporary staging files.
- **Recursive Hygiene Mandate:** IF a sequence was triggered by a specific markdown report or gap-report, YOU MUST include an atomic archival command for that source artifact as the final step of Phase 3.
- **Execution Audit & Archival Mandate:** YOU MUST explicitly trigger [SEQ-EXEC-PLAN-AUDIT](file:///home/jwils/.blueprints/governance/protocols/sequential/SEQ-EXEC-PLAN-AUDIT.md) as the final step of any implementation sequence to verify fidelity AND execute the automatic ingestion of converged artifacts into the Ghost Ledger upon 100% success.

## 3. State Preservation & Handoff
- **Integrity Anchor:** The sequence MUST update the `MANIFEST_STATE.json` at every stage transition.
- **Failure Recovery:** YOU MUST implement specific "Checkpoint Fail-Safes" to allow the Orchestrator to resume from the last successful stage.
- **Rollback:** Any critical failure in a stage MUST trigger the `SEQ-INTEGRATE-MERGE` rollback mechanism.

---

## 4. Operational Gating
- A Sequence is not complete until it returns either a "Structural Integrity Clearance" or a "Manual Intervention Request".
- It MUST NOT contain the granular implementation logic of a tool; it delegates that to the `OPS-` layer.
