---
protocol_id: SEQ-PREASSIM-RECON
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent, Genesis_Agent
assigned_role: System
purpose: Perform methodical pre-assimilation reconnaissance and diagnostic of junior substrates.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Sequential Protocol: Pre-Assimilation Reconnaissance (SEQ-PREASSIM-RECON)

## 1. Core Function & Rationale
This protocol mandates a comprehensive diagnostic pass before any junior substrate is absorbed, identifying "Doc-Code Drift" and cataloging "Ghost Features."

## 2. Universal Logic Frame (USL)

### Phase 1: Stage Initialization
- YOU MUST establish the "Orchestration Frame" by identifying the junior source and senior target.
- YOU MUST initialize the `RECON_MEMORY` buffer to capture fragility vectors.
- YOU MUST verify the presence of mandatory diagnostics tools (`assimilation_gate_check.py`).

### Phase 2: Multi-Stage Execution
- **Step 1: Functional Trace:** YOU MUST execute a live verification of running tools and persistence state.
- **Step 2: Drift Assessment:** YOU MUST quantify the structural gap between junior code and senior langgraph-social-agents.
- **Step 3: Fragility Identification:** YOU MUST scan for ad-hoc decoding, missing error recovery, and hardcoded configurations.
- YOU MUST update `MANIFEST_STATE.json` upon completion of the recon report.

### Phase 3: Recursive Refinement (Cleanup)
- YOU MUST generate and commit the "Pre-Assimilation Recon Report" to `docs/`.
- YOU MUST execute the "Gate Validation" check using `assimilation_gate_check.py`.
- YOU MUST purge ad-hoc diagnostic logs and raw tool output dumps.

## 3. Fail-Safe Mechanism
- IF the safety gate returns a `GATE_BLOCKED` signal, YOU MUST immediately ABORT and log a `SEVERITY: FATAL` error.
- **Condition:** If critical ghost-features are detected, YOU MUST dissent and block assimilation until documented.

---
