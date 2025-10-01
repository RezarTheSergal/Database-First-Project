from typing import List, Dict, Any
from backend.repository import DatabaseRepository
from backend.utils.responce_types import ResponseStatus


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

    @staticmethod
    def get_foreign_key_display(
        table: str, display_col: str, id_col: str, id_value: Any
    ) -> str:
        """Получает отображаемое значение по ID для внешнего ключа"""
        repo = DatabaseRepository()
        response = repo.get_table_data(
            table_name=table,
            columns_list=[id_col, display_col],
            filters_dict={id_col: id_value},
            limit=1,
        )

        if response.status == ResponseStatus.SUCCESS and response.data:
            return str(response.data[0].get(display_col, id_value))
        return str(id_value)

    @staticmethod
    def search_foreign_keys(
        table: str, display_col: str, id_col: str, query: str, limit: int = 30
    ) -> List[Dict[str, Any]]:
        """Выполняет поиск по внешнему ключу"""
        repo = DatabaseRepository()
        response = repo.search_foreign_key(
            table=table,
            display_col=display_col,
            id_col=id_col,
            query=query,
            limit=limit,
        )

        if response.status == ResponseStatus.SUCCESS and response.data:
            return response.data
        else:
            raise Exception(f"Search failed: {response.error}")
