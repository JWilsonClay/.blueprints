---
protocol_id: OPS-TOC-SYNC
structure_status: DRAFT
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: Verification_Agent
purpose: Synchronize and condense SUBSTRATE_HISTORY_TOC.md based on Provenance_Log entries.
version: 1.0.0
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: TOC Synchronization (OPS-TOC-SYNC)

## 1. Core Function
Ensures that the `SUBSTRATE_HISTORY_TOC.md` remains a current, human-readable map of the `substrate_history.db`. It enforces high-density summaries by grouping repetitive sequences.

## 2. Execution Frame
### Phase 1: Data Extraction
- Query `Provenance_Log` for the latest ID range.
- Extract `id`, `agent_role`, `action_type`, and `rationale`.

### Phase 2: Condensation Logic
- GROUP entries where `agent_role`, `action_type`, and `rationale` (summarized) are identical in sequence.
- FORMAT as: `[START_ID]-[END_ID]: [SUMMARY]`.

### Phase 3: Committal
- OVERWRITE `SUBSTRATE_HISTORY_TOC.md`.
- LOG the sync event in `substrate_history.db` as a `TOC_SYNC` action.

## 3. Automation Anchor
- This protocol is triggered by the [BEH-LEDGER-SYNC-01.yaml](file:///home/jwils/.blueprints/governance/behaviors/BEH-LEDGER-SYNC-01.yaml) behavioral hook.
