"""
Template Manager Utility
Handles template CRUD operations, versioning, validation, and import/export
"""

import json
import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
from models.template_models import (
    TemplateType, NormalBRDTemplate, AgenticBRDTemplate, 
    MultiAgenticBRDTemplate, ProjectMetadata, get_template_by_type
)


class TemplateManager:
    """Manages BRD templates with CRUD operations and versioning"""
    
    def __init__(self, db_path: str = "brd_templates.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize template database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Templates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS templates (
                template_id TEXT PRIMARY KEY,
                project_id TEXT UNIQUE NOT NULL,
                template_type TEXT NOT NULL,
                project_name TEXT NOT NULL,
                description TEXT,
                created_by TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_modified_by TEXT,
                last_modified_at TIMESTAMP,
                status TEXT DEFAULT 'draft',
                version TEXT DEFAULT '1.0',
                content TEXT NOT NULL,
                tags TEXT
            )
        """)
        
        # Template versions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS template_versions (
                version_id TEXT PRIMARY KEY,
                template_id TEXT NOT NULL,
                version_number TEXT NOT NULL,
                created_by TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                changes TEXT,
                content TEXT NOT NULL,
                FOREIGN KEY (template_id) REFERENCES templates(template_id)
            )
        """)
        
        # Validation history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS validation_history (
                validation_id TEXT PRIMARY KEY,
                template_id TEXT NOT NULL,
                validation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                validation_result TEXT,
                errors TEXT,
                warnings TEXT,
                FOREIGN KEY (template_id) REFERENCES templates(template_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_template(self, template_data: Dict[str, Any], user_id: str) -> str:
        """Create a new template"""
        try:
            template_id = f"tpl_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            project_id = template_data.get('metadata', {}).get('project_id')
            template_type = template_data.get('metadata', {}).get('template_type')
            
            # Validate template data
            template_class = get_template_by_type(TemplateType(template_type))
            validated_template = template_class(**template_data)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO templates 
                (template_id, project_id, template_type, project_name, description, 
                 created_by, last_modified_by, content, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                template_id,
                project_id,
                template_type,
                template_data.get('metadata', {}).get('project_name'),
                template_data.get('metadata', {}).get('project_description'),
                user_id,
                user_id,
                json.dumps(template_data, default=str),
                json.dumps(template_data.get('metadata', {}).get('tags', []))
            ))
            
            conn.commit()
            conn.close()
            
            return template_id
        except Exception as e:
            raise Exception(f"Failed to create template: {str(e)}")
    
    def get_template(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a template by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT content FROM templates WHERE template_id = ?", (template_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return json.loads(result[0])
            return None
        except Exception as e:
            raise Exception(f"Failed to retrieve template: {str(e)}")
    
    def list_templates(self, template_type: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all templates with optional filtering"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT template_id, project_id, project_name, template_type, status, version, created_at FROM templates WHERE 1=1"
            params = []
            
            if template_type:
                query += " AND template_type = ?"
                params.append(template_type)
            
            if status:
                query += " AND status = ?"
                params.append(status)
            
            query += " ORDER BY created_at DESC"
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            templates = []
            for row in results:
                templates.append({
                    'template_id': row[0],
                    'project_id': row[1],
                    'project_name': row[2],
                    'template_type': row[3],
                    'status': row[4],
                    'version': row[5],
                    'created_at': row[6]
                })
            
            return templates
        except Exception as e:
            raise Exception(f"Failed to list templates: {str(e)}")
    
    def update_template(self, template_id: str, template_data: Dict[str, Any], user_id: str) -> bool:
        """Update an existing template"""
        try:
            # Validate template data
            template_type = template_data.get('metadata', {}).get('template_type')
            template_class = get_template_by_type(TemplateType(template_type))
            validated_template = template_class(**template_data)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE templates 
                SET content = ?, last_modified_by = ?, last_modified_at = CURRENT_TIMESTAMP
                WHERE template_id = ?
            """, (json.dumps(template_data, default=str), user_id, template_id))
            
            conn.commit()
            conn.close()
            
            return cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Failed to update template: {str(e)}")
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a template"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete versions first
            cursor.execute("DELETE FROM template_versions WHERE template_id = ?", (template_id,))
            
            # Delete validation history
            cursor.execute("DELETE FROM validation_history WHERE template_id = ?", (template_id,))
            
            # Delete template
            cursor.execute("DELETE FROM templates WHERE template_id = ?", (template_id,))
            
            conn.commit()
            conn.close()
            
            return cursor.rowcount > 0
        except Exception as e:
            raise Exception(f"Failed to delete template: {str(e)}")
    
    def save_version(self, template_id: str, changes: str, user_id: str) -> str:
        """Save a new version of template"""
        try:
            template = self.get_template(template_id)
            if not template:
                raise Exception("Template not found")
            
            # Get current version number
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT version FROM templates WHERE template_id = ?", (template_id,))
            result = cursor.fetchone()
            current_version = result[0] if result else "1.0"
            
            # Increment version
            version_parts = current_version.split('.')
            version_parts[-1] = str(int(version_parts[-1]) + 1)
            new_version = '.'.join(version_parts)
            
            version_id = f"v_{template_id}_{new_version}"
            
            cursor.execute("""
                INSERT INTO template_versions 
                (version_id, template_id, version_number, created_by, changes, content)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                version_id,
                template_id,
                new_version,
                user_id,
                changes,
                json.dumps(template, default=str)
            ))
            
            # Update main template version
            cursor.execute("""
                UPDATE templates SET version = ? WHERE template_id = ?
            """, (new_version, template_id))
            
            conn.commit()
            conn.close()
            
            return version_id
        except Exception as e:
            raise Exception(f"Failed to save version: {str(e)}")
    
    def get_template_versions(self, template_id: str) -> List[Dict[str, Any]]:
        """Get all versions of a template"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT version_id, version_number, created_by, created_at, changes 
                FROM template_versions 
                WHERE template_id = ? 
                ORDER BY created_at DESC
            """, (template_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            versions = []
            for row in results:
                versions.append({
                    'version_id': row[0],
                    'version_number': row[1],
                    'created_by': row[2],
                    'created_at': row[3],
                    'changes': row[4]
                })
            
            return versions
        except Exception as e:
            raise Exception(f"Failed to get versions: {str(e)}")
    
    def validate_template(self, template_id: str) -> Dict[str, Any]:
        """Validate template structure and content"""
        try:
            template = self.get_template(template_id)
            if not template:
                return {'valid': False, 'errors': ['Template not found']}
            
            template_type = template.get('metadata', {}).get('template_type')
            template_class = get_template_by_type(TemplateType(template_type))
            
            try:
                validated = template_class(**template)
                
                # Record validation
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                validation_id = f"val_{template_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
                cursor.execute("""
                    INSERT INTO validation_history 
                    (validation_id, template_id, validation_result)
                    VALUES (?, ?, ?)
                """, (validation_id, template_id, 'valid'))
                
                conn.commit()
                conn.close()
                
                return {'valid': True, 'errors': [], 'warnings': []}
            except Exception as e:
                return {'valid': False, 'errors': [str(e)]}
        except Exception as e:
            raise Exception(f"Failed to validate template: {str(e)}")
    
    def export_template(self, template_id: str, export_format: str = 'json') -> str:
        """Export template in specified format"""
        try:
            template = self.get_template(template_id)
            if not template:
                raise Exception("Template not found")
            
            if export_format == 'json':
                return json.dumps(template, indent=2, default=str)
            else:
                raise ValueError(f"Unsupported export format: {export_format}")
        except Exception as e:
            raise Exception(f"Failed to export template: {str(e)}")
    
    def import_template(self, template_data: str, user_id: str, import_format: str = 'json') -> str:
        """Import template from specified format"""
        try:
            if import_format == 'json':
                data = json.loads(template_data)
            else:
                raise ValueError(f"Unsupported import format: {import_format}")
            
            return self.create_template(data, user_id)
        except Exception as e:
            raise Exception(f"Failed to import template: {str(e)}")
    
    def get_validation_history(self, template_id: str) -> List[Dict[str, Any]]:
        """Get validation history for a template"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT validation_id, validation_timestamp, validation_result, errors, warnings
                FROM validation_history
                WHERE template_id = ?
                ORDER BY validation_timestamp DESC
            """, (template_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            history = []
            for row in results:
                history.append({
                    'validation_id': row[0],
                    'timestamp': row[1],
                    'result': row[2],
                    'errors': json.loads(row[3]) if row[3] else [],
                    'warnings': json.loads(row[4]) if row[4] else []
                })
            
            return history
        except Exception as e:
            raise Exception(f"Failed to get validation history: {str(e)}")
