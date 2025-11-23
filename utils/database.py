"""
Database utility functions for SQLite persistence of BRD projects.
FIXED VERSION - Proper schema migration for template_type.
"""

import sqlite3
import json
import os
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)

# Database configuration
DB_PATH = "data/brd_projects.db"

def init_database():
    """Initialize the SQLite database with required tables."""
    try:
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if projects table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            # Create new table with all columns
            cursor.execute("""
                CREATE TABLE projects (
                    project_id TEXT PRIMARY KEY,
                    project_name TEXT NOT NULL,
                    template_type TEXT DEFAULT 'Normal',
                    overview_json TEXT NOT NULL,
                    ui_specs_json TEXT DEFAULT '[]',
                    api_specs_json TEXT DEFAULT '[]',
                    llm_prompts_json TEXT DEFAULT '[]',
                    db_schema_json TEXT DEFAULT '[]',
                    tech_stack_json TEXT DEFAULT '[]',
                    traceability_json TEXT DEFAULT '[]',
                    agent_architectures_json TEXT DEFAULT '[]',
                    agent_configurations_json TEXT DEFAULT '[]',
                    agent_tasks_json TEXT DEFAULT '[]',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            logger.info("Created new projects table with all columns")
        else:
            # Table exists, check for missing columns and add them
            cursor.execute("PRAGMA table_info(projects)")
            existing_columns = {row[1] for row in cursor.fetchall()}
            
            # List of columns that should exist
            required_columns = {
                'template_type': "ALTER TABLE projects ADD COLUMN template_type TEXT DEFAULT 'Normal'",
                'agent_architectures_json': "ALTER TABLE projects ADD COLUMN agent_architectures_json TEXT DEFAULT '[]'",
                'agent_configurations_json': "ALTER TABLE projects ADD COLUMN agent_configurations_json TEXT DEFAULT '[]'",
                'agent_tasks_json': "ALTER TABLE projects ADD COLUMN agent_tasks_json TEXT DEFAULT '[]'"
            }
            
            # Add missing columns
            for col_name, alter_sql in required_columns.items():
                if col_name not in existing_columns:
                    try:
                        cursor.execute(alter_sql)
                        logger.info(f"Added column: {col_name}")
                    except sqlite3.OperationalError as e:
                        if "duplicate column name" not in str(e):
                            logger.warning(f"Could not add column {col_name}: {e}")
        
        conn.commit()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise
    finally:
        conn.close()


def create_project(brd_project) -> str:
    """Create a new BRD project in the database."""
    try:
        init_database()
        
        project_id = f"proj-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Extract project name from overview
        project_name = brd_project.overview.project_name
        template_type = getattr(brd_project, 'template_type', 'Normal')
        
        # Log the values being inserted
        logger.info(f"Inserting: project_id={project_id}, project_name={project_name}, template_type={template_type}")
        
        cursor.execute("""
            INSERT INTO projects (
                project_id, project_name, template_type, overview_json, ui_specs_json,
                api_specs_json, llm_prompts_json, db_schema_json,
                tech_stack_json, traceability_json, agent_architectures_json,
                agent_configurations_json, agent_tasks_json, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            project_id,
            project_name,
            template_type,
            brd_project.overview.model_dump_json(),
            json.dumps([spec.model_dump() for spec in brd_project.ui_specifications]),
            json.dumps([spec.model_dump() for spec in brd_project.api_specifications]),
            json.dumps([spec.model_dump() for spec in brd_project.llm_prompts]),
            json.dumps([spec.model_dump() for spec in brd_project.database_schema]),
            json.dumps([spec.model_dump() for spec in brd_project.tech_stack]),
            json.dumps([spec.model_dump() for spec in brd_project.traceability_matrix]),
            json.dumps([spec.model_dump() for spec in getattr(brd_project, 'agent_architectures', [])]),
            json.dumps([spec.model_dump() for spec in getattr(brd_project, 'agent_configurations', [])]),
            json.dumps([spec.model_dump() for spec in getattr(brd_project, 'agent_tasks', [])]),
            now,
            now
        ))
        
        conn.commit()
        
        # Verify the insert
        cursor.execute("SELECT template_type FROM projects WHERE project_id = ?", (project_id,))
        result = cursor.fetchone()
        saved_template_type = result[0] if result else None
        logger.info(f"Verified: project_id={project_id} saved with template_type={saved_template_type}")
        
        if saved_template_type != template_type:
            logger.error(f"ERROR: template_type mismatch! Expected {template_type}, got {saved_template_type}")
        
        logger.info(f"Project created: {project_id} - {project_name} - Template: {template_type}")
        return project_id
        
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise
    finally:
        conn.close()


