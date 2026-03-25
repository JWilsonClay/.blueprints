---
protocol_id: OPS-GRAPH-GEN
structure_status: HARDENED
target_audience: Planning_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic tool for generating executable dependency graphs and resolving circular logic.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Graph Generation (OPS-GRAPH-GEN)

## 1. Core Function & Rationale
This protocol converts a flat task list into a non-linear, executable dependency graph, identifying critical paths and parallelization opportunities.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify the presence of a `TASK_MANIFEST_DRAFT` with unique Stage IDs.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST verify that all task targets exist in the `MANIFEST_STATE.json`.

### Phase 2: Tool/Script Execution
- YOU MUST invoke `toolkits/dependency/graph_engine.py` to detect and resolve circular dependencies.
- YOU MUST establish "Critical Handoff Locks" for sequential tasks.

### Phase 3: Rigid Output Emission
- YOU MUST output the final `TASK_DEPENDENCY_GRAPH.json`.
- YOU MUST prefix all node instructions with the required `atomic/` protocol pointers.

---
