import logging
from functools import wraps
import time
from typing import Callable, Any, Optional, ParamSpec, Tuple, Type, TypeVar

P = ParamSpec('P')
T = TypeVar('T')

class ExceptionHandler:
    """Класс для обработки исключений с централизованной настройкой логирования"""
    
    # Статические настройки по умолчанию
    _default_logger = None

    def __init__(
        self,
        default_return: Any = None,
        log_error: bool = True,
        raise_original: bool = False,
        max_retries: int = 1,
        retry_after: float = 0.5, # Секунды
        logger: Optional[logging.Logger] = None
    ):
        self.default_return = default_return
        self.log_error = log_error
        self.raise_original = raise_original
        self.max_retries = max_retries
        self.retry_after = retry_after
        self.logger = logger or self._default_logger or logging.getLogger()
    
    def __call__(self, func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for i in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if self.log_error and self.logger:
                        self.logger.error(
                            f"Ошибка в {func.__name__}: {e}, Поытка номер: {i+1}/{self.max_retries}", 
                            exc_info=True
                        )
                    
                    if self.max_retries > i:
                        time.sleep(self.retry_after)
                        continue

                    if self.raise_original:
                        raise e
                    
                    return self.default_return
                return func(*args, **kwargs)
        return wrapper