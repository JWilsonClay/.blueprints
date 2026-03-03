# =====================================================
# FILE: visualization_renderer.py
# NAME: visualization_renderer.py
# PURPOSE: Wrapper for backend Mermaid diagram generator.
# DETAILS: Intake gets architecture, Planning gets Gantt.
# VERSION: 1.0.1
# =====================================================

"""Visualization Renderer – dynamic diagrams for agents."""

import sys
from pathlib import Path

# Path injection
BLUEPRINT_ROOT = Path(__file__).parent.parent
if str(BLUEPRINT_ROOT) not in sys.path:
    sys.path.append(str(BLUEPRINT_ROOT))

try:
    from toolkits.audit_onboarding.dependency_visualizer import generate_mermaid_graph
except ImportError:
    def generate_mermaid_graph(nodes): return "graph TD\n    A[Unknown] --> B[Unknown]"

from .session_manager import get_session

def render_architecture(user_id: str) -> str:
    """Wrap backend visualizer for architecture diagrams."""
    session = get_session(user_id)
    # Extract nodes from session requirements
    nodes = [req['name'] for req in session.get("requirements", [])]
    if not nodes:
        return "```mermaid\ngraph TD\n    Start[Awaiting Discovery]\n```"
    
    # Use backend power
    mermaid_body = generate_mermaid_graph(nodes)
    return f"```mermaid\n{mermaid_body}\n```"

def render_gantt(user_id: str) -> str:
    """Renders sequence Gantt charts (Fallback for now)."""
    return "```mermaid\ngantt\n    title Project Roadmap\n    section Planning\n    Sequence Definition :active, 2026-03-02, 3d\n```"