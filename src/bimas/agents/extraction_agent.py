# ============================================================================
# FILE: agents/extraction_agent.py
# ============================================================================
from agents.base_agent import BaseAgent
from core.models import CanonicalCase, ExtractedFields
from typing import Dict, Any, List
import json
import re

class ExtractionAgent(BaseAgent):
    """Extracts structured data from documents using OCR + LLM.
    
    In production: Use Qwen/GPT-4o for vision + extraction.
    This stub simulates extraction logic.
    """
    
    def __init__(self):
        super().__init__("ExtractionAgent")
    
    def execute(self, case: CanonicalCase) -> Dict[str, Any]:
        """Extract fields from uploaded documents."""
        try:
            # Simulate document text extraction
            # In production: Use pytesseract, GPT-4o vision, etc.
            extracted_data = self._mock_extraction(case)
            
            # Validate extracted data
            confidence = self._calculate_confidence(extracted_data)
            
            # Update case
            case.extracted_fields = ExtractedFields(**extracted_data)
            
            result = {
                "success": True,
                "confidence": confidence,
                "data": extracted_data,
                "evidence": [doc.filename for doc in case.documents],
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
    
    def _mock_extraction(self, case: CanonicalCase) -> Dict[str, Any]:
        """Mock extraction for demonstration.
        
        In production: Call LLM with document images/text.
        """
        # Simulate extracted fields
        return {
            "claimant_name": "Rahim Ahmed",
            "claimant_nid": "19921234567890",
            "policy_number": "POL-BD-2024-12345",
            "incident_date": "2025-01-15",
            "incident_location": "Dhaka, Bangladesh",
            "claimed_amount": 75000.0,
            "loss_description": "Vehicle accident on Mirpur Road, front damage",
            "medical_diagnosis": None,
            "vehicle_details": {
                "make": "Toyota",
                "model": "Corolla",
                "year": 2020,
                "registration": "Dhaka-Metro-GA-12-3456"
            }
        }
    
    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate extraction confidence based on field completeness."""
        required_fields = ["claimant_name", "policy_number", "incident_date", "claimed_amount"]
        filled_fields = sum(1 for field in required_fields if data.get(field))
        return filled_fields / len(required_fields)
