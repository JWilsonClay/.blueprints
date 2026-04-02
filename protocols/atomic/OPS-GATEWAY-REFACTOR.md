---
protocol_id: OPS-GATEWAY-REFACTOR
structure_status: HARDENED
target_audience: Genesis_Agent, Orchestrator_Agent, Verification_Agent
assigned_role: Genesis_Agent
purpose: Systematically refactor root-level scripts into Protocol Gateways to enforce architectural seniority.
version: 1.0.0
status: ACTIVE
date_created: 2026-03-25
date_modified: 2026-03-25
---
# Operational Protocol: Gateway Refactor (OPS-GATEWAY-REFACTOR)

## 1. Core Function
This protocol defines the transition of a "Junior" implementation script into a "Senior" Protocol Gateway. A Gateway does not contain logic; it merely executes the appropriate Sequential Protocol.

## 2. Execution Frame (UAL)

### Phase 1: Logic Promotion
- YOU MUST extract all implementation-specific logic (functions, tools, constants) from the target script.
- YOU MUST promote extracted logic to the appropriate `governance/toolkits/` or `governance/roles/` directory.

### Phase 2: Surgical Stripping
- YOU MUST delete the original script content.
- YOU MUST recreate the script as a "Protocol Gateway".
- The Gateway content MUST be limited to:
  - Import of the execution engine.
  - A single call to `SEQ-EXECUTE-BLUEPRINT` or the target Role/Protocol.

### Phase 3: Seniority Lock
- YOU MUST verify that the new Gateway refers strictly to the senior substrate.
- YOU MUST audit the new modularized components via `OPS-RISK-AUDIT`.

---
