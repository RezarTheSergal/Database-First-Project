from functools import wraps
import time
from typing import Callable
from sqlalchemy.exc import (
    SQLAlchemyError, IntegrityError, DataError, DatabaseError,
    OperationalError, ProgrammingError, InvalidRequestError,
    TimeoutError as SQLTimeoutError, DisconnectionError
)
from psycopg2.errors import (
    UniqueViolation, ForeignKeyViolation, NotNullViolation,
    CheckViolation, StringDataRightTruncation
)
import logging

from .responce_types import ErrorCode, DatabaseResponse
from .exception_handler import ExceptionHandler, T, P

class DatabaseErrorHandler(ExceptionHandler):
    """Централизованный обработчик ошибок базы данных"""

    ERROR_MAPPING = {
        # SQLAlchemy errors
        OperationalError: ErrorCode.CONNECTION_FAILED,
        SQLTimeoutError: ErrorCode.QUERY_TIMEOUT,
        DisconnectionError: ErrorCode.CONNECTION_LOST,
        ProgrammingError: ErrorCode.QUERY_SYNTAX_ERROR,
        DataError: ErrorCode.INVALID_DATA_TYPE,
        InvalidRequestError: ErrorCode.INVALID_PARAMETERS,
        
        # PostgreSQL specific errors
        UniqueViolation: ErrorCode.DUPLICATE_KEY,
        ForeignKeyViolation: ErrorCode.FOREIGN_KEY_VIOLATION,
        NotNullViolation: ErrorCode.NULL_VALUE_NOT_ALLOWED,
        CheckViolation: ErrorCode.CHECK_CONSTRAINT_VIOLATION,
        StringDataRightTruncation: ErrorCode.DATA_TOO_LONG,
    }
    
    @classmethod
    def handle_exception(cls, e: Exception, operation: str = "") -> DatabaseResponse:
        """Обработка исключений и преобразование в стандартизированный ответ"""
        
        logging.error(f"Database error during {operation}: {str(e)}", exc_info=True)
        
        # Определяем тип ошибки и соответствующий код
        error_code = cls.ERROR_MAPPING.get(type(e), ErrorCode.UNKNOWN_ERROR)
        
        # Формируем детальное описание ошибки
        error_details = {
            "operation": operation,
            "exception_type": type(e).__name__,
            "original_message": str(e)
        }
        
        # Специальная обработка для IntegrityError
        if isinstance(e, IntegrityError):
            if "duplicate key" in str(e).lower():
                error_code = ErrorCode.DUPLICATE_KEY
                message = "Попытка вставить дублирующиеся данные"
            elif "foreign key" in str(e).lower():
                error_code = ErrorCode.FOREIGN_KEY_VIOLATION
                message = "Нарушение внешнего ключа"
            elif "not null" in str(e).lower():
                error_code = ErrorCode.NULL_VALUE_NOT_ALLOWED
                message = "Обязательное поле не может быть пустым"
            else:
                message = "Нарушение целостности данных"
        
        # Специальная обработка для других типов ошибок
        elif isinstance(e, OperationalError):
            if "timeout" in str(e).lower():
                error_code = ErrorCode.QUERY_TIMEOUT
                message = "Превышено время ожидания операции"
            elif "connection" in str(e).lower():
                error_code = ErrorCode.CONNECTION_FAILED
                message = "Ошибка подключения к базе данных"
            else:
                message = "Операционная ошибка базы данных"
        
        elif isinstance(e, ProgrammingError):
            if "table" in str(e).lower() and "does not exist" in str(e).lower():
                error_code = ErrorCode.TABLE_NOT_FOUND
                message = "Указанная таблица не существует"
            elif "column" in str(e).lower() and "does not exist" in str(e).lower():
                error_code = ErrorCode.COLUMN_NOT_FOUND
                message = "Указанная колонка не существует"
            else:
                message = "Синтаксическая ошибка в запросе"
        
        else:
            message = f"Неожиданная ошибка: {str(e)}"
        
        return DatabaseResponse.error(
            error_code=error_code,
            message=message,
            error_details=error_details
        )
    
    # Декоратор для автоматической обработки ошибок
    def __call__(self, func:Callable[P, T]) -> Callable[P, T]:
        """Декоратор для автоматической обработки ошибок БД"""
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for i in range(self.max_retries+1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i != self.max_retries:
                        if self.log_error and self.logger:
                            self.logger.error(
                                f"Ошибка в {func.__name__}: {e}, Поытка номер: {i+1}/{self.max_retries}", 
                                exc_info=True
                            )
                        if self.max_retries > i:
                            time.sleep(self.retry_after)
                            continue
                    return DatabaseErrorHandler.handle_exception(
                        e, 
                        func.__name__
                    )
            return DatabaseResponse.error(
                error_code=ErrorCode.UNKNOWN_ERROR,
                message=f"Неожиданное завершение функции {func.__name__}",
                error_details={}
            )
        return wrapper
