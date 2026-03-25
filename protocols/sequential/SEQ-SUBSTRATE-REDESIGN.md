---
protocol_id: SEQ-SUBSTRATE-REDESIGN
structure_status: CANONICAL
target_audience: Orchestrator, Verification Agent
assigned_role: System Architecture
purpose: Oversight and execution of a systematic workspace redesign and path-reconciliation.
version: 1.0.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Protocol: SEQ-SUBSTRATE-REDESIGN

## 1. Objective
Establish a high-governance framework for refactoring the substrate's directory structure while maintaining logical continuity, path-traceability, and operational stability.

---

## 2. Phases of Redesign

### Phase 1: Substrate Reconnaissance & Mapping
1.  **Systematic Scan**: YOU MUST perform a deep recursion of the entire workspace to identify all logical clusters (e.g., operational scripts, langgraph-social-agent archives, toolkit modules).
2.  **Path Detection**: YOU MUST itemize all "Hardcoded Anchors"—lines in scripts, protocols, or configs that reference absolute or relative paths.
3.  **Conflict Identification**: Detect duplicate directory names (e.g., `ai-context` vs `ai_context`) and version mismatches.

### Phase 2: Tiered Archetype Application
1.  **Logical Tiering**: YOU MUST categorize the mapped clusters into distinct tiers. 
    - *Default Tiers*: Governance, Atomic Toolkits, Provenance/History, Core/Root.
    - *Adaptive Logic*: IF a massive assimilation has occurred (e.g., BlueprintX), YOU MUST assess if the 4-tier model remains efficient or if a "Modular Domain" model (Grouped by Feature) is superior.
2.  **Structural Proposal**: Draft a `REDESIGN_PROPOSAL.md` (or similar) detailing the move-map.
    - **Approval Gate**: REQUIRES a "Structural Integrity Clearance" from the user before Phase 3.

### Phase 3: Path Convergence & Mutation
1.  **Atomic Migration**: Move files using high-governance scripts/tools, preserving metadata where possible.
2.  **Global Path Reconciliation**:
    - **Search & Replace**: Use `grep_search` and `multi_replace` to update all detected anchors from Phase 1.
    - **Symlink Management**: IF critical paths must be kept for legacy compatibility, YOU MUST establish explicit symlink bridges and document them in a `LEGACY_PATH_MAP.json`.
3.  **Cross-Reference Audit**: Scan all updated protocols and scripts to ensure no "Ghost Paths" (references to non-existent files) remain.

---

## 3. Operational Integrity Gaps
- **Integrity Anchor**: Update `MANIFEST_STATE.json` after every tier migration.
- **Rollback Protocol**: In the event of an IPC failure or major import break, trigger `SEQ-INTEGRATE-MERGE` to restore from the last verified checkpoint.
- **Validation**: YOU MUST execute [SEQ-EXEC-PLAN-AUDIT](file:///home/jwils/.blueprints/governance/protocols/sequential/SEQ-EXEC-PLAN-AUDIT.md) after the move to verify every file arrived at its destination and every path was updated.

---

## 4. Automation Readiness
This sequence is designed to be triggered by:
1.  A "Friction Alert" from the Verification Agent.
2.  A large-scale assimilation event.
3.  An autonomous scheduled "Substrate Optimization" pulse (3 AM).
