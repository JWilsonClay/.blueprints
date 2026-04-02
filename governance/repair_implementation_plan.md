# Repair Implementation Plan — CtW Audit 2026-04-02 10:43:54

## Summary
- Timestamp: 2026-04-02 10:43:54
- Scanned files: 63
- Total violations: 4
- Warnings: 0
- Auto-fixable: 0

Per doctrine:
- PEP 8: 8
- SoC: 6
- SOLID + KISS: 367
- DRY: 4 (phase 2 pending)
- YAGNI: 0 (phase 2 pending)

## Quick Wins (Auto-Fixable)
```bash
# Format & fix lint issues
ruff check --fix governance/
ruff format governance/     # If using Ruff formatter
```

## High-Impact Refactors (KISS/SOLID)
*Manual intervention required for the following hotspots:*
_None detected_

## Structural & SoC Violations
*Violations of absolute imports or directory ownership:*
- /home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/governance/thedoorway/breadcrumb_manager.py:2 -> Import block is un-sorted or un-formatted
- /home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/governance/thedoorway/dynamic_contextualizer.py:13 -> Import block is un-sorted or un-formatted
- /home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/governance/thedoorway/integrity_manager.py:2 -> Import block is un-sorted or un-formatted
- /home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/governance/thedoorway/manifest_manager.py:2 -> Import block is un-sorted or un-formatted
- /home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/governance/thedoorway/scanner.py:2 -> Import block is un-sorted or un-formatted
- /home/jwils/GoogleDrive1TB/PapiBobes/.blueprints/governance/thedoorway/structural_auditor.py:2 -> Import block is un-sorted or un-formatted

## Other Recommendations
_Follow .blueprints architectural conventions._

## Verification
Re-run `python3 governance/thedoorway/dynamic_contextualizer.py --full-scan` to verify repair status.
