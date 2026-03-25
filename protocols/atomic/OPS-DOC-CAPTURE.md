---
protocol_id: OPS-DOC-CAPTURE
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic tool for auto-generating ADRs, API specifications, and architectural graphs.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Knowledge Capture (OPS-DOC-CAPTURE)

## 1. Core Function & Rationale
This protocol ensures long-term maintainability through the auto-generation of Architecture Decision Records (ADRs), API specifications, visual graphs, and contextual annotations.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify that all required context parameters are present.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST verify the presence of `REFINEMENT_RATIONALE` or `AUDIT_REPORT` in the context.
- YOU MUST verify the target documentation directory exists and is writable.
- YOU MUST anchor documentation to a specific `protocol_id` or `role_id`.

### Phase 2: Tool/Script Execution
- **Knowledge Synthesis:** YOU MUST invoke `toolkits/dependency/documentation_generator.py` to synchronize ADRs and specifications.
- **Visualization:** YOU MUST invoke `toolkits/audit_onboarding/dependency_visualizer.py` to generate visual graphs.
- YOU MUST execute concurrently with substrate merge logic.
- YOU MUST rigidly obey the "Ventilated Prose" and "Fenced-Block Isolation" rules.

### Phase 3: Rigid Output Emission
- YOU MUST emit synchronized declarative artifacts directly alongside substrate merges.
- YOU MUST include the `protocol_id`, standard semantic versioning (vX.X.X), and an explicit "Change Log" in every file.
- YOU MUST provide the companion `_eval.md` file for every generated artifact.

## 3. Atomic Error Handling
- **Failure:** If documentation generation fails, emit a `DOC_SYNC_ERROR.json` and flag the merge as "UNSTABLE".
- **Recovery:** Retry with a narrower scope (one file at a time) if global generation times out.

---
