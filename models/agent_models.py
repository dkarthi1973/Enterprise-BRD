"""
Pydantic models for multi-agentic AI BRD components.
Supports LangGraph and CrewAI frameworks.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime


class AgentArchitectureModel(BaseModel):
    """Model for documenting individual agents in a multi-agent system."""
    
    agent_id: str = Field(..., description="Unique agent identifier (e.g., AGENT-001)")
    agent_name: str = Field(..., description="Human-readable agent name")
    agent_role: Literal["Classifier", "Executor", "Reviewer", "Coordinator", "Specialist", "Other"] = Field(
        ..., description="Role of the agent in the system"
    )
    agent_type: Literal["LLM-based", "Rule-based", "Hybrid", "Tool-based"] = Field(
        ..., description="Type of agent implementation"
    )
    primary_responsibility: str = Field(..., description="What the agent does")
    llm_model: Optional[str] = Field(None, description="LLM model used (if LLM-based)")
    system_prompt: Optional[str] = Field(None, description="System prompt/persona for the agent")
    tools_available: List[str] = Field(default_factory=list, description="List of tool IDs available to agent")
    input_requirements: str = Field(..., description="What data the agent needs as input")
    output_format: str = Field(..., description="Format of agent output (JSON, text, etc.)")
    success_criteria: str = Field(..., description="How to measure agent success")
    error_handling_strategy: str = Field(..., description="What to do if agent fails")
    max_retries: int = Field(default=2, description="Maximum retry attempts")
    timeout_seconds: int = Field(default=30, description="Maximum execution time in seconds")
    
    @validator('agent_id')
    def validate_agent_id(cls, v):
        if not v.startswith('AGENT-'):
            raise ValueError('Agent ID must start with AGENT-')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "AGENT-001",
                "agent_name": "Customer Intent Classifier",
                "agent_role": "Classifier",
                "agent_type": "LLM-based",
                "primary_responsibility": "Analyze customer input and classify intent",
                "llm_model": "llama3.2",
                "system_prompt": "You are an expert customer service classifier...",
                "tools_available": [],
                "input_requirements": "customer_message, conversation_history",
                "output_format": "JSON with intent, confidence, reasoning",
                "success_criteria": "Intent classification accuracy > 95%",
                "error_handling_strategy": "If confidence < 0.7, escalate to human",
                "max_retries": 2,
                "timeout_seconds": 5
            }
        }


class TaskSpecificationModel(BaseModel):
    """Model for documenting tasks performed by agents."""
    
    task_id: str = Field(..., description="Unique task identifier (e.g., TASK-001)")
    task_name: str = Field(..., description="Human-readable task name")
    task_description: str = Field(..., description="Detailed task description")
    assigned_agents: List[str] = Field(..., description="List of agent IDs assigned to this task")
    task_goal: str = Field(..., description="What success looks like for this task")
    input_data: str = Field(..., description="Data the task receives")
    output_data: str = Field(..., description="Data the task produces")
    dependencies: List[str] = Field(default_factory=list, description="Task IDs that must complete first")
    execution_strategy: Literal["Sequential", "Parallel", "Conditional"] = Field(
        ..., description="How this task executes"
    )
    retry_policy: str = Field(default="2 retries on failure", description="Retry strategy")
    timeout_seconds: int = Field(default=30, description="Maximum execution time")
    success_metrics: str = Field(..., description="How to measure task success")
    priority: Literal["Critical", "High", "Medium", "Low"] = Field(
        default="Medium", description="Task priority"
    )
    
    @validator('task_id')
    def validate_task_id(cls, v):
        if not v.startswith('TASK-'):
            raise ValueError('Task ID must start with TASK-')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "TASK-001",
                "task_name": "Classify Customer Intent",
                "task_description": "Analyze incoming customer message and determine the intent",
                "assigned_agents": ["AGENT-001"],
                "task_goal": "Accurately classify customer intent with >95% confidence",
                "input_data": "customer_message, conversation_history, customer_profile",
                "output_data": "intent_classification (JSON), confidence_score, reasoning",
                "dependencies": [],
                "execution_strategy": "Sequential",
                "retry_policy": "2 retries on failure",
                "timeout_seconds": 5,
                "success_metrics": "Accuracy > 95%, Response time < 5s",
                "priority": "Critical"
            }
        }


class ToolFunctionModel(BaseModel):
    """Model for documenting tools and functions available to agents."""
    
    tool_id: str = Field(..., description="Unique tool identifier (e.g., TOOL-001)")
    tool_name: str = Field(..., description="Human-readable tool name")
    tool_type: Literal["External API", "Internal Function", "Database Query", "LLM Call", "Webhook"] = Field(
        ..., description="Type of tool"
    )
    tool_description: str = Field(..., description="What the tool does")
    associated_agents: List[str] = Field(..., description="Agent IDs that can use this tool")
    input_parameters: str = Field(..., description="Input parameters (JSON schema or description)")
    output_format: str = Field(..., description="Output format (JSON schema or description)")
    error_handling: str = Field(..., description="How to handle tool failures")
    rate_limits: Optional[str] = Field(None, description="Rate limits if applicable")
    authentication: Optional[str] = Field(None, description="Authentication requirements")
    example_usage: str = Field(..., description="Code example of tool usage")
    dependencies: List[str] = Field(default_factory=list, description="Other tools this tool depends on")
    is_optional: bool = Field(default=False, description="Whether tool is optional for agent")
    
    @validator('tool_id')
    def validate_tool_id(cls, v):
        if not v.startswith('TOOL-'):
            raise ValueError('Tool ID must start with TOOL-')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "tool_id": "TOOL-001",
                "tool_name": "Web Search",
                "tool_type": "External API",
                "tool_description": "Search the web for information",
                "associated_agents": ["AGENT-002"],
                "input_parameters": "query (string, required), max_results (int, optional)",
                "output_format": "JSON with results array",
                "error_handling": "Retry with exponential backoff",
                "rate_limits": "100 requests per minute",
                "authentication": "API key in Authorization header",
                "example_usage": "web_search(query='Python LangGraph', max_results=5)",
                "dependencies": [],
                "is_optional": False
            }
        }


class AgentInteractionModel(BaseModel):
    """Model for documenting how agents interact and communicate."""
    
    interaction_id: str = Field(..., description="Unique interaction identifier (e.g., INTERACTION-001)")
    source_agent: str = Field(..., description="Agent ID initiating communication")
    target_agent: str = Field(..., description="Agent ID receiving communication")
    interaction_type: Literal["Sequential", "Parallel", "Conditional", "Hierarchical", "Broadcast"] = Field(
        ..., description="Type of interaction pattern"
    )
    communication_method: Literal["Direct Call", "Message Queue", "Shared State", "Event-based", "REST API"] = Field(
        ..., description="How agents communicate"
    )
    data_passed: str = Field(..., description="What information flows between agents")
    trigger_condition: str = Field(..., description="When this interaction occurs")
    success_criteria: str = Field(..., description="How to know interaction succeeded")
    failure_handling: str = Field(..., description="What to do if interaction fails")
    latency_requirement_ms: Optional[int] = Field(None, description="Maximum acceptable latency in milliseconds")
    
    @validator('interaction_id')
    def validate_interaction_id(cls, v):
        if not v.startswith('INTERACTION-'):
            raise ValueError('Interaction ID must start with INTERACTION-')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "interaction_id": "INTERACTION-001",
                "source_agent": "AGENT-001",
                "target_agent": "AGENT-002",
                "interaction_type": "Sequential",
                "communication_method": "Direct Call",
                "data_passed": "intent_classification, confidence_score, customer_message",
                "trigger_condition": "TASK-001 completes successfully",
                "success_criteria": "Router receives classification and routes correctly",
                "failure_handling": "Escalate to human agent",
                "latency_requirement_ms": 100
            }
        }


class WorkflowOrchestrationModel(BaseModel):
    """Model for documenting workflow graphs and execution flows."""
    
    workflow_id: str = Field(..., description="Unique workflow identifier (e.g., WORKFLOW-001)")
    workflow_name: str = Field(..., description="Human-readable workflow name")
    workflow_description: str = Field(..., description="High-level overview")
    start_node: str = Field(..., description="Where workflow begins (task or agent ID)")
    end_node: str = Field(..., description="Where workflow completes")
    workflow_graph: str = Field(..., description="Visual or textual representation of workflow")
    decision_points: List[str] = Field(default_factory=list, description="Conditional branches in workflow")
    parallel_paths: List[str] = Field(default_factory=list, description="Parallel execution paths")
    error_recovery_paths: List[str] = Field(default_factory=list, description="Fallback workflows")
    execution_timeout_seconds: int = Field(default=300, description="Maximum time for entire workflow")
    monitoring_requirements: str = Field(..., description="What to track and log")
    framework: Literal["LangGraph", "CrewAI", "Custom", "Hybrid"] = Field(
        default="Custom", description="Framework used for orchestration"
    )
    
    @validator('workflow_id')
    def validate_workflow_id(cls, v):
        if not v.startswith('WORKFLOW-'):
            raise ValueError('Workflow ID must start with WORKFLOW-')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "workflow_id": "WORKFLOW-001",
                "workflow_name": "Customer Support Ticket Processing",
                "workflow_description": "End-to-end workflow for processing support tickets",
                "start_node": "TASK-001",
                "end_node": "TASK-004",
                "workflow_graph": "TASK-001 -> TASK-002 -> TASK-003 -> TASK-004",
                "decision_points": ["confidence > 0.7", "priority == high"],
                "parallel_paths": [],
                "error_recovery_paths": ["escalate_to_human"],
                "execution_timeout_seconds": 30,
                "monitoring_requirements": "Log all decisions, response times, errors",
                "framework": "LangGraph"
            }
        }


class StateManagementModel(BaseModel):
    """Model for documenting shared state and context management."""
    
    state_id: str = Field(..., description="Unique state identifier (e.g., STATE-001)")
    state_name: str = Field(..., description="Human-readable state name")
    state_type: Literal["User Context", "Task State", "Workflow State", "Agent Memory", "Shared Context"] = Field(
        ..., description="Type of state"
    )
    state_schema: str = Field(..., description="JSON schema or structure definition")
    initialization: str = Field(..., description="How state is created")
    update_rules: str = Field(..., description="How state changes")
    persistence: Literal["In-Memory", "Database", "Cache", "Message Queue", "Distributed"] = Field(
        ..., description="How state is stored"
    )
    sharing_rules: str = Field(..., description="Which agents can access/modify")
    lifecycle: str = Field(..., description="When state is created/destroyed")
    retention_days: Optional[int] = Field(None, description="How long to retain state")
    
    @validator('state_id')
    def validate_state_id(cls, v):
        if not v.startswith('STATE-'):
            raise ValueError('State ID must start with STATE-')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "state_id": "STATE-001",
                "state_name": "Conversation Context",
                "state_type": "User Context",
                "state_schema": "JSON schema with user_id, messages, current_intent, etc.",
                "initialization": "Created when conversation starts",
                "update_rules": "Append messages, update intent after classification",
                "persistence": "Database",
                "sharing_rules": "All agents can read, only Classifier can update intent",
                "lifecycle": "Created at start, archived after 30 days",
                "retention_days": 30
            }
        }


class ErrorHandlingModel(BaseModel):
    """Model for documenting error scenarios and recovery strategies."""
    
    error_id: str = Field(..., description="Unique error identifier (e.g., ERROR-001)")
    error_scenario: str = Field(..., description="What can go wrong")
    affected_component: str = Field(..., description="Agent, task, tool, or workflow ID")
    error_type: Literal["Timeout", "API Failure", "Validation Error", "Resource Exhausted", "Authentication", "Other"] = Field(
        ..., description="Type of error"
    )
    detection_method: str = Field(..., description="How to detect this error")
    recovery_strategy: str = Field(..., description="How to recover")
    fallback_option: str = Field(..., description="What to do if recovery fails")
    logging_alerting: str = Field(..., description="What to log and alert on")
    prevention: str = Field(..., description="How to prevent this error")
    severity: Literal["Critical", "High", "Medium", "Low"] = Field(
        default="Medium", description="Error severity"
    )
    
    @validator('error_id')
    def validate_error_id(cls, v):
        if not v.startswith('ERROR-'):
            raise ValueError('Error ID must start with ERROR-')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "error_id": "ERROR-001",
                "error_scenario": "LLM API timeout during intent classification",
                "affected_component": "AGENT-001",
                "error_type": "Timeout",
                "detection_method": "Task execution exceeds 5-second timeout",
                "recovery_strategy": "Retry with exponential backoff",
                "fallback_option": "Use rule-based classifier or escalate",
                "logging_alerting": "Log error, alert if 3+ failures in 1 minute",
                "prevention": "Implement timeout, use faster model, cache results",
                "severity": "High"
            }
        }


class AgentLLMConfigurationModel(BaseModel):
    """Model for LLM-specific configurations for agents."""
    
    agent_id: str = Field(..., description="Reference to Agent Architecture")
    model_name: str = Field(..., description="LLM model name")
    system_prompt: str = Field(..., description="System prompt for agent persona")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Creativity level")
    max_tokens: int = Field(default=1000, description="Response length limit")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Diversity parameter")
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="Repetition control")
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="Topic diversity")
    stop_sequences: List[str] = Field(default_factory=list, description="When to stop generating")
    few_shot_examples: str = Field(default="", description="In-context learning examples")
    constraints: str = Field(default="", description="What the agent should NOT do")
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "AGENT-001",
                "model_name": "llama3.2",
                "system_prompt": "You are an expert customer service classifier...",
                "temperature": 0.2,
                "max_tokens": 200,
                "top_p": 0.9,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
                "stop_sequences": ["---", "END"],
                "few_shot_examples": "Q: I can't log in\nA: technical_support",
                "constraints": "Do NOT make up categories"
            }
        }


class MultiAgentBRDModel(BaseModel):
    """Complete BRD model for multi-agentic AI applications."""
    
    # Original sections
    project_id: Optional[str] = Field(None, description="Project identifier")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    # Multi-agent specific sections
    agents: List[AgentArchitectureModel] = Field(default_factory=list, description="All agents in system")
    tasks: List[TaskSpecificationModel] = Field(default_factory=list, description="All tasks")
    tools: List[ToolFunctionModel] = Field(default_factory=list, description="All tools/functions")
    interactions: List[AgentInteractionModel] = Field(default_factory=list, description="Agent interactions")
    workflows: List[WorkflowOrchestrationModel] = Field(default_factory=list, description="Workflows")
    states: List[StateManagementModel] = Field(default_factory=list, description="State definitions")
    error_handlers: List[ErrorHandlingModel] = Field(default_factory=list, description="Error handling")
    llm_configs: List[AgentLLMConfigurationModel] = Field(default_factory=list, description="LLM configurations")
    
    # Framework specification
    framework_type: Literal["LangGraph", "CrewAI", "Hybrid", "Custom"] = Field(
        default="Custom", description="Agent framework used"
    )
    framework_version: Optional[str] = Field(None, description="Framework version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "PROJ-001",
                "framework_type": "LangGraph",
                "agents": [],
                "tasks": [],
                "tools": [],
                "interactions": [],
                "workflows": [],
                "states": [],
                "error_handlers": [],
                "llm_configs": []
            }
        }