def get_project(project_id: str):
    """Retrieve a BRD project from the database."""
    try:
        from models.brd_models import (
            BRDProjectModel, OverviewModel, UISpecificationModel,
            APISpecificationModel, LLMPromptModel, DatabaseSchemaModel,
            TechStackModel, TraceabilityModel, AgentArchitectureModel,
            AgentConfigurationModel, AgentTaskModel
        )
        
        init_database()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM projects WHERE project_id = ?", (project_id,))
        row = cursor.fetchone()
        
        if not row:
            logger.warning(f"Project not found: {project_id}")
            return None
        
        # Get column names to properly map row values
        cursor.execute("PRAGMA table_info(projects)")
        column_info = cursor.fetchall()
        columns = {col[1]: col[0] for col in column_info}  # name -> index
        
        # Reconstruct the BRDProjectModel from the database row
        overview_dict = json.loads(row[columns.get('overview_json', 3)])
        overview = OverviewModel(**overview_dict)
        
        # Get template_type from the correct column
        template_type_idx = columns.get('template_type', 2)
        template_type = row[template_type_idx] if template_type_idx < len(row) and row[template_type_idx] else 'Normal'
        
        logger.info(f"Retrieved project {project_id} with template_type={template_type}")
        
        brd_project = BRDProjectModel(
            project_id=row[0],
            template_type=template_type,
            overview=overview,
            ui_specifications=[],
            api_specifications=[],
            llm_prompts=[],
            database_schema=[],
            tech_stack=[],
            traceability_matrix=[],
            agent_architectures=[],
            agent_configurations=[],
            agent_tasks=[]
        )
        
        # Load UI specifications
        ui_idx = columns.get('ui_specs_json')
        if ui_idx is not None and ui_idx < len(row) and row[ui_idx]:
            try:
                ui_specs = json.loads(row[ui_idx])
                brd_project.ui_specifications = [UISpecificationModel(**spec) for spec in ui_specs]
            except Exception as e:
                logger.warning(f"Error loading UI specs: {str(e)}")
        
        # Load API specifications
        api_idx = columns.get('api_specs_json')
        if api_idx is not None and api_idx < len(row) and row[api_idx]:
            try:
                api_specs = json.loads(row[api_idx])
                brd_project.api_specifications = [APISpecificationModel(**spec) for spec in api_specs]
            except Exception as e:
                logger.warning(f"Error loading API specs: {str(e)}")
        
        # Load LLM prompts
        llm_idx = columns.get('llm_prompts_json')
        if llm_idx is not None and llm_idx < len(row) and row[llm_idx]:
            try:
                llm_prompts = json.loads(row[llm_idx])
                brd_project.llm_prompts = [LLMPromptModel(**prompt) for prompt in llm_prompts]
            except Exception as e:
                logger.warning(f"Error loading LLM prompts: {str(e)}")
        
        # Load database schema
        db_idx = columns.get('db_schema_json')
        if db_idx is not None and db_idx < len(row) and row[db_idx]:
            try:
                db_schema = json.loads(row[db_idx])
                brd_project.database_schema = [DatabaseSchemaModel(**field) for field in db_schema]
            except Exception as e:
                logger.warning(f"Error loading database schema: {str(e)}")
        
        # Load tech stack
        tech_idx = columns.get('tech_stack_json')
        if tech_idx is not None and tech_idx < len(row) and row[tech_idx]:
            try:
                tech_stack = json.loads(row[tech_idx])
                brd_project.tech_stack = [TechStackModel(**tech) for tech in tech_stack]
            except Exception as e:
                logger.warning(f"Error loading tech stack: {str(e)}")
        
        # Load traceability matrix
        trace_idx = columns.get('traceability_json')
        if trace_idx is not None and trace_idx < len(row) and row[trace_idx]:
            try:
                traceability = json.loads(row[trace_idx])
                brd_project.traceability_matrix = [TraceabilityModel(**link) for link in traceability]
            except Exception as e:
                logger.warning(f"Error loading traceability matrix: {str(e)}")
        
        # Load agent architectures
        agent_arch_idx = columns.get('agent_architectures_json')
        if agent_arch_idx is not None and agent_arch_idx < len(row) and row[agent_arch_idx]:
            try:
                agents = json.loads(row[agent_arch_idx])
                brd_project.agent_architectures = [AgentArchitectureModel(**agent) for agent in agents]
            except Exception as e:
                logger.warning(f"Error loading agent architectures: {str(e)}")
        
        # Load agent configurations
        agent_config_idx = columns.get('agent_configurations_json')
        if agent_config_idx is not None and agent_config_idx < len(row) and row[agent_config_idx]:
            try:
                configs = json.loads(row[agent_config_idx])
                brd_project.agent_configurations = [AgentConfigurationModel(**config) for config in configs]
            except Exception as e:
                logger.warning(f"Error loading agent configurations: {str(e)}")
        
        # Load agent tasks
        agent_task_idx = columns.get('agent_tasks_json')
        if agent_task_idx is not None and agent_task_idx < len(row) and row[agent_task_idx]:
            try:
                tasks = json.loads(row[agent_task_idx])
                brd_project.agent_tasks = [AgentTaskModel(**task) for task in tasks]
            except Exception as e:
                logger.warning(f"Error loading agent tasks: {str(e)}")
        
        logger.info(f"Project retrieved: {project_id} - Template: {template_type}")
        return brd_project
        
    except Exception as e:
        logger.error(f"Error retrieving project: {str(e)}")
        raise
    finally:
        conn.close()


