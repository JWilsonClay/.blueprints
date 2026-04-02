# governance/thedoorway/scanner.py
import hashlib
import os
from datetime import datetime
from pathlib import Path

class WorkspaceScanner:
    """
    Handles filesystem intelligence for the Doorway Protocol.
    Responsible for recursive workspace scanning, content-based hashing, and delta determination.
    """

    def __init__(self, project_root: Path, ignore_dirs: set):
        self.project_root = project_root
        self.ignore_dirs = ignore_dirs

    def compute_dir_hash(self, root_path: Path) -> str:
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

    def scan(self, previous_map: dict, full_scan: bool) -> tuple:
        """
        Lazy-recursive scan using content hashes.
        Returns: Tuple[dict, int] (workspace_map, ingested_readme_count)
        """
        workspace_map = {}
        ingested_count = 0

        def should_recurse(rel_path_str: str, current_hash: str) -> bool:
            if full_scan or rel_path_str == ".":
                return True
            prev_info = previous_map.get(rel_path_str)
            if not prev_info:
                return True
            return prev_info.get("content_hash") != current_hash

        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [
                d for d in dirs if d not in self.ignore_dirs and not d.startswith(".")
            ]

            root_path = Path(root)
            try:
                rel_path = root_path.relative_to(self.project_root)
            except ValueError:
                continue
            rel_path_str = str(rel_path)

            # Content-based hash
            content_hash = self.compute_dir_hash(root_path)

            # Record entry
            has_readme = "README.md" in files
            if has_readme:
                ingested_count += 1

            workspace_map[rel_path_str] = {
                "has_readme": has_readme,
                "files_count": len(files),
                "py_files": [f for f in files if f.endswith(".py")],
                "content_hash": content_hash,
                "last_modified": datetime.fromtimestamp(
                    root_path.stat().st_mtime
                ).isoformat(),
                "subdirs": dirs,
                "last_seen": datetime.now().isoformat(),
            }

            # Prioritized skip logic: if parent hash hasn't changed, 100% of subdirs are also identical
            if not should_recurse(rel_path_str, content_hash):
                # Carry over all known children of this path from the previous map
                for p_old, info_old in previous_map.items():
                    if (
                        p_old.startswith(rel_path_str + "/")
                        and p_old not in workspace_map
                    ):
                        workspace_map[p_old] = info_old
                        # Count existing READMES being carried over
                        if info_old.get("has_readme"):
                            ingested_count += 1
                dirs[:] = []  # Stop recursion for this branch

        return workspace_map, ingested_count
