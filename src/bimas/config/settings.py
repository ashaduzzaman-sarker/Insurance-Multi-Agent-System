# ============================================================================
# FILE: config/settings.py
# ============================================================================
import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # Model Configuration
    EXTRACTION_MODEL: str = "gpt-4o-mini"
    KNOWLEDGE_MODEL: str = "claude-sonnet-4-20250514"
    DECISION_MODEL: str = "claude-sonnet-4-20250514"
    
    # System Configuration
    CONFIDENCE_THRESHOLD_AUTO: float = 0.9
    CONFIDENCE_THRESHOLD_REVIEW: float = 0.5
    MAX_PAYOUT_AUTO_APPROVE: float = 50000.0  # BDT
    
    # Bangladesh Regulatory
    REGULATORY_FRAMEWORK: str = "IDRA"  # Insurance Development & Regulatory Authority
    PII_PROTECTION_LEVEL: str = "HIGH"
    AUDIT_RETENTION_DAYS: int = 2555  # 7 years
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost/bimas"
    
    # Vector Store
    VECTOR_STORE_PATH: str = "./data/vector_store"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Paths
    POLICY_DOCS_PATH: str = "./data/policies"
    CASE_STORAGE_PATH: str = "./data/cases"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()