def update_project(brd_project) -> bool:
    """Update an existing BRD project in the database."""
    try:
        init_database()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        template_type = getattr(brd_project, 'template_type', 'Normal')
        
        logger.info(f"Updating project {brd_project.project_id} with template_type={template_type}")
        
        cursor.execute("""
            UPDATE projects SET
                project_name = ?,
                template_type = ?,
                overview_json = ?,
                ui_specs_json = ?,
                api_specs_json = ?,
                llm_prompts_json = ?,
                db_schema_json = ?,
                tech_stack_json = ?,
                traceability_json = ?,
                agent_architectures_json = ?,
                agent_configurations_json = ?,
                agent_tasks_json = ?,
                updated_at = ?
            WHERE project_id = ?
        """, (
            brd_project.overview.project_name,
            template_type,
            brd_project.overview.model_dump_json(),
            json.dumps([spec.model_dump() for spec in brd_project.ui_specifications]),
            json.dumps([spec.model_dump() for spec in brd_project.api_specifications]),
            json.dumps([spec.model_dump() for spec in brd_project.llm_prompts]),
            json.dumps([spec.model_dump() for spec in brd_project.database_schema]),
            json.dumps([spec.model_dump() for spec in brd_project.tech_stack]),
            json.dumps([spec.model_dump() for spec in brd_project.traceability_matrix]),
            json.dumps([spec.model_dump() for spec in getattr(brd_project, 'agent_architectures', [])]),
            json.dumps([spec.model_dump() for spec in getattr(brd_project, 'agent_configurations', [])]),
            json.dumps([spec.model_dump() for spec in getattr(brd_project, 'agent_tasks', [])]),
            now,
            brd_project.project_id
        ))
        
        conn.commit()
        logger.info(f"Project updated: {brd_project.project_id} - Template: {template_type}")
        return True
        
    except Exception as e:
        logger.error(f"Error updating project: {str(e)}")
        raise
    finally:
        conn.close()


def delete_project(project_id: str) -> bool:
    """Delete a BRD project from the database."""
    try:
        init_database()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM projects WHERE project_id = ?", (project_id,))
        conn.commit()
        
        logger.info(f"Project deleted: {project_id}")
        return True
        
    except Exception as e:
        logger.error(f"Error deleting project: {str(e)}")
        raise
    finally:
        conn.close()


