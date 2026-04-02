---
protocol_id: OPS-DISCOVER-INTENT
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic protocol for transforming intent into structured project manifests within the substrate.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Intent Discovery (OPS-DISCOVER-INTENT)

## 1. Core Function & Rationale
This protocol transforms user agentic intent into structured, machine-readable project manifests and prevents architectural drift by enforcing a strict requirement-harvesting phase.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify that all required input strings are present in the context.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST verify the presence of the `INITIAL_INTENT` string from the USER.
- YOU MUST verify that the `MANIFEST_STATE.json` anchor path is accessible.
- IF intent is ambiguous, YOU MUST dissent and request clarification before proceeding.

### Phase 2: Tool/Script Execution
- **Requirement Harvesting:** YOU MUST ask exactly 5-7 technical questions covering Tech Stack, Persistence, Interface, Scaling, Environment, Security, and Success Criteria.
- **Manifest Initialization:** YOU MUST generate or update the `MANIFEST_STATE.json` upon completion of harvesting.
- YOU MUST strictly follow the schema defined in `SEQ-SUBSTRATE-COMP`.
- YOU MUST prefix all terminal commands with `timeout` as per `OPS-TERMINAL-WORKFLOW`.

### Phase 3: Rigid Output Emission
- YOU MUST publish the discovery broadcast via `communication_bus.publish_discovery`.
- YOU MUST emit the final `MANIFEST_STATE.json` strictly for ingestion by the `Orchestrator_Agent`.
- **Handoff:** Generate a "Stage 1.0" handoff directive for the `Planning_Agent`.

## 3. Atomic Error Handling
- **Failure:** If harvesting is interrupted, emit `FAILURE_REPORT.json` and preserve current intent draft.
- **Recovery:** RE-invoking this protocol restores state from the last saved `MANIFEST_STATE.json`.

---
