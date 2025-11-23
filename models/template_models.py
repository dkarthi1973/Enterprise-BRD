"""
Template Models for Customized BRD Templates
Supports Normal, Agentic, and Multi-Agentic templates
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


class TemplateType(str, Enum):
    """Supported template types"""
    NORMAL = "normal"
    AGENTIC = "agentic"
    MULTI_AGENTIC = "multi_agentic"


class ProjectStatus(str, Enum):
    """Project status enumeration"""
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    APPROVED = "approved"
    ARCHIVED = "archived"


class ProjectMetadata(BaseModel):
    """Project metadata for all template types"""
    project_id: str = Field(..., description="Unique project identifier")
    project_name: str = Field(..., description="Human-readable project name")
    project_description: str = Field(..., description="Detailed project description")
    template_type: TemplateType = Field(..., description="Type of BRD template")
    version: str = Field(default="1.0", description="Project version")
    created_by: str = Field(..., description="Creator username")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_modified_by: Optional[str] = Field(None, description="Last modifier username")
    last_modified_at: Optional[datetime] = Field(None, description="Last modification time")
    status: ProjectStatus = Field(default=ProjectStatus.DRAFT)
    tags: List[str] = Field(default_factory=list, description="Project tags")
    
    @validator('project_id')
    def validate_project_id(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Project ID must be at least 3 characters')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Project ID can only contain alphanumeric characters, hyphens, and underscores')
        return v
    
    @validator('project_name')
    def validate_project_name(cls, v):
        if not v or len(v) < 3:
            raise ValueError('Project name must be at least 3 characters')
        return v


class UIComponent(BaseModel):
    """UI component specification"""
    component_id: str
    component_name: str
    component_type: str  # Text, Button, Dropdown, TextArea, etc.
    label: Optional[str] = None
    required: bool = False
    validation_rules: List[str] = Field(default_factory=list)
    properties: Dict[str, Any] = Field(default_factory=dict)


class UIScreen(BaseModel):
    """UI screen specification"""
    screen_id: str
    screen_name: str
    description: Optional[str] = None
    screen_type: str  # Form, Detail, List, Dashboard, etc.
    layout_type: str  # SingleColumn, TwoColumn, Grid, etc.
    components: List[UIComponent] = Field(default_factory=list)
    validations: List[Dict[str, str]] = Field(default_factory=list)
    business_rules: List[Dict[str, str]] = Field(default_factory=list)


class APIEndpoint(BaseModel):
    """API endpoint specification"""
    endpoint_id: str
    endpoint_path: str
    http_method: str  # GET, POST, PUT, DELETE, PATCH
    description: Optional[str] = None
    request_schema: Dict[str, Any] = Field(default_factory=dict)
    response_schema: Dict[str, Any] = Field(default_factory=dict)
    error_codes: Dict[int, str] = Field(default_factory=dict)
    authentication_required: bool = False
    rate_limit: Optional[int] = None
    timeout_seconds: Optional[int] = None


class LLMPrompt(BaseModel):
    """LLM prompt specification"""
    prompt_id: str
    prompt_name: str
    prompt_type: str  # System, User, Assistant
    prompt_text: str
    variables: List[str] = Field(default_factory=list)
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    examples: List[Dict[str, str]] = Field(default_factory=list)


class DatabaseColumn(BaseModel):
    """Database column specification"""
    column_name: str
    column_type: str  # Integer, String, Text, Float, DateTime, Boolean, JSON
    required: bool = False
    primary_key: bool = False
    foreign_key: Optional[str] = None
    unique: bool = False
    default_value: Optional[Any] = None
    enum_values: Optional[List[str]] = None
    description: Optional[str] = None


class DatabaseTable(BaseModel):
    """Database table specification"""
    table_id: str
    table_name: str
    description: Optional[str] = None
    columns: List[DatabaseColumn] = Field(default_factory=list)
    indexes: List[Dict[str, Any]] = Field(default_factory=list)
    relationships: List[Dict[str, str]] = Field(default_factory=list)


class TechStackComponent(BaseModel):
    """Technology stack component"""
    component_id: str
    component_name: str
    component_type: str  # Language, Framework, Database, Service, Library
    version: Optional[str] = None
    purpose: str
    rationale: Optional[str] = None
    alternatives: List[str] = Field(default_factory=list)


class NormalBRDTemplate(BaseModel):
    """Normal BRD Template for traditional applications"""
    metadata: ProjectMetadata
    overview: Dict[str, Any] = Field(default_factory=dict)
    ui_specifications: List[UIScreen] = Field(default_factory=list)
    api_specifications: List[APIEndpoint] = Field(default_factory=list)
    llm_prompts: List[LLMPrompt] = Field(default_factory=list)
    database_schema: List[DatabaseTable] = Field(default_factory=list)
    tech_stack: List[TechStackComponent] = Field(default_factory=list)
    deployment_strategy: Optional[Dict[str, Any]] = None
    operations_plan: Optional[Dict[str, Any]] = None
    traceability_matrix: Optional[List[Dict[str, str]]] = None
    
    class Config:
        use_enum_values = True


class AgentGoal(BaseModel):
    """Agent goal specification"""
    goal_id: str
    goal: str
    priority: str  # High, Medium, Low
    success_criteria: str
    measurable: bool = True


class AgentConstraint(BaseModel):
    """Agent constraint specification"""
    constraint_id: str
    constraint_type: str  # Resource, Behavioral, Time, Security
    description: str
    impact: Optional[str] = None


class AgentCapability(BaseModel):
    """Agent capability specification"""
    capability_id: str
    capability_name: str
    description: str
    capability_type: str  # Tool, Reasoning, Formatting, Integration
    status: str  # Required, Optional, Future
    dependencies: List[str] = Field(default_factory=list)


class AgentDefinition(BaseModel):
    """Agent specification for agentic templates"""
    agent_id: str
    agent_name: str
    agent_role: str
    agent_description: Optional[str] = None
    decision_framework: str  # ReAct, Plan-Execute, Hierarchical, RAG, CRAG
    goals: List[AgentGoal] = Field(default_factory=list)
    constraints: List[AgentConstraint] = Field(default_factory=list)
    capabilities: List[AgentCapability] = Field(default_factory=list)
    max_iterations: Optional[int] = None
    timeout_seconds: Optional[int] = None


class ToolDefinition(BaseModel):
    """Tool/Function definition for agents"""
    tool_id: str
    tool_name: str
    tool_type: str  # API Call, Database Query, Utility Function, External Service
    description: str
    function_signature: Optional[str] = None
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    error_handling: List[Dict[str, str]] = Field(default_factory=list)
    rate_limit: Optional[int] = None
    timeout_seconds: Optional[int] = None


class WorkflowStep(BaseModel):
    """Workflow step specification"""
    step_id: str
    step_name: str
    step_type: str  # Input, Processing, Tool Call, LLM Call, Output, Decision
    description: Optional[str] = None
    input_spec: Optional[Dict[str, Any]] = None
    output_spec: Optional[Dict[str, Any]] = None
    dependencies: List[str] = Field(default_factory=list)
    success_criteria: Optional[str] = None
    retry_enabled: bool = False
    max_retries: int = 0
    timeout_seconds: Optional[int] = None


class WorkflowDecision(BaseModel):
    """Workflow decision point"""
    decision_id: str
    decision_point: str
    true_path: str  # Next step if true
    false_path: str  # Next step if false
    condition: Optional[str] = None


class StateVariable(BaseModel):
    """State variable specification"""
    variable_id: str
    variable_name: str
    variable_type: str  # string, integer, float, object, array, boolean
    initial_value: Optional[Any] = None
    scope: str  # session, request, global
    description: Optional[str] = None
    persistence: str  # temporary, session, permanent


class StateTransition(BaseModel):
    """State transition specification"""
    from_state: str
    to_state: str
    trigger: str
    actions: List[str] = Field(default_factory=list)


class AgenticBRDTemplate(BaseModel):
    """Agentic BRD Template for single-agent systems"""
    metadata: ProjectMetadata
    overview: Dict[str, Any] = Field(default_factory=dict)
    agent_definition: Optional[AgentDefinition] = None
    tool_definitions: List[ToolDefinition] = Field(default_factory=list)
    workflow_definition: List[WorkflowStep] = Field(default_factory=list)
    workflow_decisions: List[WorkflowDecision] = Field(default_factory=list)
    state_management: List[StateVariable] = Field(default_factory=list)
    state_transitions: List[StateTransition] = Field(default_factory=list)
    ui_specifications: List[UIScreen] = Field(default_factory=list)
    api_specifications: List[APIEndpoint] = Field(default_factory=list)
    llm_prompts: List[LLMPrompt] = Field(default_factory=list)
    database_schema: List[DatabaseTable] = Field(default_factory=list)
    tech_stack: List[TechStackComponent] = Field(default_factory=list)
    error_handling: Optional[Dict[str, Any]] = None
    deployment_strategy: Optional[Dict[str, Any]] = None
    operations_plan: Optional[Dict[str, Any]] = None
    traceability_matrix: Optional[List[Dict[str, str]]] = None
    
    class Config:
        use_enum_values = True


class MultiAgentDefinition(BaseModel):
    """Multiple agent definition for multi-agentic systems"""
    agents: List[AgentDefinition] = Field(default_factory=list)
    supervisor_agent: Optional[AgentDefinition] = None
    agent_roles: Dict[str, str] = Field(default_factory=dict)  # agent_id -> role


class AgentInteraction(BaseModel):
    """Agent interaction specification"""
    interaction_id: str
    source_agent: str
    target_agent: str
    interaction_type: str  # Message, Request, Response, Delegation
    protocol: Optional[str] = None
    message_schema: Optional[Dict[str, Any]] = None


class TaskDefinition(BaseModel):
    """Task definition for multi-agentic systems"""
    task_id: str
    task_name: str
    description: Optional[str] = None
    assigned_agent: str
    dependencies: List[str] = Field(default_factory=list)
    success_criteria: str
    timeout_seconds: Optional[int] = None
    priority: str  # High, Medium, Low


class MultiAgenticBRDTemplate(BaseModel):
    """Multi-Agentic BRD Template for multi-agent orchestration"""
    metadata: ProjectMetadata
    overview: Dict[str, Any] = Field(default_factory=dict)
    agent_architecture: Optional[MultiAgentDefinition] = None
    task_management: List[TaskDefinition] = Field(default_factory=list)
    tool_definitions: List[ToolDefinition] = Field(default_factory=list)
    agent_interactions: List[AgentInteraction] = Field(default_factory=list)
    workflow_orchestration: List[WorkflowStep] = Field(default_factory=list)
    workflow_decisions: List[WorkflowDecision] = Field(default_factory=list)
    state_management: List[StateVariable] = Field(default_factory=list)
    state_transitions: List[StateTransition] = Field(default_factory=list)
    ui_specifications: List[UIScreen] = Field(default_factory=list)
    api_specifications: List[APIEndpoint] = Field(default_factory=list)
    llm_prompts: List[LLMPrompt] = Field(default_factory=list)
    database_schema: List[DatabaseTable] = Field(default_factory=list)
    tech_stack: List[TechStackComponent] = Field(default_factory=list)
    error_handling: Optional[Dict[str, Any]] = None
    resilience_strategy: Optional[Dict[str, Any]] = None
    deployment_strategy: Optional[Dict[str, Any]] = None
    operations_plan: Optional[Dict[str, Any]] = None
    traceability_matrix: Optional[List[Dict[str, str]]] = None
    
    class Config:
        use_enum_values = True


def get_template_by_type(template_type: TemplateType):
    """Get the appropriate template model based on type"""
    if template_type == TemplateType.NORMAL:
        return NormalBRDTemplate
    elif template_type == TemplateType.AGENTIC:
        return AgenticBRDTemplate
    elif template_type == TemplateType.MULTI_AGENTIC:
        return MultiAgenticBRDTemplate
    else:
        raise ValueError(f"Unknown template type: {template_type}")
