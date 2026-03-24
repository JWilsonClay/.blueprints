# contentflow/governance/best_practices_auditor.py
from pathlib import Path
import subprocess
import json
import re
from typing import List, Dict, Optional
from datetime import datetime

class BestPracticesAuditor:
    """
    Lightweight qualitative audit ("The Workout").
    Runs targeted Ruff + Radon checks on drifted/new/modified .py files.
    Categorizes findings by doctrine priority.
    """

    # Hardcoded sensible thresholds (no config file)
    CC_VIOLATION_THRESHOLD = 15      # >15 -> violation (long/complex method smell, KISS/SOLID)
    MI_WARNING_THRESHOLD = 50         # <50 -> warning (harder to maintain)
    RUFF_OUTPUT_FORMAT = "json"

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.results: Dict = {
            "timestamp": datetime.now().isoformat(),
            "doctrines": {
                "PEP8": [],           # Ruff style/import/fixable issues
                "SoC": [],            # Relative imports, cross-layer (custom grep or Ruff rules)
                "SOLID_KISS": [],     # High CC, low MI
                "DRY": [],            # Future placeholder (Ruff lacks native dup detection -> phase 2)
                "YAGNI": [],          # Future (unused code via vulture or Ruff unused)
            },
            "summary": {"violations": 0, "warnings": 0, "auto_fixable": 0}
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
        self._run_composition_root_audit(py_files)

        # Count totals
        for cat in self.results["doctrines"].values():
            self.results["summary"]["violations"] += len([v for v in cat if "violation" in v.get("level", "")])
            self.results["summary"]["warnings"] += len([v for v in cat if "warning" in v.get("level", "")])

        return self.results

    def _run_ruff(self, files: List[Path]):
        """Ruff: PEP8, imports (SoC hints), basic complexity/bugs."""
        cmd = [
            "ruff", "check",
            "--output-format", self.RUFF_OUTPUT_FORMAT,
            "--select", "E,F,I,UP,B,ANN",  # Errors, flake8, isort, pyupgrade, bugbear, annotations (optional)
            "--ignore", "E501",             # Let formatter handle line-length if using ruff format later
        ]
        if len(files) < 20:  # Small set -> list files; else scan dirs
            cmd.extend(str(f) for f in files)
        else:
            cmd.append(str(self.project_root / "contentflow"))  # Or drifted dirs

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
                    self.results["doctrines"][cat].append({
                        "file": issue["filename"],
                        "line": issue["location"]["row"],
                        "message": issue["message"],
                        "rule": rule,
                        "level": "violation" if "fix" not in issue else "auto_fixable"
                    })
        except Exception as e:
            self.results["doctrines"]["PEP8"].append({"error": f"Ruff failed: {str(e)}"})

    def _run_radon(self, files: List[Path]):
        """Radon: CC and MI for SOLID/KISS."""
        for file_path in files:
            try:
                # radon cc --json
                cc_out = subprocess.run(
                    ["radon", "cc", "--json", str(file_path)],
                    capture_output=True, text=True, check=True
                )
                cc_data = json.loads(cc_out.stdout)
                for func, metrics in cc_data.items():
                    cc = metrics.get("complexity", 0)
                    if cc > self.CC_VIOLATION_THRESHOLD:
                        self.results["doctrines"]["SOLID_KISS"].append({
                            "file": str(file_path),
                            "function": func,
                            "cc": cc,
                            "level": "violation",
                            "message": f"High cyclomatic complexity (exceeds {self.CC_VIOLATION_THRESHOLD})"
                        })

                # radon mi --json
                mi_out = subprocess.run(
                    ["radon", "mi", "--json", str(file_path)],
                    capture_output=True, text=True, check=True
                )
                mi_data = json.loads(mi_out.stdout)
                mi_score = mi_data.get("MI", 100)
                if mi_score < self.MI_WARNING_THRESHOLD:
                    self.results["doctrines"]["SOLID_KISS"].append({
                        "file": str(file_path),
                        "mi": mi_score,
                        "level": "warning",
                        "message": f"Low maintainability index (below {self.MI_WARNING_THRESHOLD})"
                    })
            except Exception as e:
                self.results["doctrines"]["SOLID_KISS"].append({"error": f"Radon failed on {file_path}: {str(e)}"})

    def _run_composition_root_audit(self, files: List[Path]):
        """Detects manual service instantiation outside the core context."""
        patterns = {
            r"ChromaManager\(\)": "Manual ChromaManager instantiation detected.",
            r"LLMStructuredInterface\(": "Manual LLMStructuredInterface instantiation detected.",
            r"IntegrityTools\(": "Manual IntegrityTools instantiation detected.",
            r'with open\(.*config\.yaml"': "Manual config.yaml loading detected."
        }
        
        for file_path in files:
            # Skip the context provider itself to avoid recursive flagging
            if "contentflow/core/context.py" in str(file_path):
                continue
                
            try:
                content = file_path.read_text()
                lines = content.splitlines()
                
                for i, line in enumerate(lines):
                    for pattern, message in patterns.items():
                        if re.search(pattern, line):
                            self.results["doctrines"]["DRY"].append({
                                "file": str(file_path),
                                "line": i + 1,
                                "message": f"Composition Root Violation: {message} Use ContentFlowContext.get_instance().",
                                "level": "violation"
                            })
            except Exception as e:
                self.results["doctrines"]["DRY"].append({"error": f"CompRoot audit failed on {file_path}: {str(e)}"})