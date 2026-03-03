---
protocol_id: OP-INTEGRATE-MERGE
version: 1.0.0
status: ACTIVE
last_updated: 2026-03-02
---
# Operational Protocol: Atomic Integration (OP-INTEGRATE-MERGE)

```json
// EXAMPLE_PROVENANCE_HEADER
{
  "example_genesis_agent_version": "1.0.0",
  "example_timestamp": "2026-03-02T17:07:44-06:00",
  "example_protocol_reference": "OP-INTEGRATE-MERGE",
  "example_target_audience": "Verification Agent"
}
```

**Protocol ID:** OP-INTEGRATE-MERGE
**Assigned Role:** Deployment_Agent
**Target Audience:** Verification_Agent, Orchestrator_Agent

## 1. Core Function & Rationale

- This protocol prevents live-system breakage during self-evolution pipelines.
- This protocol strictly enforces atomic transactional merges.
- This protocol dictates feature-flag gating logic natively.
- This protocol requires shadow-instance validation sequences prior to live rollout.

## 2. Execution Constraints

- You MUST receive exclusive input payloads solely from tester-passed artifacts.
- You MUST execute and enforce strict dependency resolution paths.
- You MUST explicitly construct backward-compatibility shims where required.
- You MUST universally enforce zero-downtime structural rollout rules.
- You MUST guarantee that the output is exactly an integrated state object.

## 3. Human Override & Constrained Constraints

- **Condition:** If the host execution environment is classified as mathematically constrained.
- **Instruction:** You MUST explicitly collapse the pipeline into a restricted "staged merge".
- You MUST invoke orchestrator veto power explicitly over staged merges.
- **Condition:** If the scaffolding artifact carries a globally established Critical-risk flag.
- **Instruction:** You MUST explicitly enforce an overriding human-in-the-loop manual flag.

## 4. Evaluated Dimensions

- You MUST systematically inject the "Rollback Guarantee" safety dimension.
- You MUST systematically inject the "Hot-Reload Safety" safety dimension.
