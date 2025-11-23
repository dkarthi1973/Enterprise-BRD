"""
Enhanced Pydantic models for BRD that supports both traditional and multi-agentic AI applications.
Combines original BRD sections with new agent-based sections.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Literal
from datetime import datetime
from .agent_models import (
    AgentArchitectureModel, TaskSpecificationModel, ToolFunctionModel,
    AgentInteractionModel, WorkflowOrchestrationModel, StateManagementModel,
    ErrorHandlingModel, AgentLLMConfigurationModel, MultiAgentBRDModel
)


class OverviewModel(BaseModel):
    """Project overview and metadata."""
    project_name: str = Field(..., min_length=1, max_length=255)
    project_description: str = Field(..., min_length=10, max_length=2000)
    business_goal: str = Field(..., min_length=10, max_length=2000)
    document_version: str = Field(default="1.0")
    prepared_by: Optional[str] = Field(None)
    approved_by: Optional[str] = Field(None)
    target_release_date: Optional[str] = Field(None)


class UISpecificationModel(BaseModel):
    """UI specification with master/detail support."""
    requirement_id: str = Field(...)
    feature_module: str = Field(...)
    screen_component: str = Field(...)
    requirement_description: str = Field(...)
    validation_rule: Optional[str] = Field(None)
    business_rule: Optional[str] = Field(None)
    master_detail: Literal["Master", "Detail", "N/A"] = Field(default="N/A")
    priority: Literal["Must", "Should", "Could", "Won't"] = Field(default="Should")


class APISpecificationModel(BaseModel):
    """API specification with agent endpoint support."""
    api_id: str = Field(...)
    api_name: str = Field(...)
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"] = Field(...)
    endpoint: str = Field(...)
    request_payload: str = Field(...)
    response_payload: str = Field(...)
    business_rule: Optional[str] = Field(None)
    api_type: Literal["Internal", "External (LLM)", "Third-Party", "Agent Endpoint"] = Field(default="Internal")
    agent_id: Optional[str] = Field(None, description="If agent endpoint, which agent handles it")


class LLMPromptModel(BaseModel):
    """LLM prompt configuration."""
    prompt_id: str = Field(...)
    use_case: str = Field(...)
    prompt_template: str = Field(...)
    input_variables: str = Field(...)
    expected_output: str = Field(...)
    model_name: str = Field(...)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class DatabaseSchemaModel(BaseModel):
    """Database schema definition."""
    table_name: str = Field(...)
    field_name: str = Field(...)
    data_type: str = Field(...)
    constraints: Optional[str] = Field(None)
    relationship: Literal["Primary", "Foreign", "N/A"] = Field(default="N/A")
    description: Optional[str] = Field(None)


class TechStackModel(BaseModel):
    """Technology stack selection."""
    category: str = Field(...)
    technology_tool: str = Field(...)
    version: Optional[str] = Field(None)
    rationale: Optional[str] = Field(None)
    repository_url: Optional[str] = Field(None)


class TraceabilityModel(BaseModel):
    """Traceability matrix for requirement linking."""
    business_requirement_id: str = Field(...)
    business_requirement: str = Field(...)
    linked_ui_id: Optional[str] = Field(None)
    linked_api_id: Optional[str] = Field(None)
    linked_llm_id: Optional[str] = Field(None)
    linked_agent_id: Optional[str] = Field(None, description="For multi-agent systems")
    linked_task_id: Optional[str] = Field(None, description="For multi-agent systems")
    status: Literal["Proposed", "Approved", "Implemented"] = Field(default="Proposed")


class EnhancedBRDProjectModel(BaseModel):
    """
    Enhanced BRD project model supporting both traditional and multi-agentic AI applications.
    
    This model combines:
    1. Original sections: Overview, UI Specs, API Specs, LLM Prompts, Database, Tech Stack, Traceability
    2. New multi-agent sections: Agents, Tasks, Tools, Interactions, Workflows, State Management, Error Handling
    """
    
    # Metadata
    project_id: Optional[str] = Field(None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    
    # Application type
    application_type: Literal["Traditional LLM", "Single Agent", "Multi-Agent", "Hybrid"] = Field(
        default="Traditional LLM",
        description="Type of AI application"
    )
    
    # Original BRD sections
    overview: OverviewModel = Field(...)
    ui_specifications: List[UISpecificationModel] = Field(default_factory=list)
    api_specifications: List[APISpecificationModel] = Field(default_factory=list)
    llm_prompts: List[LLMPromptModel] = Field(default_factory=list)
    database_schema: List[DatabaseSchemaModel] = Field(default_factory=list)
    tech_stack: List[TechStackModel] = Field(default_factory=list)
    traceability_matrix: List[TraceabilityModel] = Field(default_factory=list)
    
    # New multi-agent sections
    agents: List[AgentArchitectureModel] = Field(
        default_factory=list,
        description="Agent definitions (for multi-agent systems)"
    )
    tasks: List[TaskSpecificationModel] = Field(
        default_factory=list,
        description="Task specifications (for multi-agent systems)"
    )
    tools: List[ToolFunctionModel] = Field(
        default_factory=list,
        description="Tool/function definitions (for multi-agent systems)"
    )
    agent_interactions: List[AgentInteractionModel] = Field(
        default_factory=list,
        description="Agent interaction patterns (for multi-agent systems)"
    )
    workflows: List[WorkflowOrchestrationModel] = Field(
        default_factory=list,
        description="Workflow orchestrations (for multi-agent systems)"
    )
    states: List[StateManagementModel] = Field(
        default_factory=list,
        description="State management definitions (for multi-agent systems)"
    )
    error_handlers: List[ErrorHandlingModel] = Field(
        default_factory=list,
        description="Error handling strategies (for all systems)"
    )
    agent_llm_configs: List[AgentLLMConfigurationModel] = Field(
        default_factory=list,
        description="Agent-specific LLM configurations (for multi-agent systems)"
    )
    
    # Framework specification
    framework_type: Literal["None", "LangGraph", "CrewAI", "Hybrid", "Custom"] = Field(
        default="None",
        description="Agent framework used (if multi-agent)"
    )
    framework_version: Optional[str] = Field(None)
    
    # Documentation and notes
    architecture_notes: Optional[str] = Field(None, description="General architecture notes")
    implementation_notes: Optional[str] = Field(None, description="Implementation-specific notes")
    
    def is_multi_agent(self) -> bool:
        """Check if this is a multi-agent application."""
        return self.application_type in ["Multi-Agent", "Hybrid"] or len(self.agents) > 0
    
    def get_agent_by_id(self, agent_id: str) -> Optional[AgentArchitectureModel]:
        """Get agent by ID."""
        return next((a for a in self.agents if a.agent_id == agent_id), None)
    
    def get_task_by_id(self, task_id: str) -> Optional[TaskSpecificationModel]:
        """Get task by ID."""
        return next((t for t in self.tasks if t.task_id == task_id), None)
    
    def get_tool_by_id(self, tool_id: str) -> Optional[ToolFunctionModel]:
        """Get tool by ID."""
        return next((t for t in self.tools if t.tool_id == tool_id), None)
    
    def get_workflow_by_id(self, workflow_id: str) -> Optional[WorkflowOrchestrationModel]:
        """Get workflow by ID."""
        return next((w for w in self.workflows if w.workflow_id == workflow_id), None)
    
    def validate_agent_references(self) -> List[str]:
        """Validate that all agent references are valid."""
        errors = []
        agent_ids = {a.agent_id for a in self.agents}
        
        # Check task assignments
        for task in self.tasks:
            for agent_id in task.assigned_agents:
                if agent_id not in agent_ids:
                    errors.append(f"Task {task.task_id} references unknown agent {agent_id}")
        
        # Check tool associations
        for tool in self.tools:
            for agent_id in tool.associated_agents:
                if agent_id not in agent_ids:
                    errors.append(f"Tool {tool.tool_id} references unknown agent {agent_id}")
        
        # Check interactions
        for interaction in self.agent_interactions:
            if interaction.source_agent not in agent_ids:
                errors.append(f"Interaction {interaction.interaction_id} references unknown source agent {interaction.source_agent}")
            if interaction.target_agent not in agent_ids:
                errors.append(f"Interaction {interaction.interaction_id} references unknown target agent {interaction.target_agent}")
        
        # Check LLM configs
        for config in self.agent_llm_configs:
            if config.agent_id not in agent_ids:
                errors.append(f"LLM config references unknown agent {config.agent_id}")
        
        return errors
    
    def validate_task_dependencies(self) -> List[str]:
        """Validate that task dependencies are valid."""
        errors = []
        task_ids = {t.task_id for t in self.tasks}
        
        for task in self.tasks:
            for dep_id in task.dependencies:
                if dep_id not in task_ids:
                    errors.append(f"Task {task.task_id} references unknown dependency {dep_id}")
        
        return errors
    
    def validate_tool_dependencies(self) -> List[str]:
        """Validate that tool dependencies are valid."""
        errors = []
        tool_ids = {t.tool_id for t in self.tools}
        
        for tool in self.tools:
            for dep_id in tool.dependencies:
                if dep_id not in tool_ids:
                    errors.append(f"Tool {tool.tool_id} references unknown dependency {dep_id}")
        
        return errors
    
    def validate_all(self) -> List[str]:
        """Run all validations."""
        errors = []
        errors.extend(self.validate_agent_references())
        errors.extend(self.validate_task_dependencies())
        errors.extend(self.validate_tool_dependencies())
        return errors
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "PROJ-001",
                "application_type": "Multi-Agent",
                "framework_type": "LangGraph",
                "overview": {
                    "project_name": "Customer Support Multi-Agent System",
                    "project_description": "AI-powered customer support using multiple specialized agents",
                    "business_goal": "Reduce support ticket resolution time by 50%"
                },
                "agents": [],
                "tasks": [],
                "tools": [],
                "agent_interactions": [],
                "workflows": [],
                "states": [],
                "error_handlers": []
            }
        }
