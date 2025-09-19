# - лог-файл приложения (уровни INFO/ERROR) с временными метками: попытки
# подключения, выполненные DDL/DML, ошибки ограничений. (drpepperus666)

import logging
from functools import wraps
from typing import Callable, Any, Optional, Tuple, Type

class ExceptionHandler:
    """Класс для обработки исключений с централизованной настройкой логирования"""
    
    # Статические настройки по умолчанию
    _default_logger = None
    _is_configured = False
    
    @classmethod
    def configure_logging(
        cls,
        level: int = logging.ERROR,
        format_str: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        log_file: Optional[str] = None,
        console_log: bool = True
    ) -> None:
        """Настройка логирования для всех обработчиков исключений"""
        if cls._is_configured:
            # Удаляем старые handlers чтобы избежать дублирования
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
        
        # Создаем форматтер
        formatter = logging.Formatter(format_str)
        
        # Настройка корневого логгера
        root_logger = logging.getLogger()
        root_logger.setLevel(level)
        
        # Консольный handler
        if console_log:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)
        
        # Файловый handler
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        
        cls._default_logger = root_logger
        cls._is_configured = True
    
    def __init__(
        self,
        default_return: Any = None,
        log_error: bool = True,
        raise_original: bool = False,
        specific_exceptions: Tuple[Type[Exception], ...] = (Exception,),
        logger: Optional[logging.Logger] = None
    ):
        self.default_return = default_return
        self.log_error = log_error
        self.raise_original = raise_original
        self.specific_exceptions = specific_exceptions
        self.logger = logger or self._default_logger or logging.getLogger()
    
    def __call__(self, func: Callable) -> Callable:
        """Декоратор метода"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except self.specific_exceptions as e:
                if self.log_error and self.logger:
                    self.logger.error(
                        f"Ошибка в {func.__name__}: {e}", 
                        exc_info=True
                    )
                
                if self.raise_original:
                    raise e
                
                return self.default_return
        return wrapper