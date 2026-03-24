# Repair Implementation Plan — CtW Audit {timestamp}

## Summary
- Timestamp: {timestamp}
- Scanned files: {count}
- Total violations: {violations}
- Warnings: {warnings}
- Auto-fixable: {auto_fixable}

Per doctrine:
- PEP 8: {pep8_count}
- SoC: {soc_count}
- SOLID + KISS: {solid_kiss_count}
- DRY: {dry_count} (phase 2 pending)
- YAGNI: {yagni_count} (phase 2 pending)

## Quick Wins (Auto-Fixable)
```bash
# Format & fix lint issues
ruff check --fix contentflow/
ruff format contentflow/     # If using Ruff formatter
```

## High-Impact Refactors (KISS/SOLID)
*Manual intervention required for the following hotspots:*
{high_impact_refactors}

## Structural & SoC Violations
*Violations of absolute imports or directory ownership:*
{soc_violations}

## Other Recommendations
{other_recommendations}

## Verification
Re-run `python3 -m contentflow.governance.dynamic_contextualizer --full-scan` to verify repair status.
