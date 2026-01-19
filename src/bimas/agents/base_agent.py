# ============================================================================
# FILE: agents/base_agent.py
# ============================================================================
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from core.models import CanonicalCase
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in BIMAS.
    
    All agents MUST:
    - Operate on CanonicalCase
    - Return structured JSON with confidence
    - NEVER make final decisions
    - Add audit trail entries
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def execute(self, case: CanonicalCase) -> Dict[str, Any]:
        """Execute agent logic.
        
        Returns:
            {
                "success": bool,
                "confidence": float,
                "data": Any,
                "evidence": List[str],
                "errors": List[str]
            }
        """
        pass
    
    def log_execution(self, case: CanonicalCase, result: Dict[str, Any]):
        """Add execution to audit trail."""
        case.add_audit_entry(
            agent=self.name,
            action="EXECUTE",
            details={"result_summary": str(result.get("data", ""))[:200]},
            confidence=result.get("confidence")
        )
