# governance/thedoorway/audit_repairs.py
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

try:
    from governance.thedoorway.best_practices_auditor import BestPracticesAuditor
except ImportError:
    BestPracticesAuditor = None

class AuditRepairManager:
    """
    Handles Tier 2 and Tier 3 operations of the Doorway Protocol.
    Responsible for qualitative auditing, repair plan generation, and success certification.
    """

    def __init__(
        self,
        project_root: Path,
        primary_templates: Path,
        backup_templates: Path,
        repair_plan_file: Path,
        success_cert_file: Path,
        repair_template_file: Path
    ):
        self.project_root = project_root
        self.primary_templates = primary_templates
        self.backup_templates = backup_templates
        self.repair_plan_file = repair_plan_file
        self.success_cert_file = success_cert_file
        self.repair_template_file = repair_template_file

    def perform_qualitative_audit(
        self, audit_results: dict, current_map: dict, full_scan: bool
    ) -> Optional[dict]:
        """Tier 2: Qualitative Audit hook."""
        if not BestPracticesAuditor:
            return None

        # Determine files to audit (only new, modified, or everything on full_scan)
        paths_to_audit = set(audit_results["new"] + audit_results["modified"])
        files_to_audit = []

        if full_scan:
            # Full scan: audit all python files in the current map
            for path, info in current_map.items():
                for f in info.get("py_files", []):
                    files_to_audit.append(self.project_root / path / f)
        else:
            for path in paths_to_audit:
                if path in current_map:
                    for f in current_map[path].get("py_files", []):
                        files_to_audit.append(self.project_root / path / f)

        if not files_to_audit:
            return None

        auditor = BestPracticesAuditor(self.project_root)
        results = auditor.run(files_to_audit)

        # Branching Outcome
        if results["summary"]["violations"] > 0 or results["summary"]["warnings"] > 0:
            self.generate_repair_plan(results, files_to_audit)
        else:
            self.write_success_certificate(results, files_to_audit)

        return results

    def generate_repair_plan(self, results: dict, files: List[Path]):
        """Tier 3: Branch Findings → Repair Plan."""
        # Redundant template loading for repair plan
        template_content = None
        for base in [self.primary_templates, self.backup_templates]:
            tpl_file = base / "repair_plan.md.template"
            if tpl_file.exists():
                template_content = tpl_file.read_text()
                break

        if not template_content:
            # Fallback to the hardcoded path if templates missing
            if self.repair_template_file.exists():
                template_content = self.repair_template_file.read_text()
            else:
                return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        template = template_content

        # Prepare high-impact refactors (KISS/SOLID)
        high_impact = []
        for v in results["doctrines"]["SOLID_KISS"]:
            if v.get("level") == "violation":
                msg = f"- **{v['file']}**:{v.get('line', '?')} -> {v['message']}"
                if "function" in v:
                    msg += f" in `{v['function']}`"
                if "cc" in v:
                    msg += f" (CC={v['cc']})"
                high_impact.append(msg)

        # Prepare SoC violations
        soc_violations = [
            f"- {v['file']}:{v['line']} -> {v['message']}"
            for v in results["doctrines"]["SoC"]
        ]

        # Prepare DRY / Contamination violations
        dry_violations = [
            f"- {v['file']}:{v['line']} -> {v['message']}"
            for v in results["doctrines"]["DRY"]
        ]

        context = {
            "{timestamp}": timestamp,
            "{count}": str(len(files)),
            "{violations}": str(results["summary"]["violations"]),
            "{warnings}": str(results["summary"]["warnings"]),
            "{auto_fixable}": str(results["summary"]["auto_fixable"]),
            "{pep8_count}": str(len(results["doctrines"]["PEP8"])),
            "{soc_count}": str(len(results["doctrines"]["SoC"])),
            "{solid_kiss_count}": str(len(results["doctrines"]["SOLID_KISS"])),
            "{dry_count}": str(len(results["doctrines"]["DRY"])),
            "{yagni_count}": str(len(results["doctrines"]["YAGNI"])),
            "{high_impact_refactors}": "\n".join(high_impact)
            if high_impact
            else "_None detected_",
            "{soc_violations}": "\n".join(soc_violations)
            if soc_violations
            else "_None detected_",
            "{dry_violations}": "\n".join(dry_violations)
            if dry_violations
            else "_None detected_",
            "{other_recommendations}": "_Follow .blueprints architectural conventions._",
        }

        report = template
        for k, v in context.items():
            report = report.replace(k, v)

        self.repair_plan_file.write_text(report)
        print(
            f"\n[!] Audit Findings: Repair plan generated at {self.repair_plan_file.relative_to(self.project_root)}"
        )

    def write_success_certificate(self, results: dict, files: List[Path]):
        """Tier 3: Branch Success → Success Certificate."""
        cert = {
            "status": "ZERO_FINDING",
            "timestamp": datetime.now().isoformat(),
            "summary": results["summary"],
            "files_scanned": len(files),
        }
        self.success_cert_file.write_text(json.dumps(cert, indent=2))
        if self.repair_plan_file.exists():
            self.repair_plan_file.unlink()  # Clear legacy repair plan
        print(f"\n[+] ZERO-FINDING STATE: Workspace verified at {cert['timestamp']}")
