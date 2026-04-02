---
protocol_id: OPS-TEST-EXEC
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic protocol for sandboxed execution of test suites.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Test Execution (OPS-TEST-EXEC)

## 1. Core Function & Rationale
This protocol executes deterministic statistical test suites within isolated environments to gather raw performance and reliability data.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify and ingest all required test suite parameters.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST verify the presence of a `CANDIDATE_ARTIFACT` and `AGENTIC_SEED`.

### Phase 2: Tool Execution
- YOU MUST initialize the environment using `toolkits/dependency/testing_sandbox.py`.
- YOU MUST execute the test battery using `toolkits/audit_onboarding/auto_test_generator.py`.

### Phase 3: Rigid Output Emission
- YOU MUST emit the raw test logs and variance metrics in JSON format.
- **Orchestrational Transparency:** All calls MUST include the purpose summary from the YAML header.

---
