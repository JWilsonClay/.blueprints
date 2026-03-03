# Strategic Needs List: Protocol Substrate Hardening (v1.0.0)

**Focus:** Universal Structural Alignment & Peer-to-Anchor Reliability

---

## 1. Immediate Technical Needs (Sprint 1)
1.  **Unified Substrate Validator:**
    - Evolve [role_seniority_validator.py](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/toolkits/audit_onboarding/role_seniority_validator.py) into `substrate_seniority_validator.py`.
    - Support any Markdown artifact containing a [date_created](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/toolkits/audit_onboarding/role_seniority_validator.py#27-37) stamp (Roles, Protocols, specs).
2.  **Universal Protocol Header (UPH) Template:**
    - Stabilize the 5-field schema: `Protocol_ID`, `Structure_Status`, `Target_Audience`, `Assigned_Role`, `Purpose`.
    - This is the "Anchor Source" for all Cycle 1 Structural Injections.
3.  **Protocol-Class Assimilation Script:**
    - A dedicated reformat loop for protocols to ensure they match the UPH and the 3-cycle sequence.

---

## 2. Orchestration & Intelligence Needs (Sprint 2)
1.  **Seniority-Ranked Context Assembly:**
    - Update `Orchestrator_Agent` (00) to build prompt contexts by sorting active protocols by [date_created](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/toolkits/audit_onboarding/role_seniority_validator.py#27-37) (Ancient first).
    - This ensures the LLM's "First Impression" is the most hardened logic.
2.  **Supersede/Redundancy Registry:**
    - Implementation of the `supersedes: [ID, ...]` field in protocol frontmatter.
    - Automated hygiene triggers when the total "Absorption Count" overlaps $>80\%$.

---

## 3. Substrate Resilience Needs (Sprint 3)
1.  **Recursive Protocol Audit Loop:**
    - A specialized tier in `OP-RISK-AUDIT` that specifically tests protocol-on-protocol logic clashes.
2.  **Dynamic Threshold Scaling:**
    - Automated adjustment of the 10% variance limit based on protocol complexity (e.g., higher tolerance for 300+ line documents).
