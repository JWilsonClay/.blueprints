---
protocol_id: SEQ-PIPELINE-BUILD
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Define the mandatory stages and templates for high-density agentic development.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Sequential Protocol: Development Pipeline (SEQ-PIPELINE-BUILD)

## 1. Core Function & Rationale
This protocol defines the mandatory stages and templates for development iterations, ensuring consistency from requirements to deployment.

## 2. Universal Logic Frame (USL)

### Phase 1: Stage Initialization
- YOU MUST ingest global project context: Project Name, Root Path, Venv Path, and Log Path.
- YOU MUST verify that all required manifests (e.g., `MANIFEST_STATE.json`) are initialized.
- YOU MUST initialize the `STAGE_MEMORY` to track progression from Stage 0 to 8.

### Phase 2: Multi-Stage Execution
- **Step 0: Requirements & Planning:** Capture skill gaps and success metrics.
- **Step 1: Code Structure & Style:** Eliminate style violations early.
- **Step 2: Functional Correctness:** Verify behavior against intended requirements.
- **Step 3: Debugging & Repair:** Fix targeted bugs using reproduction steps.
- **Step 4: Security Audit:** Perform threat modeling on sensitive modules.
- **Step 5: Testing Strategy:** Implement unit, integration, and edge-case tests.
- **Step 6: Optimization:** Compute delta metrics (before/after) for hot paths.
- **Step 7: Documentation:** Synchronize README and protocol files.
- **Step 8: Integration Review:** Ensure global architectural consistency.
- YOU MUST update `MANIFEST_STATE.json` after the completion of each stage.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST execute a "Final Integrity Audit" (via `OPS-RISK-AUDIT`) on the integrated pipeline.
- YOU MUST perform "Substrate Hygiene" by purging temporary Stage-level artifacts.
- YOU MUST emit the final "Hardened" status signal to the `Deployment_Agent`.

---
