# ============================================================================
# FILE: core/security.py
# ============================================================================
import re
from typing import Dict, List, Any

class PIIMasker:
    """PII detection and masking using regex patterns (Presidio-style).
    
    For production, integrate actual Presidio library.
    """
    
    PII_PATTERNS = {
        "NID": r"\\b\\d{10}\\b|\\b\\d{13}\\b|\\b\\d{17}\\b",  # Bangladesh NID formats
        "PHONE": r"\\b01[3-9]\\d{8}\\b",  # Bangladesh mobile
        "EMAIL": r"\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b",
        "PASSPORT": r"\\b[A-Z]{1,2}\\d{7}\\b",
        "BANK_ACCOUNT": r"\\b\\d{10,16}\\b",
    }
    
    @classmethod
    def mask_text(cls, text: str) -> str:
        """Mask PII in text."""
        if not text:
            return text
            
        masked = text
        for pii_type, pattern in cls.PII_PATTERNS.items():
            masked = re.sub(pattern, f"[{pii_type}_REDACTED]", masked)
        return masked
    
    @classmethod
    def mask_dict(cls, data: Dict[str, Any], fields_to_mask: List[str]) -> Dict[str, Any]:
        """Mask specific fields in a dictionary."""
        masked_data = data.copy()
        for field in fields_to_mask:
            if field in masked_data and isinstance(masked_data[field], str):
                masked_data[field] = cls.mask_text(masked_data[field])
        return masked_data
    
    @classmethod
    def detect_pii(cls, text: str) -> List[Dict[str, str]]:
        """Detect PII entities in text."""
        findings = []
        for pii_type, pattern in cls.PII_PATTERNS.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                findings.append({
                    "type": pii_type,
                    "value": match.group(),
                    "start": match.start(),
                    "end": match.end()
                })
        return findings