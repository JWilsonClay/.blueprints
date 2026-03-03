# =====================================================
# FILE: documentation_generator.py
# NAME: documentation_generator.py
# PURPOSE: Auto-builds ADRs, API specs, graphs, and migration guides.
# DETAILS: Embeds audit findings and evaluator metrics automatically. Outputs Markdown with ventilated prose.
# VERSION: 1.0.0
# =====================================================

"""Documentation generator for the Genesis_Agent role."""

def generate_adr_from_changeset(changeset: Dict) -> str:
    """Creates an Architecture Decision Record."""
    return f"""# ADR-001: {changeset.get('title')}

## Status
Accepted

## Context
{changeset.get('rationale')}

## Decision
Implemented via Genesis_Agent role and OP-REFINE-HARDEN@1.0.0.
"""