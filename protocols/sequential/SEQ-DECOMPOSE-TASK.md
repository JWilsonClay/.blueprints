---
protocol_id: SEQ-DECOMPOSE-TASK
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Decompose architectural stages into atomic, executable implementation tasks.
version: 1.2.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Sequential Protocol: Task Decomposition (SEQ-DECOMPOSE-TASK)

## 1. Core Function & Rationale
This protocol coordinates the breakdown of complex architectural objectives into atomic tasks. It follows the **Pure Orchestration** model, delegating all implementation logic to the `atomic/` layer.

## 2. Universal Logic Frame (USL)

### Phase 1: Stage Initialization
- YOU MUST establish the "Orchestration Frame" by ingesting logic anchors: UOL, USL, and UAL.
- YOU MUST explicitly compare `date_created` stamps of the target specification against the substrate manifest; Seniority defines the truth anchor.
- [OPS-INPUT-INIT](file:///home/jwils/.blueprints/governance/protocols/atomic/OPS-INPUT-INIT.md) -- Purpose: Atomic tool for substrate state ingestion and manifest verification.

### Phase 2: Multi-Stage Execution

- **Step 1: Task Atomicization**
  - [OPS-DOC-CAPTURE](file:///home/jwils/.blueprints/governance/protocols/atomic/OPS-DOC-CAPTURE.md) -- Purpose: Segment architectural stages and extract technical prompts for the `Genesis_Agent`.
  
- **Step 2: Dependency Resolution & Graphing**
  - [OPS-GRAPH-GEN](file:///home/jwils/.blueprints/governance/protocols/atomic/OPS-GRAPH-GEN.md) -- Purpose: Identify circular dependencies and generate the final executable `TASK_DEPENDENCY_GRAPH.json`.

- **Step 3: Verification Check**
  - [OPS-RISK-AUDIT](file:///home/jwils/.blueprints/governance/protocols/atomic/OPS-RISK-AUDIT.md) -- Purpose: Perform a hallucination and grounding sweep on the newly generated task manifest.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST update the `MANIFEST_STATE.json` with the path to the final `TASK_DEPENDENCY_GRAPH.json`.
- YOU MUST perform "Substrate Hygiene" by purging transient scratch notes or draft manifests.

---
