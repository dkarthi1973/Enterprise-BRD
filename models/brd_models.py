"""
Pydantic models for the Business Requirement Document (BRD) structure.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime


class OverviewModel(BaseModel):
    """Overview and Document Control information."""
    project_name: str = Field(..., min_length=1, max_length=255, description="Name of the project")
    project_description: str = Field(..., min_length=10, max_length=2000, description="Brief description of the project")
    business_goal: str = Field(..., min_length=10, max_length=2000, description="Primary business objective")
    document_version: str = Field(default="1.0", description="Current version of the BRD")
    prepared_by: str = Field(default="", max_length=255, description="Name of the author")
    approved_by: str = Field(default="", max_length=255, description="Name of the approver")
    target_release_date: Optional[str] = Field(default=None, description="Planned release date (YYYY-MM-DD)")

    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "GenAI Customer Feedback Management Platform",
                "project_description": "A platform to ingest and analyze customer feedback using Generative AI.",
                "business_goal": "Automate feedback categorization with 90% accuracy.",
                "document_version": "1.0",
                "prepared_by": "Manus AI",
                "approved_by": "Stakeholder Name",
                "target_release_date": "2025-12-31"
            }
        }


class UISpecificationModel(BaseModel):
    """UI Specification requirement."""
    requirement_id: str = Field(default="", max_length=50, description="...")
    feature_module: str = Field(default="", max_length=255, description="...")
    screen_component: str = Field(..., min_length=1, max_length=255, description="Screen or component name")
    requirement_description: str = Field(..., min_length=10, max_length=2000, description="Detailed description")
    validation_rule: str = Field(default="", max_length=1000, description="Front-end validation rule")
    business_rule: str = Field(default="", max_length=1000, description="Business logic rule")
    master_detail: str = Field(default="N/A", description="Master, Detail, or N/A")
    priority: str = Field(default="Should", description="MoSCoW priority: Must, Should, Could, Won't")

    class Config:
        json_schema_extra = {
            "example": {
                "requirement_id": "UI-001",
                "feature_module": "Feedback Ingestion",
                "screen_component": "Feedback Submission Form",
                "requirement_description": "Allow users to submit feedback via text area.",
                "validation_rule": "Feedback text must be between 50 and 5000 characters.",
                "business_rule": "All feedback must be queued for AI processing.",
                "master_detail": "N/A",
                "priority": "Must"
            }
        }


class APISpecificationModel(BaseModel):
    """API Specification."""
    api_id: str = Field(..., min_length=1, max_length=50, description="Unique identifier (e.g., API-001)")
    api_name: str = Field(..., min_length=1, max_length=255, description="Descriptive name")
    method: str = Field(..., description="HTTP method: GET, POST, PUT, DELETE")
    endpoint: str = Field(..., min_length=1, max_length=255, description="API path")
    request_payload: str = Field(default="", max_length=2000, description="Request payload structure")
    response_payload: str = Field(default="", max_length=2000, description="Response payload structure")
    business_rule: str = Field(default="", max_length=1000, description="Business logic")
    api_type: str = Field(default="Internal", description="Internal, External (LLM), or Third-Party")

    class Config:
        json_schema_extra = {
            "example": {
                "api_id": "API-001",
                "api_name": "Submit New Feedback",
                "method": "POST",
                "endpoint": "/api/v1/feedback",
                "request_payload": '{ "text": "string", "category": "string" }',
                "response_payload": '{ "feedback_id": "integer", "status": "success" }',
                "business_rule": "Validate user_id against User table.",
                "api_type": "Internal"
            }
        }


class LLMPromptModel(BaseModel):
    """LLM Prompt configuration."""
    prompt_id: str = Field(..., min_length=1, max_length=50, description="Unique identifier (e.g., LLM-001)")
    use_case: str = Field(..., min_length=1, max_length=255, description="Specific function of the prompt")
    prompt_template: str = Field(..., min_length=10, max_length=5000, description="Base prompt template")
    input_variables: str = Field(default="", max_length=1000, description="Variables to substitute")
    expected_output: str = Field(default="", max_length=1000, description="Desired output format")
    model_name: str = Field(default="llama3.2", description="LLM model to use")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature parameter")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt_id": "LLM-001",
                "use_case": "Customer Sentiment Analysis",
                "prompt_template": "Analyze sentiment of: [FEEDBACK_TEXT]",
                "input_variables": "[FEEDBACK_TEXT]",
                "expected_output": '{ "sentiment": "string" }',
                "model_name": "llama3.2",
                "temperature": 0.2
            }
        }


class DatabaseSchemaModel(BaseModel):
    """Database schema definition."""
    table_name: str = Field(..., min_length=1, max_length=255, description="Table name")
    field_name: str = Field(..., min_length=1, max_length=255, description="Column/field name")
    data_type: str = Field(..., min_length=1, max_length=100, description="SQL data type")
    constraints: str = Field(default="", max_length=500, description="Constraints (NOT NULL, UNIQUE, etc.)")
    relationship: str = Field(default="N/A", description="Relationship type")
    description: str = Field(default="", max_length=1000, description="Field purpose")

    class Config:
        json_schema_extra = {
            "example": {
                "table_name": "Feedback",
                "field_name": "feedback_id",
                "data_type": "INT",
                "constraints": "Primary Key, NOT NULL",
                "relationship": "Primary",
                "description": "Unique identifier for feedback."
            }
        }


class TechStackModel(BaseModel):
    """Technology Stack and Version Control."""
    category: str = Field(..., min_length=1, max_length=255, description="Technology category")
    technology_tool: str = Field(..., min_length=1, max_length=255, description="Technology or tool name")
    version: str = Field(default="", max_length=100, description="Required version")
    rationale: str = Field(default="", max_length=1000, description="Justification for selection")
    repository_url: str = Field(default="", max_length=500, description="Repository URL")

    class Config:
        json_schema_extra = {
            "example": {
                "category": "Backend Framework",
                "technology_tool": "FastAPI",
                "version": "0.115.6",
                "rationale": "High-performance Python web framework.",
                "repository_url": "https://github.com/example/repo"
            }
        }


class TraceabilityModel(BaseModel):
    """Traceability Matrix linking requirements to implementations."""
    business_requirement_id: str = Field(..., min_length=1, max_length=50, description="Business requirement ID")
    business_requirement: str = Field(..., min_length=10, max_length=2000, description="Business requirement description")
    linked_ui_id: str = Field(default="", max_length=500, description="Linked UI requirement IDs")
    linked_api_id: str = Field(default="", max_length=500, description="Linked API IDs")
    linked_llm_id: str = Field(default="", max_length=500, description="Linked LLM prompt IDs")
    status: str = Field(default="Proposed", description="Status: Proposed, Approved, Implemented")


class AgentArchitectureModel(BaseModel):
    """Agent Architecture specification."""
    agent_id: str = Field(..., min_length=1, max_length=50, description="Unique agent identifier")
    agent_name: str = Field(..., min_length=1, max_length=255, description="Agent name")
    agent_type: str = Field(..., description="Type: Autonomous, Reactive, Proactive, Hybrid")
    primary_role: str = Field(..., min_length=1, max_length=255, description="Primary role/responsibility")
    capabilities: str = Field(default="", max_length=2000, description="Agent capabilities")
    dependencies: str = Field(default="", max_length=500, description="Dependent agents or services")
    communication_protocol: str = Field(default="REST", description="Communication protocol")
    description: str = Field(default="", max_length=1000, description="Detailed description")

    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "AGENT-001",
                "agent_name": "Feedback Analyzer",
                "agent_type": "Autonomous",
                "primary_role": "Analyze customer feedback sentiment",
                "capabilities": "NLP processing, sentiment analysis, categorization",
                "dependencies": "Database service, LLM service",
                "communication_protocol": "REST",
                "description": "Autonomous agent for real-time feedback analysis"
            }
        }


class AgentConfigurationModel(BaseModel):
    """Agent Configuration and Parameters."""
    config_id: str = Field(..., min_length=1, max_length=50, description="Configuration ID")
    agent_id: str = Field(..., min_length=1, max_length=50, description="Reference to agent")
    parameter_name: str = Field(..., min_length=1, max_length=255, description="Parameter name")
    parameter_value: str = Field(..., min_length=1, max_length=1000, description="Parameter value")
    parameter_type: str = Field(default="string", description="Type: string, integer, float, boolean, json")
    description: str = Field(default="", max_length=500, description="Parameter description")
    required: bool = Field(default=True, description="Is parameter required?")

    class Config:
        json_schema_extra = {
            "example": {
                "config_id": "CONFIG-001",
                "agent_id": "AGENT-001",
                "parameter_name": "sentiment_threshold",
                "parameter_value": "0.7",
                "parameter_type": "float",
                "description": "Minimum confidence threshold for sentiment classification",
                "required": True
            }
        }


class AgentTaskModel(BaseModel):
    """Agent Task and Workflow Definition."""
    task_id: str = Field(..., min_length=1, max_length=50, description="Unique task ID")
    agent_id: str = Field(..., min_length=1, max_length=50, description="Reference to agent")
    task_name: str = Field(..., min_length=1, max_length=255, description="Task name")
    task_type: str = Field(..., description="Type: Data Processing, Decision Making, Communication, Coordination")
    input_data: str = Field(default="", max_length=1000, description="Input data specification")
    output_data: str = Field(default="", max_length=1000, description="Output data specification")
    success_criteria: str = Field(default="", max_length=1000, description="Success criteria")
    error_handling: str = Field(default="", max_length=500, description="Error handling strategy")
    description: str = Field(default="", max_length=1000, description="Detailed task description")

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "TASK-001",
                "agent_id": "AGENT-001",
                "task_name": "Analyze Feedback",
                "task_type": "Data Processing",
                "input_data": "Raw feedback text",
                "output_data": "Sentiment score and category",
                "success_criteria": "Accuracy > 90%",
                "error_handling": "Retry with different model",
                "description": "Process and analyze customer feedback"
            }
        }


class BRDProjectModel(BaseModel):
    """Complete BRD Project model."""
    project_id: Optional[str] = Field(default=None, description="Unique project ID")
    template_type: str = Field(default="Normal", description="Template type: Normal, Agentic, Multi-Agentic")
    overview: OverviewModel
    ui_specifications: List[UISpecificationModel] = Field(default_factory=list)
    api_specifications: List[APISpecificationModel] = Field(default_factory=list)
    llm_prompts: List[LLMPromptModel] = Field(default_factory=list)
    database_schema: List[DatabaseSchemaModel] = Field(default_factory=list)
    tech_stack: List[TechStackModel] = Field(default_factory=list)
    traceability_matrix: List[TraceabilityModel] = Field(default_factory=list)
    agent_architectures: List[AgentArchitectureModel] = Field(default_factory=list, description="Agent architectures (Agentic/Multi-Agentic only)")
    agent_configurations: List[AgentConfigurationModel] = Field(default_factory=list, description="Agent configurations (Agentic/Multi-Agentic only)")
    agent_tasks: List[AgentTaskModel] = Field(default_factory=list, description="Agent tasks (Agentic/Multi-Agentic only)")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "project_id": "proj-001",
                "overview": {
                    "project_name": "GenAI Customer Feedback Management",
                    "project_description": "A platform for feedback analysis.",
                    "business_goal": "Automate feedback categorization.",
                    "document_version": "1.0"
                },
                "ui_specifications": [],
                "api_specifications": [],
                "llm_prompts": [],
                "database_schema": [],
                "tech_stack": [],
                "traceability_matrix": [],
                "created_at": "2025-11-20T00:00:00",
                "updated_at": "2025-11-20T00:00:00"
            }
        }
