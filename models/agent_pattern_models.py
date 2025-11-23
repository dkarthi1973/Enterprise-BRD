"""
Agent Pattern Models for Advanced AI Patterns
Supports ReAct, Plan-Execute, Hierarchical, RAG, and CRAG patterns
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class AgentPatternType(str, Enum):
    """Supported agent patterns"""
    REACT = "react"
    PLAN_EXECUTE = "plan_execute"
    HIERARCHICAL = "hierarchical"
    RAG = "rag"
    CRAG = "crag"


class ReActAction(BaseModel):
    """Action definition for ReAct pattern"""
    action_id: str
    action_name: str
    action_type: str  # API Call, Tool, Computation, Query
    description: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    expected_output: Optional[str] = None


class ReActPattern(BaseModel):
    """ReAct (Reason + Act) Pattern - Transparent decision-making"""
    pattern_id: str
    pattern_type: AgentPatternType = AgentPatternType.REACT
    description: Optional[str] = None
    reasoning_prompt: str
    available_actions: List[ReActAction] = Field(default_factory=list)
    max_reasoning_steps: int = Field(default=10, ge=1, le=100)
    termination_conditions: List[str] = Field(default_factory=list)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    
    class Config:
        use_enum_values = True


class ExecutionStep(BaseModel):
    """Execution step for Plan-Execute pattern"""
    step_id: str
    step_name: str
    description: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    timeout_seconds: Optional[int] = None
    retry_enabled: bool = False
    max_retries: int = 0
    parallel_execution: bool = False


class PlanExecutePattern(BaseModel):
    """Plan-and-Execute Pattern - Multi-step planning and execution"""
    pattern_id: str
    pattern_type: AgentPatternType = AgentPatternType.PLAN_EXECUTE
    description: Optional[str] = None
    execution_strategy: str  # sequential, parallel, adaptive
    max_plan_steps: int = Field(default=20, ge=1, le=100)
    allow_replanning: bool = True
    max_replans: int = Field(default=3, ge=0, le=10)
    planning_prompt: str
    execution_steps: List[ExecutionStep] = Field(default_factory=list)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    
    class Config:
        use_enum_values = True


class WorkerAgent(BaseModel):
    """Worker agent in hierarchical team"""
    worker_id: str
    worker_name: str
    specialization: str
    description: Optional[str] = None
    max_concurrent_tasks: int = Field(default=1, ge=1)
    capabilities: List[str] = Field(default_factory=list)
    performance_metrics: Optional[Dict[str, float]] = None


class HierarchicalPattern(BaseModel):
    """Hierarchical Agent Teams Pattern - Supervisor-worker model"""
    pattern_id: str
    pattern_type: AgentPatternType = AgentPatternType.HIERARCHICAL
    description: Optional[str] = None
    supervisor_name: str
    supervisor_role: str
    supervisor_authority: List[str] = Field(default_factory=list)  # routing, escalation, approval
    workers: List[WorkerAgent] = Field(default_factory=list)
    task_routing_rules: List[Dict[str, str]] = Field(default_factory=list)
    quality_assurance_enabled: bool = True
    escalation_rules: Optional[Dict[str, str]] = None
    model: Optional[str] = None
    
    class Config:
        use_enum_values = True


class DocumentSource(BaseModel):
    """Document source for RAG pattern"""
    source_id: str
    source_type: str  # database, api, file_system, web
    source_name: str
    connection_string: Optional[str] = None
    query_template: Optional[str] = None
    description: Optional[str] = None


class RetrievalStrategy(BaseModel):
    """Retrieval strategy for RAG pattern"""
    method: str  # semantic, bm25, hybrid, vector
    ranking_strategy: str  # bm25, similarity, relevance
    relevance_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    max_results: int = Field(default=10, ge=1, le=100)
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None


class GenerationStrategy(BaseModel):
    """Generation strategy for RAG pattern"""
    prompt_template: str
    citation_style: str  # inline, footnote, endnote, none
    hallucination_prevention: List[str] = Field(default_factory=list)  # consistency_check, source_validation
    max_citations: Optional[int] = None
    include_confidence: bool = True


class RAGPattern(BaseModel):
    """Agentic RAG (Retrieval-Augmented Generation) Pattern"""
    pattern_id: str
    pattern_type: AgentPatternType = AgentPatternType.RAG
    description: Optional[str] = None
    document_sources: List[DocumentSource] = Field(default_factory=list)
    retrieval_strategy: RetrievalStrategy = Field(default_factory=RetrievalStrategy)
    generation_strategy: GenerationStrategy = Field(default_factory=GenerationStrategy)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    
    class Config:
        use_enum_values = True


class RetrievalValidator(BaseModel):
    """Retrieval validator for CRAG pattern"""
    validation_criteria: List[str] = Field(default_factory=list)
    hallucination_detection_methods: List[str] = Field(default_factory=list)  # semantic, factual
    relevance_check_enabled: bool = True
    source_quality_check: bool = True


class SelfReflection(BaseModel):
    """Self-reflection configuration for CRAG pattern"""
    assessment_criteria: List[str] = Field(default_factory=list)
    quality_dimensions: List[str] = Field(default_factory=list)  # factuality, relevance, coherence
    reflection_prompt: Optional[str] = None
    scoring_method: str  # numeric, categorical, binary


class CorrectionMechanism(BaseModel):
    """Correction mechanism for CRAG pattern"""
    correction_triggers: List[str] = Field(default_factory=list)  # low_confidence, conflicting_info
    correction_strategies: List[str] = Field(default_factory=list)  # re_retrieve, regenerate, combine
    max_correction_attempts: int = Field(default=3, ge=1, le=10)
    fallback_strategy: Optional[str] = None


class CRAGPattern(BaseModel):
    """Corrective RAG with Self-Reflection (CRAG) Pattern"""
    pattern_id: str
    pattern_type: AgentPatternType = AgentPatternType.CRAG
    description: Optional[str] = None
    document_sources: List[DocumentSource] = Field(default_factory=list)
    retrieval_strategy: RetrievalStrategy = Field(default_factory=RetrievalStrategy)
    retrieval_validator: RetrievalValidator = Field(default_factory=RetrievalValidator)
    generation_strategy: GenerationStrategy = Field(default_factory=GenerationStrategy)
    self_reflection: SelfReflection = Field(default_factory=SelfReflection)
    correction_mechanism: CorrectionMechanism = Field(default_factory=CorrectionMechanism)
    admission_of_limitation: bool = True
    confidence_threshold: float = Field(default=0.6, ge=0.0, le=1.0)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    
    class Config:
        use_enum_values = True


def get_pattern_by_type(pattern_type: AgentPatternType):
    """Get the appropriate pattern model based on type"""
    if pattern_type == AgentPatternType.REACT:
        return ReActPattern
    elif pattern_type == AgentPatternType.PLAN_EXECUTE:
        return PlanExecutePattern
    elif pattern_type == AgentPatternType.HIERARCHICAL:
        return HierarchicalPattern
    elif pattern_type == AgentPatternType.RAG:
        return RAGPattern
    elif pattern_type == AgentPatternType.CRAG:
        return CRAGPattern
    else:
        raise ValueError(f"Unknown pattern type: {pattern_type}")


def validate_react_pattern(pattern: ReActPattern) -> Dict[str, Any]:
    """Validate ReAct pattern configuration"""
    errors = []
    warnings = []
    
    if not pattern.reasoning_prompt:
        errors.append("Reasoning prompt is required")
    if not pattern.available_actions:
        errors.append("At least one action must be defined")
    if pattern.max_reasoning_steps < 1:
        errors.append("Max reasoning steps must be at least 1")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_plan_execute_pattern(pattern: PlanExecutePattern) -> Dict[str, Any]:
    """Validate Plan-Execute pattern configuration"""
    errors = []
    warnings = []
    
    if not pattern.planning_prompt:
        errors.append("Planning prompt is required")
    if not pattern.execution_steps:
        errors.append("At least one execution step must be defined")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_hierarchical_pattern(pattern: HierarchicalPattern) -> Dict[str, Any]:
    """Validate Hierarchical pattern configuration"""
    errors = []
    warnings = []
    
    if not pattern.supervisor_name:
        errors.append("Supervisor name is required")
    if not pattern.workers:
        errors.append("At least one worker agent must be defined")
    if not pattern.task_routing_rules:
        warnings.append("No task routing rules defined - all tasks may go to first worker")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_rag_pattern(pattern: RAGPattern) -> Dict[str, Any]:
    """Validate RAG pattern configuration"""
    errors = []
    warnings = []
    
    if not pattern.document_sources:
        errors.append("At least one document source must be defined")
    if not pattern.retrieval_strategy.method:
        errors.append("Retrieval method must be specified")
    if not pattern.generation_strategy.prompt_template:
        errors.append("Generation prompt template is required")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }


def validate_crag_pattern(pattern: CRAGPattern) -> Dict[str, Any]:
    """Validate CRAG pattern configuration"""
    errors = []
    warnings = []
    
    if not pattern.document_sources:
        errors.append("At least one document source must be defined")
    if not pattern.retrieval_validator.validation_criteria:
        warnings.append("No retrieval validation criteria defined")
    if not pattern.self_reflection.assessment_criteria:
        warnings.append("No self-reflection assessment criteria defined")
    if not pattern.correction_mechanism.correction_triggers:
        warnings.append("No correction triggers defined")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
