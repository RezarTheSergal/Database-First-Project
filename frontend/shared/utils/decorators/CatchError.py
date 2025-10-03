# Define generic types
from functools import wraps
from typing import ParamSpec,TypeVar,Callable
from backend.utils.logger import logging

P = ParamSpec("P")  # Represents the parameters of the decorated function
R = TypeVar("R")  # Represents the return type of the decorated function


def CatchError(func: Callable[P, R], logger: None | logging.Logger = None) -> Callable[P, R | None]:
    """Decorator that catches exceptions and logs them, preserving type signatures"""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            message: str = f"Error in {func.__name__}: {e}"
            if logger:
                logger.error(message)
            else:
                print(message)
            return None

    return wrapper
