# governance/thedoorway/manifest_manager.py
from pathlib import Path

class ManifestManager:
    """
    Handles surgical updates to the workspace MANIFEST.md.
    Syncs discovered READMEs into the (Auto-Synced) section.
    """

    def __init__(self, project_root: Path, manifest_file: Path):
        self.project_root = project_root
        self.manifest_file = manifest_file

    def sync(self, current_map: dict):
        """Surgically updates MANIFEST.md with all discovered READMEs."""
        if not self.manifest_file.exists():
            return

        try:
            # 1. Collect all paths with READMEs
            discovered_readmes = []
            for path, info in current_map.items():
                if info.get("has_readme"):
                    # Use absolute paths for file links as per project standards
                    abs_path = self.project_root / path
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
                    if line.startswith("---") or (
                        line.startswith("## ") and "(Auto-Synced)" not in line
                    ):
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
            print(
                f"[MANIFEST] Synced {len(formatted_entries)} READMEs to governance/MANIFEST.md"
            )

        except Exception as e:
            print(f"[ERROR] Manifest sync failed: {e}")
