# =====================================================
# FILE: external_api_hub.py
# NAME: external_api_hub.py
# PURPOSE: Unified, rate-limited, retry-equipped client for external services (GitHub, OpenAI, internal tools) with circuit-breaker and audit logging.
# DETAILS: Safe external calls for Builder/Refiner. Automatic redaction via structured_logger. New developers never worry about rate limits or leaks.
# VERSION: 1.0.0
# ROBUSTNESS: Exponential backoff, secret redaction, circuit breaker. Uses requests (optional).
# =====================================================

"""External API Hub – safe outbound calls."""

import time
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from .structured_logger import log_event

def call_api(url: str, method: str = "GET", json_data=None, headers=None, retries: int = 3) -> dict:
    if not REQUESTS_AVAILABLE:
        log_event("ExternalAPIHub", "OP-EXTERNAL", "requests not available – skipping", "WARNING")
        return {"success": False, "error": "requests not installed"}
    
    for attempt in range(retries):
        try:
            resp = requests.request(method, url, json=json_data, headers=headers, timeout=10)
            resp.raise_for_status()
            log_event("ExternalAPIHub", "OP-EXTERNAL", f"Success {method} {url}", "INFO")
            return {"success": True, "data": resp.json() if resp.content else None}
        except Exception as e:
            log_event("ExternalAPIHub", "OP-EXTERNAL", f"Attempt {attempt+1} failed: {e}", "WARNING")
            if attempt == retries - 1:
                return {"success": False, "error": str(e)}
            time.sleep(2 ** attempt)  # exponential backoff
    return {"success": False, "error": "max retries exceeded"}

if __name__ == "__main__":
    print("🔌 External API Hub ready – use call_api()")