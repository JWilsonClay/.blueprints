# governance/thedoorway/dynamic_contextualizer.py
import os
import json
import time
from pathlib import Path
from datetime import datetime
import hashlib
import argparse
from typing import List, Optional

# Resolve paths standalone for .blueprints workspace
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

try:
    from governance.thedoorway.best_practices_auditor import BestPracticesAuditor
except ImportError:
    BestPracticesAuditor = None

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
            ".git", ".venv", "__pycache__", ".ipynb_checkpoints",
            "node_modules", "build", "dist", ".pytest_cache"
        }
        self.success_cert = DATA_DIR / "ctw_last_success.json"
        self.repair_template = PROJECT_ROOT / "governance" / "thedoorway" / "templates" / "repair_plan.md.template"
        self.repair_plan_file = PROJECT_ROOT / "governance" / "repair_implementation_plan.md"
        
        # Redundant template locations for self-healing
        self.primary_templates = PROJECT_ROOT / "governance" / "thedoorway" / "templates"
        self.backup_templates = PROJECT_ROOT / "templates" / "doorway"

    def run(self, full_scan: bool = False, auto_apply: bool = False, verbose: bool = True) -> dict:
        """Main execution loop for dynamic contextualization."""
        start_time = time.time()
        
        # 0. Ensure Substrate Integrity (Self-Healing)
        self._ensure_substrate_integrity()
        
        # 0.5 Auto-Apply Approved Breadcrumbs
        if auto_apply:
            self._apply_approved_breadcrumbs()
            
        # 1. Load Previous Snapshot
        previous_map = self._load_snapshot()
        
        # 1. Prioritized Structural Scan
        current_map = self._scan_workspace(previous_map, full_scan)
        
        # 2. Detect Drift & Log Proposals
        audit_results = self._audit_structure(current_map, previous_map)
        
        # 3. Persistence
        self._save_snapshot(current_map)

        # 4. Manifest Synchronization
        self._sync_manifest(current_map)
        
        # 5. Protocol Recommendation
        recommendations = self._recommend_protocols(audit_results)
        
        # 6. Qualitative 'Workout' & 7. 'Breakfast' Branching
        quality_results = self._perform_qualitative_audit(audit_results, current_map, full_scan)
        
        overhead = time.time() - start_time
        
        results = {
            "map": current_map,
            "drift": audit_results,
            "recommendations": recommendations,
            "overhead": overhead,
            "skipped": len(previous_map) - len(audit_results.get("modified", [])) - len(audit_results.get("deleted", [])) if not full_scan else 0
        }
        
        if verbose:
            self._render_report(results)
            
        return results

    def _ensure_substrate_integrity(self):
        """Self-Healing: Ensures core files and directories exist."""
        # 1. Ensure data directory
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            (DATA_DIR / ".gitkeep").touch()
            print("[SELF-HEAL] Created missing data/ directory.")

        # 2. Ensure core governance files
        critical_files = {
            self.ownership_file: "FOLDER_OWNERSHIP.md.template",
            self.manifest_file: "MANIFEST.md.template"
        }
        
        for file_path, template_name in critical_files.items():
            if not file_path.exists():
                self._heal(file_path, template_name)

    def _heal(self, target_path: Path, template_name: str):
        """Heals a missing file using redundant templates."""
        template_content = None
        
        # Try Primary
        primary = self.primary_templates / template_name
        if primary.exists():
            template_content = primary.read_text()
        else:
            # Fallback to Backup
            backup = self.backup_templates / template_name
            if backup.exists():
                template_content = backup.read_text()
                print(f"[SELF-HEAL] Primary template missing. Used backup for {target_path.name}.")
        
        if template_content:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(template_content)
            print(f"[SELF-HEAL] Recreated missing {target_path.relative_to(PROJECT_ROOT)} from template.")
        else:
            print(f"[ERROR] Failed to heal {target_path.name}: No template found in primary or backup.")

    def _compute_dir_hash(self, root_path: Path) -> str:
        """Computes hash from concatenated content of sorted .py files."""
        py_files = sorted([f for f in root_path.glob("*.py") if f.is_file()])
        hasher = hashlib.sha256()
        
        for py_file in py_files:
            try:
                # Hash filename and content
                hasher.update(py_file.name.encode())
                hasher.update(py_file.read_bytes())
            except Exception:
                continue
                
        return hasher.hexdigest()

    def _scan_workspace(self, previous_map: dict, full_scan: bool) -> dict:
        """Lazy-recursive scan using content hashes."""
        workspace_map = {}
        
        def should_recurse(rel_path_str: str, current_hash: str) -> bool:
            if full_scan or rel_path_str == ".":
                return True
            prev_info = previous_map.get(rel_path_str)
            if not prev_info:
                return True
            return prev_info.get("content_hash") != current_hash

        for root, dirs, files in os.walk(PROJECT_ROOT):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs and not d.startswith('.')]
            
            root_path = Path(root)
            try:
                rel_path = root_path.relative_to(PROJECT_ROOT)
            except ValueError:
                continue
            rel_path_str = str(rel_path)
            
            # Content-based hash
            content_hash = self._compute_dir_hash(root_path)
            
            # Record entry
            workspace_map[rel_path_str] = {
                "has_readme": "README.md" in files,
                "files_count": len(files),
                "py_files": [f for f in files if f.endswith('.py')],
                "content_hash": content_hash,
                "last_modified": datetime.fromtimestamp(root_path.stat().st_mtime).isoformat(),
                "subdirs": dirs,
                "last_seen": datetime.now().isoformat()
            }
            
            # Prioritized skip logic: if parent hash hasn't changed, 100% of subdirs are also identical
            if not should_recurse(rel_path_str, content_hash):
                # Carry over all known children of this path from the previous map
                for p_old, info_old in previous_map.items():
                    if p_old.startswith(rel_path_str + "/") and p_old not in workspace_map:
                        workspace_map[p_old] = info_old
                dirs[:] = [] # Stop recursion for this branch
                
        return workspace_map

    def _audit_structure(self, current_map: dict, previous_map: dict) -> dict:
        """Detects drift and logs Breadcrumb proposals."""
        drift = {"new": [], "deleted": [], "readme_gaps": [], "unowned": [], "modified": []}
        ownership_map = self._parse_ownership()
        
        for path, info in current_map.items():
            # Change detection
            if path != "." and path not in previous_map:
                drift["new"].append(path)
                self._propose_breadcrumb(path, "new directory")
            elif path in previous_map:
                if info["content_hash"] != previous_map[path].get("content_hash"):
                    drift["modified"].append(path)
                    self._propose_breadcrumb(path, "hash drift")
            
            # README check
            if not info["has_readme"]:
                drift["readme_gaps"].append(path)
                self._create_templated_readme(path)
                
            if path != "." and not self._is_owned(path, ownership_map):
                drift["unowned"].append(path)
                
        for path in previous_map:
            if path not in current_map:
                drift["deleted"].append(path)
                
        return drift

    def _propose_breadcrumb(self, folder_path: str, reason: str):
        """Logs a breadcrumb update request to data/context_updates.log."""
        log_entry = (
            f"Folder: {folder_path}\n"
            f"Proposed breadcrumb: [PENDING AGENT SUMMARIZATION]\n"
            f"Reason: {reason}\n\n"
        )
        try:
            with open(self.update_log, "a") as f:
                f.write(log_entry)
        except Exception:
            pass

    def _is_owned(self, path_str: str, ownership_map: list) -> bool:
        """Smarter Ownership: Exact match or parent-of logic."""
        if path_str == ".":
            return True
        path = Path(path_str)
        
        # Check path and all its parents
        current = path
        while str(current) != ".":
            if str(current).rstrip("/") in ownership_map:
                return True
            if current.parent == current: # Reached root
                break
            current = current.parent
            
        return False

    def _parse_ownership(self) -> list:
        """Extracts directory owners from FOLDER_OWNERSHIP.md."""
        owned_dirs = []
        if not self.ownership_file.exists():
            return owned_dirs
        
        try:
            lines = self.ownership_file.read_text().splitlines()
            for line in lines:
                if line.strip().startswith("- "):
                    # Extract path from '- path/: description'
                    parts = line.split(":")
                    if parts:
                        path_part = parts[0].replace("- ", "").strip().rstrip("/")
                        owned_dirs.append(path_part)
        except Exception:
            pass
        return owned_dirs

    def _create_templated_readme(self, folder_path_str: str):
        """Self-healing: Creates a standard README.md."""
        target = PROJECT_ROOT / folder_path_str / "README.md"
        name = Path(folder_path_str).name
        
        # Try to load template from redundant locations
        template_content = None
        for base in [self.primary_templates, self.backup_templates]:
            tpl_file = base / "README.md.template"
            if tpl_file.exists():
                template_content = tpl_file.read_text()
                break
        
        if template_content:
            # Replace placeholders
            template_content = template_content.replace("{name}", name)
            template_content = template_content.replace("{path}", folder_path_str)
        else:
            # Fallback inline template
            template_content = f"""# {name} — [One Sentence Owner Description Placeholder]

This directory is part of the .blueprints architecture.

## Ownership
- **Owner**: [Defined in FOLDER_OWNERSHIP.md]
- **Standard Sentence**: "- {folder_path_str}/: [Description]"

## Contents
<!-- BREADCRUMB -->
Auto-generated summary for navigation.
<!-- BREADCRUMB_END -->
"""
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(template_content)
        except Exception:
            pass

    def _recommend_protocols(self, drift: dict) -> list:
        """Intelligence Layer: Suggests specific SEQ files."""
        recs = []
        if drift["new"]:
            recs.append({
                "id": "SEQ-SUBSTRATE-HEALTH", 
                "reason": f"New directories detected ({', '.join(drift['new'][:2])}). Verify architectural alignment."
            })
        if drift["unowned"]:
            recs.append({
                "id": "SEQ-SUBSTRATE-HYGIENE",
                "reason": f"Unowned folders found. Update FOLDER_OWNERSHIP.md to prevent logic bloat."
            })
        return recs

    def _load_snapshot(self) -> dict:
        if self.snapshot_file.exists():
            try:
                return json.loads(self.snapshot_file.read_text())
            except Exception:
                return {}
        return {}

    def _save_snapshot(self, data: dict):
        try:
            self.snapshot_file.write_text(json.dumps(data, indent=2))
        except Exception:
            pass

    def _render_report(self, results: dict):
        print("\n=== .blueprints Live Architectural Map ===")
        print(f"Scan completed in {results['overhead']:.2f}s")
        
        if results["drift"]["new"]:
            print(f"[+] NEW DIRECTORIES: {', '.join(results['drift']['new'])}")
        
        if results["drift"]["modified"]:
            print(f"[*] MODIFIED: {', '.join(results['drift']['modified'])}")
            
        if results["drift"]["readme_gaps"]:
            print(f"[!] README SEEDING: Created templates in {len(results['drift']['readme_gaps'])} folders.")
        
        print(f"\nContext web update complete. {len(results['map'])} directories scanned, {results['skipped']} skipped.")
        print("Detailed proposals logged to data/context_updates.log")

    def _apply_approved_breadcrumbs(self):
        """Processes the log and applies non-placeholder breadcrumbs to READMEs."""
        if not self.update_log.exists():
            return

        try:
            content = self.update_log.read_text()
            if not content:
                return

            # Split into proposals
            proposals = content.split("--- PROPOSAL")
            remaining_proposals = []
            
            # Simple header if it was empty-ish
            if not proposals[0].strip():
                proposals = proposals[1:]

            for prop in proposals:
                prop_str = "--- PROPOSAL" + prop if not prop.startswith("Folder:") else prop
                lines = prop_str.strip().splitlines()
                
                folder = None
                breadcrumb = None
                
                for line in lines:
                    if line.startswith("Folder:"):
                        folder = line.replace("Folder:", "").strip()
                    if line.startswith("Proposed breadcrumb:"):
                        val = line.replace("Proposed breadcrumb:", "").strip()
                        if val and val != "[PENDING AGENT SUMMARIZATION]":
                            breadcrumb = val
                
                if folder and breadcrumb:
                    # Apply
                    if self._update_readme_breadcrumb(folder, breadcrumb):
                        print(f"[AUTO-APPLY] Updated {folder}")
                    else:
                        remaining_proposals.append(prop_str)
                else:
                    remaining_proposals.append(prop_str)

            # Rewrite log with remaining
            if remaining_proposals:
                self.update_log.write_text("\n\n".join(remaining_proposals) + "\n")
            else:
                self.update_log.write_text("")

        except Exception as e:
            print(f"[ERROR] Auto-apply failed: {e}")

    def _update_readme_breadcrumb(self, folder_path_str: str, breadcrumb: str) -> bool:
        """Surgically updates the BREADCRUMB section in a README."""
        target = PROJECT_ROOT / folder_path_str / "README.md"
        if not target.exists():
            return False

        try:
            content = target.read_text()
            tag_start = "<!-- BREADCRUMB -->"
            tag_end = "<!-- BREADCRUMB_END -->"
            
            if tag_start in content and tag_end in content:
                # Replace the middle
                parts_before = content.split(tag_start)
                parts_after = content.split(tag_end)
                if len(parts_before) > 1 and len(parts_after) > 1:
                    before = parts_before[0]
                    after = parts_after[-1]
                    new_content = f"{before}{tag_start}\n{breadcrumb}\n{tag_end}{after}"
                    target.write_text(new_content)
                    return True
            else:
                # Append tags if missing to ensure contextualization
                new_content = content.rstrip() + f"\n\n## Contents\n{tag_start}\n{breadcrumb}\n{tag_end}\n"
                target.write_text(new_content)
                return True
        except Exception:
            pass
        return False

    def _perform_qualitative_audit(self, audit_results: dict, current_map: dict, full_scan: bool) -> Optional[dict]:
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
                    files_to_audit.append(PROJECT_ROOT / path / f)
        else:
            for path in paths_to_audit:
                if path in current_map:
                    for f in current_map[path].get("py_files", []):
                        files_to_audit.append(PROJECT_ROOT / path / f)

        if not files_to_audit:
            return None

        auditor = BestPracticesAuditor(PROJECT_ROOT)
        results = auditor.run(files_to_audit)
        
        # Branching Outcome
        if results["summary"]["violations"] > 0 or results["summary"]["warnings"] > 0:
            self._generate_repair_plan(results, files_to_audit)
        else:
            self._write_success_certificate(results, files_to_audit)
            
        return results

    def _generate_repair_plan(self, results: dict, files: List[Path]):
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
            if self.repair_template.exists():
                template_content = self.repair_template.read_text()
            else:
                return
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        template = template_content
        
        # Prepare high-impact refactors (KISS/SOLID)
        high_impact = []
        for v in results["doctrines"]["SOLID_KISS"]:
            if v.get("level") == "violation":
                msg = f"- **{v['file']}**:{v.get('line','?')} -> {v['message']}"
                if "function" in v: msg += f" in `{v['function']}`"
                if "cc" in v: msg += f" (CC={v['cc']})"
                high_impact.append(msg)
        
        # Prepare SoC violations
        soc_violations = [f"- {v['file']}:{v['line']} -> {v['message']}" for v in results["doctrines"]["SoC"]]
        
        # Prepare DRY / Contamination violations
        dry_violations = [f"- {v['file']}:{v['line']} -> {v['message']}" for v in results["doctrines"]["DRY"]]
        
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
            "{high_impact_refactors}": "\n".join(high_impact) if high_impact else "_None detected_",
            "{soc_violations}": "\n".join(soc_violations) if soc_violations else "_None detected_",
            "{dry_violations}": "\n".join(dry_violations) if dry_violations else "_None detected_",
            "{other_recommendations}": "_Follow .blueprints architectural conventions._"
        }
        
        report = template
        for k, v in context.items():
            report = report.replace(k, v)
            
        self.repair_plan_file.write_text(report)
        print(f"\n[!] Audit Findings: Repair plan generated at {self.repair_plan_file.relative_to(PROJECT_ROOT)}")

    def _write_success_certificate(self, results: dict, files: List[Path]):
        """Tier 3: Branch Success → Success Certificate."""
        cert = {
            "status": "ZERO_FINDING",
            "timestamp": datetime.now().isoformat(),
            "summary": results["summary"],
            "files_scanned": len(files)
        }
        self.success_cert.write_text(json.dumps(cert, indent=2))
        if self.repair_plan_file.exists():
            self.repair_plan_file.unlink() # Clear legacy repair plan
        print(f"\n[+] ZERO-FINDING STATE: Workspace verified at {cert['timestamp']}")

    def _sync_manifest(self, current_map: dict):
        """Surgically updates MANIFEST.md with all discovered READMEs."""
        if not self.manifest_file.exists():
            return

        try:
            # 1. Collect all paths with READMEs
            discovered_readmes = []
            for path, info in current_map.items():
                if info.get("has_readme"):
                    # Use absolute paths for file links as per project standards
                    abs_path = PROJECT_ROOT / path
                    abs_readme = abs_path / "README.md"
                    
                    # Formatting matching MANIFEST.md style
                    display_name = f"/{path}" if path != "." else "/root"
                    entry = f"- [{display_name}](file://{abs_path}/) : [README](file://{abs_readme})"
                    discovered_readmes.append((path, entry))

            # 2. Sort alphabetally (but keep root first if present)
            discovered_readmes.sort(key=lambda x: (x[0] != ".", x[0]))
            formatted_entries = [entry for path, entry in discovered_readmes]

            # 3. Surgical Update of MANIFEST.md
            content = self.manifest_file.read_text()
            lines = content.splitlines()
            
            new_lines = []
            in_directories_section = False
            section_replaced = False

            for line in lines:
                if line.startswith("## Root Directories") or "(Auto-Synced)" in line:
                    new_lines.append("## Root Directories (Auto-Synced)")
                    new_lines.extend(formatted_entries)
                    in_directories_section = True
                    section_replaced = True
                    continue
                
                if in_directories_section:
                    if line.startswith("---") or (line.startswith("## ") and "(Auto-Synced)" not in line):
                        in_directories_section = False
                        new_lines.append("")
                        new_lines.append(line)
                    continue
                
                new_lines.append(line)

            # If we didn't find the section to replace, append it (safety fallback)
            if not section_replaced:
                new_lines.append("\n## Root Directories (Auto-Synced)")
                new_lines.extend(formatted_entries)

            self.manifest_file.write_text("\n".join(new_lines) + "\n")
            print(f"[MANIFEST] Synced {len(formatted_entries)} READMEs to governance/MANIFEST.md")

        except Exception as e:
            print(f"[ERROR] Manifest sync failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blueprints Doorway Contextualizer")
    parser.add_argument("--full-scan", action="store_true", help="Force deep scan of all directories")
    parser.add_argument("--auto-apply", action="store_true", help="Apply approved breadcrumbs from the log")
    args = parser.parse_args()

    contextualizer = DoorwayContextualizer()
    contextualizer.run(full_scan=args.full_scan, auto_apply=args.auto_apply)
