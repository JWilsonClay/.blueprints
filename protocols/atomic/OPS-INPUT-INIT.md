---
protocol_id: OPS-INPUT-INIT
structure_status: HARDENED
target_audience: Planning_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic tool for environment state ingestion and project root verification.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Input Initialization (OPS-INPUT-INIT)

## 1. Core Function & Rationale
This protocol initiates the agentic context by verifying and ingesting the substrate state, ensuring a stable foundation for downstream orchestration.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify the presence of a valid `MANIFEST_STATE.json` in the substrate root.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST dissent if the directory scope is ambiguous.

### Phase 2: Tool/Script Execution
- YOU MUST invoke `toolkits/dependency/state_ingestor.py` to index current artifact locations.
- YOU MUST verify all senior protocol headers (UPH) for the active task scope.

### Phase 3: Rigid Output Emission
- YOU MUST emit a `SUBSTRATE_STATE_OBJECT` containing the project root, agent manifests, and dependency pointers.
- YOU MUST update the `MANIFEST_STATE.json` lifecycle to `INGESTED`.

---