def list_projects() -> List[Dict[str, Any]]:
    """List all BRD projects in the database."""
    try:
        init_database()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT project_id, project_name, template_type, created_at, updated_at
            FROM projects
            ORDER BY updated_at DESC
        """)
        
        rows = cursor.fetchall()
        
        projects = [
            {
                'project_id': row[0],
                'project_name': row[1],
                'template_type': row[2] if len(row) > 2 else 'Normal',
                'created_at': row[3] if len(row) > 3 else '',
                'updated_at': row[4] if len(row) > 4 else ''
            }
            for row in rows
        ]
        
        logger.info(f"Listed {len(projects)} projects")
        return projects
        
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        return []
    finally:
        conn.close()


def get_project_count() -> int:
    """Get the total number of projects."""
    try:
        init_database()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()[0]
        
        logger.info(f"Total projects: {count}")
        return count
        
    except Exception as e:
        logger.error(f"Error getting project count: {str(e)}")
        return 0
    finally:
        conn.close()


def export_project_data(project_id: str) -> Dict[str, Any]:
    """Export project data as dictionary."""
    try:
        project = get_project(project_id)
        
        if not project:
            logger.warning(f"Cannot export: Project not found: {project_id}")
            return None
        
        data = {
            'project_id': project.project_id,
            'template_type': getattr(project, 'template_type', 'Normal'),
            'overview': project.overview.model_dump(),
            'ui_specifications': [spec.model_dump() for spec in project.ui_specifications],
            'api_specifications': [spec.model_dump() for spec in project.api_specifications],
            'llm_prompts': [prompt.model_dump() for prompt in project.llm_prompts],
            'database_schema': [field.model_dump() for field in project.database_schema],
            'tech_stack': [tech.model_dump() for tech in project.tech_stack],
            'traceability_matrix': [link.model_dump() for link in project.traceability_matrix],
            'agent_architectures': [agent.model_dump() for agent in getattr(project, 'agent_architectures', [])],
            'agent_configurations': [config.model_dump() for config in getattr(project, 'agent_configurations', [])],
            'agent_tasks': [task.model_dump() for task in getattr(project, 'agent_tasks', [])]
        }
        
        logger.info(f"Project data exported: {project_id}")
        return data
        
    except Exception as e:
        logger.error(f"Error exporting project data: {str(e)}")
        raise


def import_project_data(data: Dict[str, Any]) -> str:
    """Import project data from dictionary."""
    try:
        from models.brd_models import (
            BRDProjectModel, OverviewModel, UISpecificationModel,
            APISpecificationModel, LLMPromptModel, DatabaseSchemaModel,
            TechStackModel, TraceabilityModel, AgentArchitectureModel,
            AgentConfigurationModel, AgentTaskModel
        )
        
        # Reconstruct project from data
        overview = OverviewModel(**data['overview'])
        
        brd_project = BRDProjectModel(
            template_type=data.get('template_type', 'Normal'),
            overview=overview,
            ui_specifications=[UISpecificationModel(**spec) for spec in data.get('ui_specifications', [])],
            api_specifications=[APISpecificationModel(**spec) for spec in data.get('api_specifications', [])],
            llm_prompts=[LLMPromptModel(**prompt) for prompt in data.get('llm_prompts', [])],
            database_schema=[DatabaseSchemaModel(**field) for field in data.get('database_schema', [])],
            tech_stack=[TechStackModel(**tech) for tech in data.get('tech_stack', [])],
            traceability_matrix=[TraceabilityModel(**link) for link in data.get('traceability_matrix', [])],
            agent_architectures=[AgentArchitectureModel(**agent) for agent in data.get('agent_architectures', [])],
            agent_configurations=[AgentConfigurationModel(**config) for config in data.get('agent_configurations', [])],
            agent_tasks=[AgentTaskModel(**task) for task in data.get('agent_tasks', [])]
        )
        
        project_id = create_project(brd_project)
        logger.info(f"Project imported: {project_id}")
        return project_id
        
    except Exception as e:
        logger.error(f"Error importing project data: {str(e)}")
        raise
