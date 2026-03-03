---
protocol_id: OP-DISCOVER-INTENT
version: 1.0.0
status: ACTIVE
last_updated: 2026-03-03
---
# Operational Protocol: Intent Discovery (OP-DISCOVER-INTENT)

**Protocol ID:** OP-DISCOVER-INTENT
**Assigned Role:** Intake_Agent
**Target Audience:** Planning_Agent, Orchestrator_Agent

## 1. Core Function & Rationale
- This protocol transforms vague user intentions into structured, machine-readable project manifests.
- It prevents architectural drift by enforcing a strict requirement-harvesting phase.

## 2. Requirement Harvesting (The 7 Pillars)
You MUST ask exactly 5-7 technical questions covering:
1.  **Tech Stack**: Languages, frameworks, and versions.
2.  **Persistence**: Databases, local storage, or cloud state.
3.  **Interface**: CLI, Web, GUI, or API-only.
4.  **Scaling**: Performance expectations and user load.
5.  **Environment**: Infrastructure, OS, and local constraints.
6.  **Security**: PII handling, authentication, and compliance.
7.  **Success Criteria**: Explicit definition of "Done".

## 3. Manifest Initialization
- You MUST generate a `MANIFEST_STATE.json` upon completion of harvesting.
- You MUST strictly follow the schema defined in `OP-CORE-COMP`.

## 4. Execution Constraints
- You MUST wait for explicit user verification before handing off to the Planning_Agent.
- You MUST publish the discovery broadcast via `communication_bus.publish_discovery`.

---
*Ventilated Prose Enforced | Protocol: OP-DISCOVER-INTENT*
