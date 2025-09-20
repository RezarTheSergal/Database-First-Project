import logging
from functools import wraps
from typing import Callable, Any, Optional, Tuple, Type

class ExceptionHandler:
    """Класс для обработки исключений с централизованной настройкой логирования"""
    
    # Статические настройки по умолчанию
    _default_logger = None

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