"""
Logger Utility
Comprehensive logging and audit trail management
"""

import logging
import json
import sqlite3
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
from enum import Enum


class LogLevel(str, Enum):
    """Log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class EventType(str, Enum):
    """Audit event types"""
    TEMPLATE_CREATED = "template_created"
    TEMPLATE_UPDATED = "template_updated"
    TEMPLATE_DELETED = "template_deleted"
    TEMPLATE_EXPORTED = "template_exported"
    TEMPLATE_IMPORTED = "template_imported"
    TEMPLATE_VALIDATED = "template_validated"
    LLM_CALL = "llm_call"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    CONFIG_CHANGED = "config_changed"
    GOVERNANCE_VIOLATION = "governance_violation"
    ERROR = "error"
    WARNING = "warning"


class AppLogger:
    """Application logger with file and database support"""
    
    def __init__(self, log_file: str = "app.log", db_path: str = "audit.db"):
        self.log_file = log_file
        self.db_path = db_path
        self.logger = self._setup_logger()
        self._init_audit_db()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup Python logger"""
        logger = logging.getLogger('brd_tool')
        logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _init_audit_db(self):
        """Initialize audit database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                event_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT NOT NULL,
                user_id TEXT,
                resource_id TEXT,
                resource_type TEXT,
                action TEXT,
                details TEXT,
                status TEXT,
                ip_address TEXT,
                user_agent TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_log (
                error_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_type TEXT,
                error_message TEXT,
                stack_trace TEXT,
                context TEXT,
                severity TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_log (
                perf_id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                operation TEXT,
                duration_ms FLOAT,
                resource_id TEXT,
                status TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def log_event(self, event_type: EventType, user_id: str, resource_id: str = None,
                  resource_type: str = None, action: str = None, details: Dict[str, Any] = None,
                  status: str = "success", ip_address: str = None, user_agent: str = None) -> str:
        """Log an audit event"""
        try:
            event_id = f"evt_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO audit_log 
                (event_id, event_type, user_id, resource_id, resource_type, action, details, status, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_id,
                event_type.value,
                user_id,
                resource_id,
                resource_type,
                action,
                json.dumps(details) if details else None,
                status,
                ip_address,
                user_agent
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Event: {event_type.value} - Resource: {resource_id} - Status: {status}")
            
            return event_id
        except Exception as e:
            self.logger.error(f"Failed to log event: {str(e)}")
            raise
    
    def log_error(self, error_type: str, error_message: str, stack_trace: str = None,
                  context: Dict[str, Any] = None, severity: str = "error") -> str:
        """Log an error"""
        try:
            error_id = f"err_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO error_log 
                (error_id, error_type, error_message, stack_trace, context, severity)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                error_id,
                error_type,
                error_message,
                stack_trace,
                json.dumps(context) if context else None,
                severity
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.error(f"{error_type}: {error_message}")
            
            return error_id
        except Exception as e:
            self.logger.error(f"Failed to log error: {str(e)}")
            raise
    
    def log_performance(self, operation: str, duration_ms: float, resource_id: str = None,
                       status: str = "success") -> str:
        """Log performance metrics"""
        try:
            perf_id = f"perf_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}"
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO performance_log 
                (perf_id, operation, duration_ms, resource_id, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                perf_id,
                operation,
                duration_ms,
                resource_id,
                status
            ))
            
            conn.commit()
            conn.close()
            
            self.logger.debug(f"Performance: {operation} - {duration_ms}ms")
            
            return perf_id
        except Exception as e:
            self.logger.error(f"Failed to log performance: {str(e)}")
            raise
    
    def get_audit_log(self, limit: int = 100, event_type: str = None, user_id: str = None) -> list:
        """Retrieve audit log entries"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM audit_log WHERE 1=1"
            params = []
            
            if event_type:
                query += " AND event_type = ?"
                params.append(event_type)
            
            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            return results
        except Exception as e:
            self.logger.error(f"Failed to retrieve audit log: {str(e)}")
            raise
    
    def get_error_log(self, limit: int = 100, severity: str = None) -> list:
        """Retrieve error log entries"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM error_log WHERE 1=1"
            params = []
            
            if severity:
                query += " AND severity = ?"
                params.append(severity)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            return results
        except Exception as e:
            self.logger.error(f"Failed to retrieve error log: {str(e)}")
            raise
    
    def get_performance_log(self, operation: str = None, limit: int = 100) -> list:
        """Retrieve performance log entries"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = "SELECT * FROM performance_log WHERE 1=1"
            params = []
            
            if operation:
                query += " AND operation = ?"
                params.append(operation)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()
            
            return results
        except Exception as e:
            self.logger.error(f"Failed to retrieve performance log: {str(e)}")
            raise
    
    def cleanup_old_logs(self, days: int = 30):
        """Delete logs older than specified days"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_date = datetime.utcnow().timestamp() - (days * 86400)
            
            cursor.execute("DELETE FROM audit_log WHERE timestamp < datetime(?, 'unixepoch')", (cutoff_date,))
            cursor.execute("DELETE FROM error_log WHERE timestamp < datetime(?, 'unixepoch')", (cutoff_date,))
            cursor.execute("DELETE FROM performance_log WHERE timestamp < datetime(?, 'unixepoch')", (cutoff_date,))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Cleaned up logs older than {days} days")
        except Exception as e:
            self.logger.error(f"Failed to cleanup logs: {str(e)}")
            raise
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get logging statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM audit_log")
            audit_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM error_log")
            error_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM performance_log")
            perf_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT user_id) FROM audit_log")
            unique_users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(DISTINCT event_type) FROM audit_log")
            event_types = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'audit_log_entries': audit_count,
                'error_log_entries': error_count,
                'performance_log_entries': perf_count,
                'unique_users': unique_users,
                'event_types': event_types
            }
        except Exception as e:
            self.logger.error(f"Failed to get statistics: {str(e)}")
            raise
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message)
