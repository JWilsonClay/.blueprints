# governance/thedoorway/best_practices_auditor.py
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List


class BestPracticesAuditor:
    """
    Lightweight qualitative audit ("The Workout").
    Runs targeted Ruff + Radon checks on drifted/new/modified .py files.
    Categorizes findings by doctrine priority.
    """

    # Hardcoded sensible thresholds (no config file)
    CC_VIOLATION_THRESHOLD = (
        15  # >15 -> violation (long/complex method smell, KISS/SOLID)
    )
    MI_WARNING_THRESHOLD = 50  # <50 -> warning (harder to maintain)
    RUFF_OUTPUT_FORMAT = "json"

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results: Dict = {
            "timestamp": datetime.now().isoformat(),
            "doctrines": {
                "PEP8": [],  # Ruff style/import/fixable issues
                "SoC": [],  # Relative imports, cross-layer (custom grep or Ruff rules)
                "SOLID_KISS": [],  # High CC, low MI
                "DRY": [],  # Detection of old-workspace contamination
                "YAGNI": [],  # Future (unused code via vulture or Ruff unused)
            },
            "summary": {"violations": 0, "warnings": 0, "auto_fixable": 0},
        }

    def run(self, audit_files: List[Path], full_scan: bool = False) -> Dict:
        """Main entry: analyze only relevant files."""
        if not audit_files:
            return {"status": "no_files_to_audit", **self.results}

        py_files = [f for f in audit_files if f.suffix == ".py" and f.is_file()]
        if not py_files:
            return {"status": "no_python_files", **self.results}

        self._run_ruff(py_files)
        self._run_radon(py_files)
        self._run_contamination_audit(py_files)

        # Count totals
        for cat in self.results["doctrines"].values():
            self.results["summary"]["violations"] += len(
                [v for v in cat if "violation" in v.get("level", "")]
            )
            self.results["summary"]["warnings"] += len(
                [v for v in cat if "warning" in v.get("level", "")]
            )

        return self.results

    def _run_ruff(self, files: List[Path]):
        """Ruff: PEP8, imports (SoC hints), basic complexity/bugs."""
        cmd = [
            "ruff",
            "check",
            "--output-format",
            self.RUFF_OUTPUT_FORMAT,
            "--select",
            "E,F,I,UP,B,ANN",  # Errors, flake8, isort, pyupgrade, bugbear, annotations
            "--ignore",
            "E501",  # Let formatter handle line-length
        ]
        if len(files) < 20:  # Small set -> list files; else scan root
            cmd.extend(str(f) for f in files)
        else:
            cmd.append(str(self.project_root))

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if result.returncode == 0 or result.returncode == 1:  # 1 = issues found
                data = json.loads(result.stdout or "[]")
                for issue in data:
                    rule = issue.get("code", "")
                    if rule.startswith(("E", "W")):
                        cat = "PEP8"
                    elif rule.startswith("I"):
                        cat = "SoC"  # Import order violations hint at SoC issues
                    else:
                        cat = "SOLID_KISS"  # Bugbear or other smells
                    self.results["doctrines"][cat].append(
                        {
                            "file": issue["filename"],
                            "line": issue["location"]["row"],
                            "message": issue["message"],
                            "rule": rule,
                            "level": "violation"
                            if "fix" not in issue
                            else "auto_fixable",
                        }
                    )
        except Exception as e:
            self.results["doctrines"]["PEP8"].append(
                {"error": f"Ruff failed: {str(e)}"}
            )

    def _run_radon(self, files: List[Path]):
        """Radon: CC and MI for SOLID/KISS."""
        for file_path in files:
            try:
                # radon cc --json
                cc_out = subprocess.run(
                    ["radon", "cc", "--json", str(file_path)],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                cc_data = json.loads(cc_out.stdout)
                # Results can be a list of dicts for the file
                for item in cc_data.get(str(file_path), []):
                    cc = item.get("complexity", 0)
                    if cc > self.CC_VIOLATION_THRESHOLD:
                        self.results["doctrines"]["SOLID_KISS"].append(
                            {
                                "file": str(file_path),
                                "function": item.get("name", "unknown"),
                                "cc": cc,
                                "level": "violation",
                                "message": f"High cyclomatic complexity (exceeds {self.CC_VIOLATION_THRESHOLD})",
                            }
                        )

                # radon mi --json
                mi_out = subprocess.run(
                    ["radon", "mi", "--json", str(file_path)],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                mi_data = json.loads(mi_out.stdout)
                file_mi = mi_data.get(str(file_path), {})
                mi_score = file_mi.get("mi", 100)
                if mi_score < self.MI_WARNING_THRESHOLD:
                    self.results["doctrines"]["SOLID_KISS"].append(
                        {
                            "file": str(file_path),
                            "mi": mi_score,
                            "level": "warning",
                            "message": f"Low maintainability index (below {self.MI_WARNING_THRESHOLD})",
                        }
                    )
            except Exception as e:
                self.results["doctrines"]["SOLID_KISS"].append(
                    {"error": f"Radon failed on {file_path}: {str(e)}"}
                )

    def _run_contamination_audit(self, files: List[Path]):
        """Option A: Detects old-workspace path strings and package references."""
        patterns = {
            r"/home/jwils/Public/langgraph-social-agent": "Old workspace absolute path found.",
            r"contentflow": "Old package reference 'contentflow' found.",
            r"langgraph-social-agent": "Old workspace name 'langgraph-social-agent' found.",
        }

        for file_path in files:
            try:
                content = file_path.read_text()
                lines = content.splitlines()

                for i, line in enumerate(lines):
                    for pattern, message in patterns.items():
                        if re.search(pattern, line):
                            self.results["doctrines"]["DRY"].append(
                                {
                                    "file": str(file_path),
                                    "line": i + 1,
                                    "message": f"Contamination Violation: {message} Purge and reprogram for .blueprints.",
                                    "level": "violation",
                                }
                            )
            except Exception as e:
                self.results["doctrines"]["DRY"].append(
                    {"error": f"Contamination audit failed on {file_path}: {str(e)}"}
                )
