from enum import Enum
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
import json

class ResponseStatus(Enum):
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"

class ErrorCode(Enum):
    # Database connection errors
    CONNECTION_FAILED = "DB_CONNECTION_FAILED"
    CONNECTION_TIMEOUT = "DB_CONNECTION_TIMEOUT"
    CONNECTION_LOST = "DB_CONNECTION_LOST"
    
    # Table/Model errors
    TABLE_NOT_FOUND = "TABLE_NOT_FOUND"
    MODEL_NOT_FOUND = "MODEL_NOT_FOUND"
    INVALID_TABLE_NAME = "INVALID_TABLE_NAME"
    
    # Column errors
    COLUMN_NOT_FOUND = "COLUMN_NOT_FOUND"
    INVALID_COLUMN_TYPE = "INVALID_COLUMN_TYPE"
    MISSING_REQUIRED_COLUMNS = "MISSING_REQUIRED_COLUMNS"
    
    # Data validation errors
    INVALID_DATA_TYPE = "INVALID_DATA_TYPE"
    DATA_TOO_LONG = "DATA_TOO_LONG"
    NULL_VALUE_NOT_ALLOWED = "NULL_VALUE_NOT_ALLOWED"
    DUPLICATE_KEY = "DUPLICATE_KEY"
    FOREIGN_KEY_VIOLATION = "FOREIGN_KEY_VIOLATION"
    CHECK_CONSTRAINT_VIOLATION = "CHECK_CONSTRAINT_VIOLATION"
    
    # Query errors
    INVALID_FILTER = "INVALID_FILTER"
    INVALID_ORDER_BY = "INVALID_ORDER_BY"
    QUERY_SYNTAX_ERROR = "QUERY_SYNTAX_ERROR"
    QUERY_TIMEOUT = "QUERY_TIMEOUT"
    
    # Permission errors
    ACCESS_DENIED = "ACCESS_DENIED"
    INSUFFICIENT_PRIVILEGES = "INSUFFICIENT_PRIVILEGES"
    
    # General errors
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INVALID_PARAMETERS = "INVALID_PARAMETERS"
    OPERATION_FAILED = "OPERATION_FAILED"
    TRANSACTION_FAILED = "TRANSACTION_FAILED"

@dataclass
class DatabaseResponse:
    """Стандартизированный ответ для всех операций с БД"""
    status: ResponseStatus
    data: Optional[Any] = None
    message: str = ""
    error_code: Optional[ErrorCode] = None
    error_details: Optional[Dict[str, Any]] = None
    affected_rows: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразование в словарь для отправки на фронтенд"""
        result = {
            "status": self.status.value,
            "message": self.message
        }
        
        if self.data is not None:
            result["data"] = self.data
            
        if self.error_code:
            result["error_code"] = self.error_code.value
            
        if self.error_details:
            result["error_details"] = self.error_details
            
        if self.affected_rows is not None:
            result["affected_rows"] = self.affected_rows
            
        return result
    
    def to_json(self) -> str:
        """Преобразование в JSON для API ответов"""
        return json.dumps(self.to_dict(), ensure_ascii=False, default=str)
    
    @classmethod
    def success(cls, data: Any = None, message: str = "Операция выполнена успешно", affected_rows: Optional[int] = None):
        return cls(
            status=ResponseStatus.SUCCESS,
            data=data,
            message=message,
            affected_rows=affected_rows
        )
    
    @classmethod
    def error(cls, error_code: ErrorCode, message: str, error_details: Optional[Dict[str, Any]] = None):
        return cls(
            status=ResponseStatus.ERROR,
            message=message,
            error_code=error_code,
            error_details=error_details
        )
    
    @classmethod
    def warning(cls, message: str, data: Any = None):
        return cls(
            status=ResponseStatus.WARNING,
            message=message,
            data=data
        )