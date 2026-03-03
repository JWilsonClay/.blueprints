# Implementation Plan: Protocol Substrate Hardening (v1.0.0)

This plan outlines the technical steps to extend our anti-corruption and seniority gates to the 18+ Operational Protocols in the `.blueprints/protocols/` directory.

## Proposed Changes

### [Tooling & Architecture]

#### [MODIFY] [role_seniority_validator.py](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/toolkits/audit_onboarding/role_seniority_validator.py)
- Rename (internally or logically) to **Substrate Seniority Validator**.
- Ensure the extraction logic can handle both [role](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/toolkits/audit_onboarding/simulate_assimilation_drift.py#13-29) and `protocol_id` keys in YAML frontmatter.
- Implement the Universal Protocol Header (UPH) verification logic.

#### [NEW] [OP-SUBSTRATE-ASSIMILATE](file:///home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/protocols/substrate_assimilation_protocol.md)
- Pivot the existing role-based assimilation protocol to a universal substrate-level reformat loop.
- Mandate the 3-cycle reformat for any protocol artifact ingested as context.

### [Substrate Standardization]

#### [MODIFY] Protocol Files (Batch Execution)
- Systematically inject the UPH into all 18 protocol files:
    - `Protocol_ID`
    - `Structure_Status`
    - `Target_Audience`
    - `Assigned_Role`
    - `Purpose`

## Verification Plan

### Automated Tests
- Run the `substrate_seniority_validator` against a sample of protocols.
- Execute a "Protocol Drift Simulation":
    - Create a junior protocol with legacy headers.
    - Verify that the `Verification_Agent` flags the structural variance and triggers the UPH-injection loop.

### Manual Verification
- Review the [Intelligence_Assessment_Protocol_Substrate.md](file:///home/jwils/.gemini/antigravity/brain/504349b6-87a7-4d90-989b-3626964a0e23/Intelligence_Assessment_Protocol_Substrate.md) for strategic alignment.
