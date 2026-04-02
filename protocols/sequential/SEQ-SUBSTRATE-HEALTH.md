---
protocol_id: SEQ-SUBSTRATE-HEALTH
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: Verification_Agent
purpose: Orchestrate directory-level health assessments against Universal Logic standards (UAL, UOL, USL) and trigger substrate repairs.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Sequential Protocol: Substrate Health Orchestration (SEQ-SUBSTRATE-HEALTH)

## 1. Core Function & Rationale
This workflow governs the periodic health check of the core directories (`roles/`, `protocols/atomic/`, `protocols/sequential/`) to ensure long-term architectural integrity.

## 2. Universal Logic Frame (USL)

### Phase 1: Stage Initialization
- YOU MUST establish the "Orchestration Frame" by ingesting the three Logic Anchors: UAL, UOL, and USL.
- YOU MUST verify the target directory path and initialize the `HEALTH_MEMORY` buffer.
- YOU MUST explicitly explain the reason for any sequence pause to the USER (Transparency Mandate).

### Phase 2: Multi-Stage Execution
- **Step 1: Workspace Benchmark Audit:** 
  - YOU MUST execute `OPS-RISK-AUDIT` against all target artifacts in scope (e.g., `roles/`, `protocols/`).
  - YOU MUST extract seniority data from UPH headers to establish an audit sequence.
- **Step 2: Redundancy & Bloom Audit:** 
  - YOU MUST scan the protocol library for overlapping logic domains and "Logic Bloat."
- **Step 3: Seniority Audit:** YOU MUST evaluate junior artifacts against "Ancient Anchors."
- **Step 4: Findings Aggregation & Merge Feasibility:**
  - YOU MUST aggregate all findings into a unified `SUBSTRATE_HEALTH_REPORT.json`.
  - YOU MUST identify candidates for "Seniorization" (Merging Junior to Senior).
- **Step 5: Remediation Trigger & Recursive Hygiene:**
  - IF `CRITICAL/HIGH` findings exist: YOU MUST trigger `SEQ-SUBSTRATE-ASSIMILATE` or `SEQ-SUBSTRATE-MAINTAIN`.
  - YOU MUST identify the source Recommendation or Gap Report artifact that triggered this remediation.
  - UPON SUCCESSFUL IMPLEMENTATION: YOU MUST immediately trigger `SEQ-SUBSTRATE-HYGIENE` archival for the source artifact.
- YOU MUST update `MANIFEST_STATE.json` at every stage transition.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST execute a "Final Integrity Audit" (via `OPS-RISK-AUDIT`) on the generated JSON and MD reports.
- YOU MUST perform "Substrate Hygiene" by purging temporary audit state files.
- **Remediation Trigger:** YOU MUST pass the `SUBSTRATE_HEALTH_REPORT.json` to the `Orchestrator_Agent` for automated reformatting.

## 3. Transparency Mandate
- YOU MUST explicitly broadcast the reason for the sequence pause (e.g., "Sequence pausing for mandatory Human-in-the-Loop verification") to prevent misinterpretation of termination as a failure.

---
