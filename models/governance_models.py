"""
Governance Models for LLM Governance and Guardrails
Comprehensive framework for responsible AI implementation
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class GuardrailType(str, Enum):
    """Types of guardrails"""
    INPUT = "input"
    OUTPUT = "output"
    MODEL = "model"
    BEHAVIORAL = "behavioral"


class SeverityLevel(str, Enum):
    """Severity levels for violations"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class InputGuardrail(BaseModel):
    """Input guardrails for LLM requests"""
    guardrail_id: str
    name: str
    description: Optional[str] = None
    enabled: bool = True
    severity: SeverityLevel = SeverityLevel.WARNING
    
    # Validation rules
    max_input_length: Optional[int] = Field(None, description="Maximum input length in characters")
    min_input_length: Optional[int] = Field(None, description="Minimum input length in characters")
    
    # Content filtering
    blocked_keywords: List[str] = Field(default_factory=list, description="Keywords to block")
    blocked_patterns: List[str] = Field(default_factory=list, description="Regex patterns to block")
    allowed_languages: List[str] = Field(default_factory=list, description="Allowed languages (ISO 639-1)")
    
    # Security checks
    sql_injection_check: bool = False
    prompt_injection_check: bool = True
    xss_check: bool = False
    
    # PII handling
    pii_detection_enabled: bool = True
    pii_masking_enabled: bool = False
    pii_types_to_mask: List[str] = Field(default_factory=list)  # email, phone, ssn, credit_card, etc.
    
    # Validation
    require_authentication: bool = False
    rate_limit_per_minute: Optional[int] = None
    rate_limit_per_hour: Optional[int] = None


class OutputGuardrail(BaseModel):
    """Output guardrails for LLM responses"""
    guardrail_id: str
    name: str
    description: Optional[str] = None
    enabled: bool = True
    severity: SeverityLevel = SeverityLevel.WARNING
    
    # Length constraints
    max_output_length: Optional[int] = Field(None, description="Maximum output length in characters")
    min_output_length: Optional[int] = Field(None, description="Minimum output length in characters")
    
    # Content validation
    blocked_output_keywords: List[str] = Field(default_factory=list)
    blocked_output_patterns: List[str] = Field(default_factory=list)
    required_keywords: List[str] = Field(default_factory=list)
    
    # Quality checks
    hallucination_detection: bool = True
    hallucination_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    
    bias_detection: bool = True
    bias_categories: List[str] = Field(default_factory=list)  # gender, race, age, etc.
    
    toxicity_detection: bool = True
    toxicity_threshold: float = Field(default=0.5, ge=0.0, le=1.0)
    
    # Format validation
    expected_format: Optional[str] = None  # json, markdown, plain_text, html
    validate_json_schema: Optional[Dict[str, Any]] = None
    
    # PII in output
    pii_in_output_allowed: bool = False
    redact_pii_in_output: bool = True
    
    # Citation requirements
    require_citations: bool = False
    citation_format: Optional[str] = None  # inline, footnote, endnote


class ModelGuardrail(BaseModel):
    """Model-level guardrails"""
    guardrail_id: str
    name: str
    description: Optional[str] = None
    enabled: bool = True
    
    # Cost control
    max_tokens_per_request: Optional[int] = None
    max_tokens_per_day: Optional[int] = None
    max_cost_per_request: Optional[float] = None
    max_cost_per_day: Optional[float] = None
    
    # Rate limiting
    max_requests_per_minute: Optional[int] = None
    max_requests_per_hour: Optional[int] = None
    max_concurrent_requests: Optional[int] = None
    
    # Timeout
    request_timeout_seconds: int = Field(default=30, ge=1, le=300)
    
    # Model constraints
    allowed_models: List[str] = Field(default_factory=list)
    temperature_range: tuple = Field(default=(0.0, 2.0))
    top_p_range: tuple = Field(default=(0.0, 1.0))
    
    # Fallback strategy
    enable_fallback: bool = True
    fallback_model: Optional[str] = None
    fallback_strategy: str = Field(default="retry")  # retry, cached, degraded


class BehavioralGuardrail(BaseModel):
    """Behavioral guardrails for agent behavior"""
    guardrail_id: str
    name: str
    description: Optional[str] = None
    enabled: bool = True
    severity: SeverityLevel = SeverityLevel.WARNING
    
    # Action constraints
    allowed_actions: List[str] = Field(default_factory=list)
    blocked_actions: List[str] = Field(default_factory=list)
    
    # State constraints
    max_state_size_mb: Optional[float] = None
    max_iterations: Optional[int] = None
    max_tool_calls: Optional[int] = None
    
    # Resource constraints
    max_memory_mb: Optional[float] = None
    max_cpu_percent: Optional[float] = None
    
    # Safety constraints
    require_approval_for_actions: List[str] = Field(default_factory=list)
    audit_all_actions: bool = True
    
    # Escalation
    escalation_enabled: bool = True
    escalation_threshold: int = Field(default=3, ge=1)
    escalation_action: str = Field(default="notify_admin")


