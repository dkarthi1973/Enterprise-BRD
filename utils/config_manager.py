"""
Configuration Manager Utility
Handles centralized configuration management, import/export, and system settings
"""

import json
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime


class ConfigManager:
    """Manages application configuration with YAML and JSON support"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.configs = {}
        self.load_all_configs()
    
    def load_all_configs(self):
        """Load all configuration files from config directory"""
        for config_file in self.config_dir.glob("*.yaml"):
            config_name = config_file.stem
            self.load_config(config_name)
        for config_file in self.config_dir.glob("*.json"):
            config_name = config_file.stem
            self.load_config(config_name)
    
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """Load a specific configuration file"""
        try:
            yaml_path = self.config_dir / f"{config_name}.yaml"
            json_path = self.config_dir / f"{config_name}.json"
            
            if yaml_path.exists():
                with open(yaml_path, 'r') as f:
                    config = yaml.safe_load(f) or {}
            elif json_path.exists():
                with open(json_path, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
            
            self.configs[config_name] = config
            return config
        except Exception as e:
            raise Exception(f"Failed to load config {config_name}: {str(e)}")
    
    def get_config(self, config_name: str) -> Dict[str, Any]:
        """Get a configuration by name"""
        if config_name not in self.configs:
            self.load_config(config_name)
        return self.configs.get(config_name, {})
    
    def get_value(self, config_name: str, key_path: str, default: Any = None) -> Any:
        """Get a specific value from configuration using dot notation"""
        config = self.get_config(config_name)
        keys = key_path.split('.')
        value = config
        
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        
        return value if value is not None else default
    
    def set_value(self, config_name: str, key_path: str, value: Any):
        """Set a specific value in configuration using dot notation"""
        if config_name not in self.configs:
            self.configs[config_name] = {}
        
        config = self.configs[config_name]
        keys = key_path.split('.')
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
    
    def save_config(self, config_name: str, format: str = 'yaml'):
        """Save configuration to file"""
        try:
            if config_name not in self.configs:
                raise Exception(f"Configuration {config_name} not found")
            
            config = self.configs[config_name]
            
            if format == 'yaml':
                file_path = self.config_dir / f"{config_name}.yaml"
                with open(file_path, 'w') as f:
                    yaml.dump(config, f, default_flow_style=False)
            elif format == 'json':
                file_path = self.config_dir / f"{config_name}.json"
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=2)
            else:
                raise ValueError(f"Unsupported format: {format}")
        except Exception as e:
            raise Exception(f"Failed to save config {config_name}: {str(e)}")
    
    def create_config(self, config_name: str, initial_data: Dict[str, Any] = None):
        """Create a new configuration"""
        self.configs[config_name] = initial_data or {}
    
    def delete_config(self, config_name: str):
        """Delete a configuration"""
        if config_name in self.configs:
            del self.configs[config_name]
        
        # Delete files
        yaml_path = self.config_dir / f"{config_name}.yaml"
        json_path = self.config_dir / f"{config_name}.json"
        
        if yaml_path.exists():
            yaml_path.unlink()
        if json_path.exists():
            json_path.unlink()
    
    def export_config(self, config_name: str, format: str = 'json') -> str:
        """Export configuration as string"""
        config = self.get_config(config_name)
        
        if format == 'json':
            return json.dumps(config, indent=2)
        elif format == 'yaml':
            return yaml.dump(config, default_flow_style=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_config(self, config_name: str, config_data: str, format: str = 'json'):
        """Import configuration from string"""
        try:
            if format == 'json':
                config = json.loads(config_data)
            elif format == 'yaml':
                config = yaml.safe_load(config_data)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            self.configs[config_name] = config
        except Exception as e:
            raise Exception(f"Failed to import config: {str(e)}")
    
    def merge_configs(self, config_name: str, other_config: Dict[str, Any]):
        """Merge another configuration into existing one"""
        if config_name not in self.configs:
            self.configs[config_name] = {}
        
        self._deep_merge(self.configs[config_name], other_config)
    
    def _deep_merge(self, target: Dict, source: Dict):
        """Deep merge source dict into target dict"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def list_configs(self) -> list:
        """List all loaded configurations"""
        return list(self.configs.keys())
    
    def validate_config(self, config_name: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration against a schema"""
        config = self.get_config(config_name)
        errors = []
        warnings = []
        
        # Simple validation - can be extended
        for key, expected_type in schema.items():
            if key not in config:
                errors.append(f"Missing required key: {key}")
            elif not isinstance(config[key], expected_type):
                errors.append(f"Invalid type for {key}: expected {expected_type.__name__}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


class SystemConfig:
    """System configuration manager"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.system_config = config_manager.get_config('system')
    
    def get_app_title(self) -> str:
        """Get application title"""
        return self.config_manager.get_value('system', 'app.title', 'BRD Template Tool')
    
    def get_app_version(self) -> str:
        """Get application version"""
        return self.config_manager.get_value('system', 'app.version', '2.0.0')
    
    def get_debug_mode(self) -> bool:
        """Check if debug mode is enabled"""
        return self.config_manager.get_value('system', 'app.debug', False)
    
    def get_database_path(self) -> str:
        """Get database path"""
        return self.config_manager.get_value('system', 'database.path', 'brd_templates.db')
    
    def get_log_level(self) -> str:
        """Get log level"""
        return self.config_manager.get_value('system', 'logging.level', 'INFO')
    
    def get_log_file(self) -> str:
        """Get log file path"""
        return self.config_manager.get_value('system', 'logging.file', 'app.log')
    
    def get_max_upload_size_mb(self) -> int:
        """Get maximum upload size in MB"""
        return self.config_manager.get_value('system', 'upload.max_size_mb', 50)
    
    def get_session_timeout_minutes(self) -> int:
        """Get session timeout in minutes"""
        return self.config_manager.get_value('system', 'session.timeout_minutes', 30)
    
    def get_ollama_host(self) -> str:
        """Get Ollama host URL"""
        return self.config_manager.get_value('system', 'ollama.host', 'http://localhost:11434')
    
    def get_enabled_models(self) -> list:
        """Get list of enabled LLM models"""
        return self.config_manager.get_value('system', 'llm.enabled_models', [
            'mistral', 'llama3.2', 'deepseek-r1', 'phi4-mini'
        ])
    
    def get_feature_flags(self) -> Dict[str, bool]:
        """Get all feature flags"""
        return self.config_manager.get_value('system', 'features', {
            'ai_suggestions': True,
            'template_versioning': True,
            'export_excel': True,
            'governance_framework': True
        })
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled"""
        flags = self.get_feature_flags()
        return flags.get(feature_name, False)
    
    def update_feature_flag(self, feature_name: str, enabled: bool):
        """Update a feature flag"""
        self.config_manager.set_value('system', f'features.{feature_name}', enabled)
        self.config_manager.save_config('system')


class TemplateDefaults:
    """Template defaults configuration"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.defaults = config_manager.get_config('template_defaults')
    
    def get_normal_template_defaults(self) -> Dict[str, Any]:
        """Get defaults for Normal BRD template"""
        return self.config_manager.get_value('template_defaults', 'normal', {})
    
    def get_agentic_template_defaults(self) -> Dict[str, Any]:
        """Get defaults for Agentic BRD template"""
        return self.config_manager.get_value('template_defaults', 'agentic', {})
    
    def get_multi_agentic_template_defaults(self) -> Dict[str, Any]:
        """Get defaults for Multi-Agentic BRD template"""
        return self.config_manager.get_value('template_defaults', 'multi_agentic', {})


class LLMConfig:
    """LLM configuration manager"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.llm_config = config_manager.get_config('llm_config')
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get configuration for a specific model"""
        return self.config_manager.get_value('llm_config', f'models.{model_name}', {})
    
    def get_default_temperature(self) -> float:
        """Get default temperature"""
        return self.config_manager.get_value('llm_config', 'defaults.temperature', 0.7)
    
    def get_default_max_tokens(self) -> int:
        """Get default max tokens"""
        return self.config_manager.get_value('llm_config', 'defaults.max_tokens', 2000)
    
    def get_default_top_p(self) -> float:
        """Get default top_p"""
        return self.config_manager.get_value('llm_config', 'defaults.top_p', 0.9)


class GovernanceConfig:
    """Governance configuration manager"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.governance_config = config_manager.get_config('governance')
    
    def is_governance_enabled(self) -> bool:
        """Check if governance is enabled"""
        return self.config_manager.get_value('governance', 'enabled', True)
    
    def get_input_guardrails(self) -> Dict[str, Any]:
        """Get input guardrails configuration"""
        return self.config_manager.get_value('governance', 'guardrails.input', {})
    
    def get_output_guardrails(self) -> Dict[str, Any]:
        """Get output guardrails configuration"""
        return self.config_manager.get_value('governance', 'guardrails.output', {})
    
    def get_compliance_policies(self) -> Dict[str, Any]:
        """Get compliance policies"""
        return self.config_manager.get_value('governance', 'compliance', {})
