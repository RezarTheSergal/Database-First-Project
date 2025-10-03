from typing import List, Dict, Any
from backend.repository import DatabaseRepository
from backend.utils.responce_types import ResponseStatus
from frontend.shared.utils.DatabaseMiddleware import DatabaseMiddleware


class DataValidator:
    """Сервис для проверки валидности данных"""

    @staticmethod
    def is_valid_integer(value: Any, min_val: int, max_val: int) -> bool:
        if value is None:
            return False
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (TypeError, ValueError):
            return False

    @staticmethod
    def is_valid_float(value: Any, min_val: float, max_val: float) -> bool:
        if value is None:
            return False
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (TypeError, ValueError):
            return False
