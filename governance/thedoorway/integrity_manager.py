# governance/thedoorway/integrity_manager.py
from pathlib import Path

class IntegrityManager:
    """
    Handles substrate integrity and self-healing for the Doorway Protocol.
    Responsible for ensuring critical governance artifacts exist and recreating them from templates if missing.
    """

    def __init__(self, project_root: Path, primary_templates: Path, backup_templates: Path):
        self.project_root = project_root
        self.primary_templates = primary_templates
        self.backup_templates = backup_templates

    def ensure_substrate(self, data_dir: Path, critical_files: dict):
        """Self-Healing: Ensures core files and directories exist."""
        # 1. Ensure data directory
        if not data_dir.exists():
            data_dir.mkdir(parents=True, exist_ok=True)
            (data_dir / ".gitkeep").touch()
            print("[SELF-HEAL] Created missing data/ directory.")

        # 2. Ensure core governance files
        for file_path, template_name in critical_files.items():
            if not file_path.exists():
                self.heal(file_path, template_name)

    def heal(self, target_path: Path, template_name: str):
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
                print(
                    f"[SELF-HEAL] Primary template missing. Used backup for {target_path.name}."
                )

        if template_content:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(template_content)
            print(
                f"[SELF-HEAL] Recreated missing {target_path.relative_to(self.project_root)} from template."
            )
        else:
            print(
                f"[ERROR] Failed to heal {target_path.name}: No template found in primary or backup."
            )

    def create_readme(self, folder_path_str: str) -> bool:
        """Self-healing: Creates a standard README.md."""
        target = self.project_root / folder_path_str / "README.md"
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
            return True
        except Exception:
            return False
