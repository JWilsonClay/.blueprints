---
protocol_id: OPS-EVAL-MEASURE
structure_status: HARDENED
target_audience: Verification_Agent, Orchestrator_Agent
assigned_role: System
purpose: Atomic tool for running runtime benchmarks and capability delta analyses.
version: 1.1.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Benchmark Evaluation (OPS-EVAL-MEASURE)

## 1. Core Function & Rationale
This protocol answers the objective question of whether the substrate improved agentic capability by running standardized runtime benchmarks and delta analyses.

## 2. Universal Logic Frame (UOL)

### Phase 1: Input Validation
- YOU MUST verify that all required metric parameters are present.
- YOU MUST explicitly compare `date_created` strings of all merge or override candidates; the Senior artifact (oldest date) MUST be the implementation target.
- **Birthdate Authority:** The `date_created` field MUST be derived from the automated filesystem metadata (via `OPS-YAML-CREATED`).
- YOU MUST verify that `INTEGRATED_STATE_ARTIFACTS` are present.
- YOU MUST verify that a `BASELINE_METRIC_REPORT` exists for comparison.
- YOU MUST specify the audit tier (File-Level or Workspace-Level).

### Phase 2: Tool/Script Execution
- **Benchmark Execution:** YOU MUST invoke `toolkits/dependency/benchmark_evaluator.py` to parse Delta metrics and compute Pareto-fronts.
- YOU MUST analyze success rate, token efficiency, safety violation rate, and autonomy index.
- YOU MUST identify "Pareto Impact" and "Novelty Detection" dimensions.
- YOU MUST rigorously flag any detected regressions immediately.

### Phase 3: Rigid Output Emission
- YOU MUST compute a structured quantitative impact report.
- YOU MUST supply the quantitative report directly to `SEQ-ORCHESTRATE-META.md`.
- IF regression is detected, YOU MUST tag metadata with "REGRESSION" and trigger a `RESTART_PIPELINE` signal.

## 3. Atomic Error Handling
- **Failure:** If benchmark execution fails, emit `METRIC_FAILURE.json` with clear environment diagnostic logs.
- **Recovery:** Roll back to the baseline state and notify the `Verification_Agent`.

---
