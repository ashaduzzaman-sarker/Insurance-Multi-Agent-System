# ============================================================================
# FILE: core/audit.py
# ============================================================================
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from core.models import CanonicalCase

class AuditLogger:
    """Immutable audit trail for regulatory compliance."""
    
    def __init__(self, storage_path: str = "./data/audit"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def log_case_creation(self, case: CanonicalCase):
        """Log case creation event."""
        self._write_log({
            "event": "CASE_CREATED",
            "case_id": case.case_id,
            "engine": case.engine.value,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_agent_execution(self, case_id: str, agent_name: str, result: Dict[str, Any]):
        """Log agent execution."""
        self._write_log({
            "event": "AGENT_EXECUTION",
            "case_id": case_id,
            "agent": agent_name,
            "timestamp": datetime.utcnow().isoformat(),
            "confidence": result.get("confidence"),
            "success": result.get("success", True)
        })
    
    def log_human_decision(self, case_id: str, decision: str, justification: str, user_id: str):
        """Log human decision (critical for compliance)."""
        self._write_log({
            "event": "HUMAN_DECISION",
            "case_id": case_id,
            "decision": decision,
            "justification": justification,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def _write_log(self, entry: Dict[str, Any]):
        """Write to immutable log file."""
        log_file = self.storage_path / f"{datetime.utcnow().strftime('%Y-%m-%d')}_audit.jsonl"
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def get_case_audit_trail(self, case_id: str) -> list:
        """Retrieve full audit trail for a case."""
        trail = []
        for log_file in sorted(self.storage_path.glob("*_audit.jsonl")):
            with open(log_file) as f:
                for line in f:
                    entry = json.loads(line)
                    if entry.get("case_id") == case_id:
                        trail.append(entry)
        return trail
