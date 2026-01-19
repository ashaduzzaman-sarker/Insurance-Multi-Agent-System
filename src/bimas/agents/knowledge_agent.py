# ============================================================================
# FILE: agents/knowledge_agent.py
# ============================================================================
from agents.base_agent import BaseAgent
from core.models import CanonicalCase, PolicyClause
from typing import Dict, Any, List
import numpy as np

class KnowledgeAgent(BaseAgent):
    """Retrieves relevant policy clauses using RAG.
    
    In production: Use actual vector DB (FAISS, Pinecone, Weaviate).
    """
    
    def __init__(self, vector_store=None):
        super().__init__("KnowledgeAgent")
        self.vector_store = vector_store  # Mock for now
    
    def execute(self, case: CanonicalCase) -> Dict[str, Any]:
        """Retrieve relevant policy clauses."""
        try:
            query = self._build_query(case)
            clauses = self._retrieve_clauses(query, case.policy_id)
            
            # Update case
            case.policy_clauses = clauses
            
            result = {
                "success": True,
                "confidence": self._calculate_retrieval_confidence(clauses),
                "data": {"clauses": [c.dict() for c in clauses]},
                "evidence": [f"Clause {c.clause_id}" for c in clauses],
                "errors": []
            }
            
            self.log_execution(case, result)
            return result
            
        except Exception as e:
            result = {
                "success": False,
                "confidence": 0.0,
                "data": {},
                "evidence": [],
                "errors": [str(e)]
            }
            self.log_execution(case, result)
            return result
    
    def _build_query(self, case: CanonicalCase) -> str:
        """Build retrieval query from case data."""
        query_parts = []
        
        if case.extracted_fields.loss_description:
            query_parts.append(case.extracted_fields.loss_description)
        
        if case.extracted_fields.vehicle_details:
            query_parts.append("vehicle damage claim")
        
        return " ".join(query_parts)
    
    def _retrieve_clauses(self, query: str, policy_id: str) -> List[PolicyClause]:
        """Mock retrieval from vector store.
        
        In production: Use FAISS/Pinecone similarity search.
        """
        # Mock policy clauses
        return [
            PolicyClause(
                clause_id="SEC-3-CLAUSE-2",
                section="Section 3: Motor Vehicle Coverage",
                text="The insurer shall cover damages to the insured vehicle resulting from collision, subject to deductible of BDT 5,000 and maximum limit of BDT 500,000.",
                relevance_score=0.92,
                source_page=12
            ),
            PolicyClause(
                clause_id="SEC-3-CLAUSE-5",
                section="Section 3: Motor Vehicle Coverage",
                text="Claims must be reported within 48 hours of incident. Late reporting may result in claim denial.",
                relevance_score=0.85,
                source_page=13
            ),
            PolicyClause(
                clause_id="SEC-5-CLAUSE-1",
                section="Section 5: Exclusions",
                text="This policy does not cover damages resulting from driving under the influence of alcohol or drugs.",
                relevance_score=0.78,
                source_page=22
            )
        ]
    
    def _calculate_retrieval_confidence(self, clauses: List[PolicyClause]) -> float:
        """Calculate confidence based on relevance scores."""
        if not clauses:
            return 0.0
        return sum(c.relevance_score for c in clauses) / len(clauses)

