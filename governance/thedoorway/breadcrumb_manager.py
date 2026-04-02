# governance/thedoorway/breadcrumb_manager.py
from pathlib import Path

class BreadcrumbManager:
    """
    Handles breadcrumb orchestration for the Doorway Protocol.
    Responsible for logging proposals and auto-applying approved summaries to READMEs.
    """

    def __init__(self, project_root: Path, update_log_file: Path):
        self.project_root = project_root
        self.update_log = update_log_file

    def propose(self, folder_path: str, reason: str):
        """Logs a breadcrumb update request to the context log."""
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

    def apply_approved(self):
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
                prop_str = (
                    "--- PROPOSAL" + prop if not prop.startswith("Folder:") else prop
                )
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
                    if self.update_readme(folder, breadcrumb):
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

    def update_readme(self, folder_path_str: str, breadcrumb: str) -> bool:
        """Surgically updates the BREADCRUMB section in a README."""
        target = self.project_root / folder_path_str / "README.md"
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
                new_content = (
                    content.rstrip()
                    + f"\n\n## Contents\n{tag_start}\n{breadcrumb}\n{tag_end}\n"
                )
                target.write_text(new_content)
                return True
        except Exception:
            pass
        return False
