# governance/thedoorway/dynamic_contextualizer.py
import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# Resolve paths standalone for .blueprints workspace
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

from governance.thedoorway.audit_repairs import AuditRepairManager
from governance.thedoorway.scanner import WorkspaceScanner
from governance.thedoorway.breadcrumb_manager import BreadcrumbManager
from governance.thedoorway.integrity_manager import IntegrityManager
from governance.thedoorway.structural_auditor import StructuralAuditor
from governance.thedoorway.recommender import ProtocolRecommender
from governance.thedoorway.manifest_manager import ManifestManager
from governance.thedoorway.reporter import SubstrateReporter


class DoorwayContextualizer:
    """
    Dynamic Ingestion Protocol ("The Doorway").
    Performs active structural audits, self-healing READMEs, and protocol recommendations.
    Now enhanced with Substrate Integrity (Self-Healing) for core governance files.
    """

    def __init__(self):
        self.snapshot_file = DATA_DIR / "workspace_snapshot.json"
        self.ownership_file = PROJECT_ROOT / "docs" / "FOLDER_OWNERSHIP.md"
        self.manifest_file = PROJECT_ROOT / "governance" / "MANIFEST.md"
        self.update_log = DATA_DIR / "context_updates.log"
        self.ignore_dirs = {
            ".git",
            ".venv",
            "__pycache__",
            ".ipynb_checkpoints",
            "node_modules",
            "build",
            "dist",
            ".pytest_cache",
        }
        self.success_cert = DATA_DIR / "ctw_last_success.json"
        self.repair_template = (
            PROJECT_ROOT
            / "governance"
            / "thedoorway"
            / "templates"
            / "repair_plan.md.template"
        )
        self.repair_plan_file = (
            PROJECT_ROOT / "governance" / "repair_implementation_plan.md"
        )

        # Metrics Tracking (v1.1.0)
        self.metrics = {"created": 0, "ingested": 0, "repairs": 0}

        # Redundant template locations for self-healing
        self.primary_templates = (
            PROJECT_ROOT / "governance" / "thedoorway" / "templates"
        )
        self.backup_templates = PROJECT_ROOT / "templates" / "doorway"

        # Tier 2/3 Audit & Repair Manager (v1.1.0 Refactor)
        self.audit_manager = AuditRepairManager(
            PROJECT_ROOT,
            self.primary_templates,
            self.backup_templates,
            self.repair_plan_file,
            self.success_cert,
            self.repair_template
        )

        # Tier 1 Scanner (v1.1.0 Refactor)
        self.scanner = WorkspaceScanner(PROJECT_ROOT, self.ignore_dirs)

        # Breadcrumb Orchestration Manager (v1.1.0 Refactor)
        self.breadcrumb_manager = BreadcrumbManager(PROJECT_ROOT, self.update_log)

        # Substrate Integrity Manager (v1.1.0 Refactor)
        self.integrity_manager = IntegrityManager(
            PROJECT_ROOT, self.primary_templates, self.backup_templates
        )
        # Tier 4 Structural Auditor (v1.1.0 Refactor)
        self.auditor = StructuralAuditor(
            PROJECT_ROOT,
            self.ownership_file,
            self.breadcrumb_manager,
            self.integrity_manager,
            self.metrics
        )

        # Intelligence Layer (v1.1.0 Refactor)
        self.recommender = ProtocolRecommender()

        # Manifest Synchronization Manager (v1.1.0 Refactor)
        self.manifest_manager = ManifestManager(PROJECT_ROOT, self.manifest_file)

        # Assertion-Based Reporter (v1.1.0 Refactor)
        self.reporter = SubstrateReporter()

    def run(
        self, full_scan: bool = False, auto_apply: bool = False, verbose: bool = True
    ) -> dict:
        """Main execution loop for dynamic contextualization."""
        start_time = time.time()

        # 0. Ensure Substrate Integrity (Self-Healing)
        critical_files = {
            self.ownership_file: "FOLDER_OWNERSHIP.md.template",
            self.manifest_file: "MANIFEST.md.template",
        }
        self.integrity_manager.ensure_substrate(DATA_DIR, critical_files)

        # 0.5 Auto-Apply Approved Breadcrumbs
        if auto_apply:
            self.breadcrumb_manager.apply_approved()

        # 1. Load Previous Snapshot
        previous_map = self._load_snapshot()

        # 1. Prioritized Structural Scan
        current_map, ingested_count = self.scanner.scan(previous_map, full_scan)
        self.metrics["ingested"] = ingested_count

        # 2. Detect Drift & Log Proposals
        audit_results = self.auditor.audit(current_map, previous_map)

        # 3. Persistence
        self._save_snapshot(current_map)

        # 4. Manifest Synchronization
        self.manifest_manager.sync(current_map)

        # 5. Protocol Recommendation
        recommendations = self.recommender.recommend(audit_results)

        # 6. Qualitative 'Workout' & 7. 'Breakfast' Branching
        self.audit_manager.perform_qualitative_audit(audit_results, current_map, full_scan)

        overhead = time.time() - start_time

        results = {
            "map": current_map,
            "drift": audit_results,
            "recommendations": recommendations,
            "overhead": overhead,
            "skipped": len(previous_map)
            - len(audit_results.get("modified", []))
            - len(audit_results.get("deleted", []))
            if not full_scan
            else 0,
        }

        if verbose:
            self.reporter.render(results, self.metrics)

        return results

    def _load_snapshot(self) -> dict:
        """Persistence Layer: Snapshot Loading."""
        if self.snapshot_file.exists():
            try:
                return json.loads(self.snapshot_file.read_text())
            except Exception:
                return {}
        return {}

    def _save_snapshot(self, data: dict):
        """Persistence Layer: Snapshot Saving."""
        try:
            self.snapshot_file.write_text(json.dumps(data, indent=2))
        except Exception:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blueprints Doorway Contextualizer")
    parser.add_argument(
        "--full-scan", action="store_true", help="Force deep scan of all directories"
    )
    parser.add_argument(
        "--auto-apply",
        action="store_true",
        help="Apply approved breadcrumbs from the log",
    )
    args = parser.parse_args()

    contextualizer = DoorwayContextualizer()
    contextualizer.run(full_scan=args.full_scan, auto_apply=args.auto_apply)
