---
protocol_id: OP-PIPELINE-BUILD
version: 1.0.0
status: ACTIVE
date_created: 2026-03-03
date_modified: 2026-03-03
---
# Operational Protocol: Development Pipeline (OP-PIPELINE-BUILD)

**Purpose:** To define the mandatory stages and templates for high-density agentic development.

## 1. Global Project Context (Mandatory)

Every iteration MUST ingest and update the following context:
- Project Name / Project Root Path.
- Virtual Env Path / Log File Path.
- Overall Goal / Current Architecture Summary.
- Last Major Change.

## 2. Pipeline Stages & Templates

### Stage 0: Requirements & Planning
- **Goal:** Capture complete requirements, skill gaps, and success metrics.
- **Mandate:** Define non-functional requirements and feasibility before any code.
- **Mandate:** Verify that all required state manifests (e.g., `MANIFEST_STATE.json`) have been initialized pursuant to `OP-TERMINAL-WORKFLOW`.

### Stage 1: Code Structure & Style
- **Goal:** Ensure modularity and adherence to "Ventilated Prose" guidelines.
- **Mandate:** Eliminate style violations and monolithic file structures early.

### Stage 2: Functional Correctness
- **Goal:** Verify behavior against intended requirements.
- **Mandate:** Identify requirement gaps and provide corrected logic.

### Stage 3: Debugging & Repair
- **Goal:** Diagnose and fix targeted bugs using reproduction steps.
- **Mandate:** Trace actual vs. expected behavior explicitly.

### Stage 4: Security Audit
- **Goal:** Identify vulnerabilities and data handling gaps.
- **Mandate:** Perform mandatory threat modeling on sensitive modules.

### Stage 5: Testing Strategy
- **Goal:** Implement unit, integration, and edge-case tests.
- **Mandate:** Define isolated test types and verify execution.

### Stage 6: Optimization
- **Goal:** Identify bottlenecks and improve token/compute efficiency.
- **Mandate:** Compute delta metrics (before/after) for hot paths.

### Stage 7: Documentation & Maintainability
- **Goal:** Add docstrings and architectural notes.
- **Mandate:** Ensure README and protocol files are synchronized.

### Stage 8: Integration Review
- **Goal:** Ensureglobal architectural consistency.
- **Mandate:** Verify dependency handoffs across the pipeline.

*Ventilated Prose Enforced | Protocol: OP-PIPELINE-BUILD*
