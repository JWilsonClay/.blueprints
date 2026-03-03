---
protocol_id: OP-DECOMPOSE-TASK
version: 1.0.0
status: ACTIVE
date_created: 2026-03-03
date_modified: 2026-03-03
---
# Operational Protocol: Task Decomposition (OP-DECOMPOSE-TASK)

**Protocol ID:** OP-DECOMPOSE-TASK
**Assigned Role:** Planning_Agent
**Target Audience:** Genesis_Agent, Orchestrator_Agent

## 1. Core Function & Rationale
- This protocol decomposes architectural stages into atomic, executable implementation tasks.
- It ensures dependency graph integrity.
- This MUST occur before the Genesis_Agent begins generation.

## 2. Decomposition Logic
- You MUST ingest `MANIFEST_STATE.json` and current substrate status.
- You MUST break stages into tasks utilizing the "Stage #.#.#" title format.
- You MUST identify and resolve circular dependencies in the task sequence.

## 3. Task Metadata
Every task MUST include:
1.  **Identifier**: Unique Stage ID.
2.  **Priority**: High, Medium, or Low.
3.  **Target**: Specific files or directories.
4.  **Prompt**: Explicit, technical instructions for the `Genesis_Agent`.

## 4. Execution Constraints
- You MUST publish the execution sequence via `communication_bus.publish_sequence`.
- You MUST provide the Orchestrator with a valid dependency graph payload.

---
*Ventilated Prose Enforced | Protocol: OP-DECOMPOSE-TASK*
