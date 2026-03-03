# =====================================================
# FILE: schemas.py
# NAME: schemas.py
# PURPOSE: Rigid Pydantic state definitions for the Frontend Orchestration Layer.
# DETAILS: Ensures all agent payloads are grounded and verifiable.
# VERSION: 1.0.0
# =====================================================

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ProvenanceHeader(BaseModel):
    agent_version: str = "1.0.0"
    timestamp: str
    protocol_reference: str
    target_audience: str

class DiscoveryPayload(BaseModel):
    project_name: str
    requirements: List[Dict[str, Any]]
    tech_stack: Dict[str, str]

class SequencePayload(BaseModel):
    sequence_id: str
    tasks: List[Dict[str, Any]]
    priority: str

class DebugEventPayload(BaseModel):
    filename: str
    error_context: str
    suggested_fix: Optional[str] = None
    estimated_impact: float

class SessionState(BaseModel):
    user_id: str
    requirements: List[Dict[str, Any]] = []
    sequence: List[Dict[str, Any]] = []
    debug_log: List[Dict[str, Any]] = []
    last_updated: str
