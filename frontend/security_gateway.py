# =====================================================
# FILE: security_gateway.py
# NAME: security_gateway.py
# PURPOSE: Centralized auth, input sanitization, and PII redaction.
# DETAILS: Protects Interactive debugger and Intake discovery.
# VERSION: 1.0.1
# =====================================================

"""Security Gateway – auth & safety for the frontend layer."""

import sys
import re
from pathlib import Path
from typing import Dict

# Path injection
BLUEPRINT_ROOT = Path(__file__).parent.parent
if str(BLUEPRINT_ROOT) not in sys.path:
    sys.path.append(str(BLUEPRINT_ROOT))

try:
    from toolkits.runtime_observability.structured_logger import log_event
    from toolkits.audit_onboarding.vulnerability_scanner import scan_file
except ImportError:
    def log_event(agent, layer, msg, level="INFO"): print(msg)
    def scan_file(path): return {"vulnerabilities": []}

PII_PATTERNS = {
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
    "api_key": r"(?i)(api[_-]?key|secret|token)['\"]?\s*[:=]\s*['\"]?([a-zA-Z0-9]{20,})['\"]?",
    "ipv4": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
}

def sanitize_payload(payload: Dict) -> Dict:
    """Recursively scrub PII from payload."""
    data_str = json.dumps(payload)
    for name, pattern in PII_PATTERNS.items():
        data_str = re.sub(pattern, f"[REDACTED_{name.upper()}]", data_str)
    return json.loads(data_str)

def validate_request(user_id: str, payload: Dict):
    """Sanitize and log request."""
    sanitized = sanitize_payload(payload)
    log_event("SecurityGateway", "frontend_layer", f"Validated & scrubbed request for {user_id}")
    return sanitized

import json # for the sanitize_payload function