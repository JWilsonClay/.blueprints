---
protocol_id: OP-SCAFFOLD-BUILD
version: 1.0.0
status: ACTIVE
last_updated: 2026-03-02
---
# Operational Protocol: Scaffolding Generation (OP-SCAFFOLD-BUILD)

```json
// EXAMPLE_PROVENANCE_HEADER
{
  "example_genesis_agent_version": "1.0.0",
  "example_timestamp": "2026-03-02T17:07:44-06:00",
  "example_protocol_reference": "OP-SCAFFOLD-BUILD",
  "example_target_audience": "Verification Agent"
}
```

**Protocol ID:** OP-SCAFFOLD-BUILD
**Assigned Role:** Builder
**Target Audience:** Verification Agent, Refiner Role

## 1. Core Function & Rationale

- This protocol defines mandatory file-generation templates.
- This protocol defines required naming conventions.
- This protocol enforces strict dependency graphs.
- This protocol institutes a seven-robustness-attribute checklist explicitly for the Builder.
- This protocol prevents the Builder from emitting unstructured scaffolding that cascades failures.

## 2. Execution Constraints

- You MUST enforce that every generated file embeds a traceable provenance header.
- You MUST evaluate generated scaffolding against the "Template Completeness" dimension.
- You MUST evaluate generated scaffolding against the "Provenance Traceability" dimension.

## 3. The Pure-Prompt Scaffolding Variant

- **Condition:** If the generated scaffolding contains no executable code (pure-prompt generation).
- **Instruction:** You MUST explicitly invoke the LLM-only template variant.
- You MUST generate exactly three variant seeds for the pure-prompt scaffold.
- You MUST execute a majority-vote internal check across the three variant seeds.
- You MUST select the winning variant as the final output.

## 4. Required Output Checklist

- [ ] Is the generated module strictly Scalable?
- [ ] Is the generated module strictly Modular?
- [ ] Is the generated module strictly Comprehensive?
- [ ] Is the generated module strictly Verifiable?
- [ ] Is the generated module strictly Maintainable?
- [ ] Is the generated module strictly Adaptable?
- [ ] Is the generated module strictly Efficient?
