---
protocol_id: OPS-OPTIMIZE-TUNE
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent, Genesis_Agent
assigned_role: System
purpose: Authoritative senior anchor for performance optimization and token-reduction.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Performance Optimization (OPS-OPTIMIZE-TUNE)

## 1. Core Function & Rationale
This protocol explicitly prevents unsustainable compute bloat by proposing and applying structural token-reduction refactors and strategic parallelization.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify and ingest all required metrics and logs.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST verify the presence of `EVALUATOR_METRICS` and `RUNTIME_LOGS`.
- YOU MUST verify that the target context window utilization is >= 80% if triggering a summarization layer.
- YOU MUST specify the "Auto-Reject" threshold for critical-risk alterations.

### Phase 2: Tool/Script Execution
- **Optimization Strategy:** YOU MUST invoke `toolkits/dependency/performance_optimizer.py` to automate code-segment parallelization.
- **Complexity Baselining:** YOU MUST invoke `toolkits/audit_onboarding/codebase_analyzer.py` before optimization.
- YOU MUST implement a mandatory summarization layer if the combined prompt exceeds 80% of the window.
- YOU MUST identify and prune redundant or low-priority tokens.

### Phase 3: Rigid Output Emission
- YOU MUST output structural interventions within `<OPTIMIZATION_DIFF>` XML blocks.
- YOU MUST supply an "Efficiency vs. Robustness Trade-off Matrix" and a "Regression Risk Score".
- YOU MUST forward optimized artifacts strictly to be re-audited and re-tested.

## 3. Atomic Error Handling
- **Failure:** IF optimization degrades robustness attributes, YOU MUST automatically reject the change and notify the `Genesis_Agent`.
- **Recovery:** Re-evaluate the Pareto-front using updated baseline metrics.

---
