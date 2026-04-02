# governance/thedoorway/structural_auditor.py
from pathlib import Path

class StructuralAuditor:
    """
    Handles structural auditing and drift detection for the Doorway Protocol.
    Responsible for comparing workspace maps, verifying directory ownership, and flagging README gaps.
    """

    def __init__(self, project_root: Path, ownership_file: Path, breadcrumb_manager, integrity_manager, metrics: dict):
        self.project_root = project_root
        self.ownership_file = ownership_file
        self.breadcrumb_manager = breadcrumb_manager
        self.integrity_manager = integrity_manager
        self.metrics = metrics

    def audit(self, current_map: dict, previous_map: dict) -> dict:
        """Detects drift and logs Breadcrumb proposals."""
        drift = {
            "new": [],
            "deleted": [],
            "readme_gaps": [],
            "unowned": [],
            "modified": [],
        }
        ownership_map = self.parse_ownership()

        for path, info in current_map.items():
            # Change detection
            if path != "." and path not in previous_map:
                drift["new"].append(path)
                self.breadcrumb_manager.propose(path, "new directory")
            elif path in previous_map:
                if info["content_hash"] != previous_map[path].get("content_hash"):
                    drift["modified"].append(path)
                    self.breadcrumb_manager.propose(path, "hash drift")

            # README check
            if not info["has_readme"]:
                drift["readme_gaps"].append(path)
                # Trigger self-healing
                if self.integrity_manager.create_readme(path):
                    self.metrics["created"] += 1
                    self.metrics["repairs"] += 1

            if path != "." and not self.is_owned(path, ownership_map):
                drift["unowned"].append(path)

        for path in previous_map:
            if path not in current_map:
                drift["deleted"].append(path)

        return drift

    def is_owned(self, path_str: str, ownership_map: list) -> bool:
        """Smarter Ownership: Exact match or parent-of logic."""
        if path_str == ".":
            return True
        path = Path(path_str)

        # Check path and all its parents
        current = path
        while str(current) != ".":
            if str(current).rstrip("/") in ownership_map:
                return True
            if current.parent == current:  # Reached root
                break
            current = current.parent

        return False

    def parse_ownership(self) -> list:
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