class CompliancePolicy(BaseModel):
    """Compliance policy for governance"""
    policy_id: str
    policy_name: str
    description: Optional[str] = None
    enabled: bool = True
    
    # Regulatory compliance
    gdpr_compliant: bool = False
    hipaa_compliant: bool = False
    sox_compliant: bool = False
    ccpa_compliant: bool = False
    
    # Data handling
    data_retention_days: Optional[int] = None
    data_encryption_required: bool = True
    encryption_algorithm: str = Field(default="AES-256")
    
    # Audit requirements
    audit_logging_enabled: bool = True
    audit_retention_days: int = Field(default=90, ge=1)
    
    # Approval workflows
    require_approval: bool = False
    approval_roles: List[str] = Field(default_factory=list)
    approval_timeout_hours: Optional[int] = None


class LLMGovernanceFramework(BaseModel):
    """Comprehensive LLM Governance Framework"""
    framework_id: str
    framework_name: str
    description: Optional[str] = None
    version: str = Field(default="1.0")
    enabled: bool = True
    
    # Guardrails
    input_guardrails: List[InputGuardrail] = Field(default_factory=list)
    output_guardrails: List[OutputGuardrail] = Field(default_factory=list)
    model_guardrails: List[ModelGuardrail] = Field(default_factory=list)
    behavioral_guardrails: List[BehavioralGuardrail] = Field(default_factory=list)
    
    # Compliance
    compliance_policies: List[CompliancePolicy] = Field(default_factory=list)
    
    # Monitoring
    enable_monitoring: bool = True
    monitoring_metrics: List[str] = Field(default_factory=list)  # latency, cost, errors, etc.
    alert_thresholds: Dict[str, float] = Field(default_factory=dict)
    
    # Logging
    enable_detailed_logging: bool = True
    log_retention_days: int = Field(default=30, ge=1)
    log_sensitive_data: bool = False
    
    # Feedback loop
    enable_feedback_collection: bool = True
    feedback_categories: List[str] = Field(default_factory=list)
    
    class Config:
        use_enum_values = True


class GovernanceViolation(BaseModel):
    """Record of a governance violation"""
    violation_id: str
    timestamp: str
    guardrail_id: str
    guardrail_name: str
    violation_type: GuardrailType
    severity: SeverityLevel
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    violation_details: Dict[str, Any] = Field(default_factory=dict)
    action_taken: Optional[str] = None
    resolved: bool = False


class GovernanceReport(BaseModel):
    """Governance compliance report"""
    report_id: str
    report_date: str
    framework_id: str
    total_requests: int
    violations_count: int
    critical_violations: int
    warnings_count: int
    compliance_score: float = Field(ge=0.0, le=100.0)
    violations: List[GovernanceViolation] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


def create_default_governance_framework() -> LLMGovernanceFramework:
    """Create a default governance framework"""
    return LLMGovernanceFramework(
        framework_id="default_framework",
        framework_name="Default LLM Governance Framework",
        description="Default framework with standard guardrails",
        input_guardrails=[
            InputGuardrail(
                guardrail_id="input_1",
                name="Input Length Validation",
                max_input_length=10000,
                min_input_length=1,
                prompt_injection_check=True
            )
        ],
        output_guardrails=[
            OutputGuardrail(
                guardrail_id="output_1",
                name="Output Quality Check",
                max_output_length=5000,
                hallucination_detection=True,
                toxicity_detection=True
            )
        ],
        model_guardrails=[
            ModelGuardrail(
                guardrail_id="model_1",
                name="Model Resource Control",
                max_tokens_per_request=2000,
                request_timeout_seconds=60,
                max_requests_per_minute=60
            )
        ]
    )


def validate_governance_framework(framework: LLMGovernanceFramework) -> Dict[str, Any]:
    """Validate governance framework configuration"""
    errors = []
    warnings = []
    
    if not framework.input_guardrails and not framework.output_guardrails:
        warnings.append("No input or output guardrails defined")
    
    if not framework.enable_monitoring:
        warnings.append("Monitoring is disabled - compliance tracking may be limited")
    
    if not framework.enable_detailed_logging:
        warnings.append("Detailed logging is disabled - audit trail may be incomplete")
    
    # Check for conflicting settings
    for policy in framework.compliance_policies:
        if policy.gdpr_compliant and not framework.enable_detailed_logging:
            errors.append("GDPR compliance requires detailed logging to be enabled")
        if policy.data_encryption_required and not framework.input_guardrails:
            warnings.append("Data encryption is required but no input guardrails are defined")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "framework_id": framework.framework_id
    }
