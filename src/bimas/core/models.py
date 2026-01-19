# ============================================================================
# FILE: core/models.py
# ============================================================================
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Literal
from datetime import datetime
from enum import Enum
import uuid

class BusinessEngine(str, Enum):
    UNDERWRITING = "UNDERWRITING"
    CLAIMS = "CLAIMS"
    POLICY_ADMIN = "POLICY_ADMIN"

class WorkflowStage(str, Enum):
    FNOL = "FNOL"  # First Notice of Loss
    EXTRACTION = "EXTRACTION"
    POLICY_CHECK = "POLICY_CHECK"
    RISK = "RISK"
    COMPLIANCE = "COMPLIANCE"
    DECISION = "DECISION"
    HUMAN = "HUMAN"
    COMPLETED = "COMPLETED"

class NextAction(str, Enum):
    AUTO_ASSIST = "AUTO_ASSIST"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    REJECT = "REJECT"

class AuditEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent: str
    action: str
    details: Dict[str, Any]
    confidence: Optional[float] = None

class DocumentMetadata(BaseModel):
    doc_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    doc_type: str  # claim_form, medical_report, police_report, etc.
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    file_path: Optional[str] = None

class ExtractedFields(BaseModel):
    claimant_name: Optional[str] = None
    claimant_nid: Optional[str] = None  # National ID (Bangladesh)
    policy_number: Optional[str] = None
    incident_date: Optional[str] = None
    incident_location: Optional[str] = None
    claimed_amount: Optional[float] = None
    loss_description: Optional[str] = None
    medical_diagnosis: Optional[str] = None
    vehicle_details: Optional[Dict[str, Any]] = None
    witnesses: Optional[List[str]] = None

class PolicyClause(BaseModel):
    clause_id: str
    section: str
    text: str
    relevance_score: float
    source_page: Optional[int] = None

class RiskFlag(BaseModel):
    flag_type: str  # fraud, inconsistency, missing_data, high_amount
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    description: str
    evidence: List[str]

class CanonicalCase(BaseModel):
    # Identity
    case_id: str = Field(default_factory=lambda: f"CASE-{uuid.uuid4().hex[:12].upper()}")
    engine: BusinessEngine
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Workflow State
    stage: WorkflowStage = WorkflowStage.FNOL
    
    # Core Data
    policy_id: Optional[str] = None
    documents: List[DocumentMetadata] = Field(default_factory=list)
    
    # Agent Outputs
    extracted_fields: ExtractedFields = Field(default_factory=ExtractedFields)
    policy_clauses: List[PolicyClause] = Field(default_factory=list)
    risk_flags: List[RiskFlag] = Field(default_factory=list)
    
    # Decision Data
    calculated_payout: Optional[float] = None
    recommended_action: Optional[str] = None
    confidence_score: float = 0.0
    human_review_required: bool = True
    
    # Compliance
    pii_masked: bool = False
    regulatory_checks: Dict[str, bool] = Field(default_factory=dict)
    
    # Audit Trail (IMMUTABLE)
    audit_log: List[AuditEntry] = Field(default_factory=list)
    
    def add_audit_entry(self, agent: str, action: str, details: Dict[str, Any], confidence: Optional[float] = None):
        entry = AuditEntry(agent=agent, action=action, details=details, confidence=confidence)
        self.audit_log.append(entry)
        self.updated_at = datetime.utcnow()
    
    def update_stage(self, new_stage: WorkflowStage):
        self.add_audit_entry(
            agent="ORCHESTRATOR",
            action="STAGE_TRANSITION",
            details={"from": self.stage.value, "to": new_stage.value}
        )
        self.stage = new_stage
