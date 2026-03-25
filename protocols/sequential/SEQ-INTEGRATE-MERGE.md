---
protocol_id: SEQ-INTEGRATE-MERGE
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent, Deployment_Agent
assigned_role: System
purpose: Oversee and validate the atomic transactional merger of agentic substrates across workspaces, preventing path drift and ensuring zero-downtime structural rollout.
version: 1.2.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Sequential Protocol: Atomic Substrate Merger (SEQ-INTEGRATE-MERGE)

## 1. Core Function & Rationale
This protocol serves as the senior anchor for all substrate environment transitions. It prevents live-system breakage and "Path Drift" by enforcing atomic transactional merges, mandatory shadow-instance validation, and global path normalization.

## 2. Universal Logic Frame (USL)

### Phase 1: Stage Initialization
- YOU MUST establish the "Orchestration Frame" by verifying the presence of senior logic anchors (UAL, USL, UOL).
- YOU MUST verify that [SEQ-PREASSIM-RECON](file:///home/jwils/.blueprints/governance/protocols/sequential/SEQ-PREASSIM-RECON.md) has successfully completed.
- YOU MUST initialize the `ROLLBACK_BUFFER` with the current stable state of target files.
- YOU MUST initialize `SEQUENCE_MEMORY` with legacy and target path patterns for normalization.

### Phase 2: Multi-Stage Execution
- **Step 1: Staged Shadow-Merge & Normalization:**
  - YOU MUST execute a shadow-instance merge to identify structural conflicts.
  - YOU MUST execute absolute-to-relative path normalization across all artifacts in the buffer.
- **Step 2: Dependency & Gating Verification:**
  - YOU MUST verify that all internal markdown links and file references exist in the target root.
  - YOU MUST explicitly wrap new logic in feature-flags where applicable.
- **Step 3: Atomic Lock & Commit:**
  - YOU MUST transition the normalized shadow-merge to the live substrate in a single atomic transaction.
  - YOU MUST update `MANIFEST_STATE.json` to reflect the new absolute project root.
- YOU MUST update `SEQUENCE_MEMORY` upon completion of the transaction.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST generate and commit a "Standardized Merge Context Report" to the `docs/` directory.
- YOU MUST execute a "Final Integrity Audit" (via `OPS-RISK-AUDIT`) on the merged substrate and manifest.
- YOU MUST purge shadow-instances, staging caches, and ad-hoc mapping notes.
- **Rollback Policy:** IF post-merge audit fails, YOU MUST trigger the immediate rollback guarantee utilizing the `ROLLBACK_BUFFER`.

## 3. Human Gate & State Handoff
- **Condition:** If the environment is mathematically constrained or carries a `CRITICAL` risk flag.
- **Instruction:** YOU MUST enforce an overriding human-in-the-loop manual flag before final commit.
- **Handoff:** Upon successful cleanup, pass the final report to the `Orchestrator_Agent` to trigger a final `SEQ-SUBSTRATE-ASSIMILATE` pass.

---
