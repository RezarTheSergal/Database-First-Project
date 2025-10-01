from typing import List, Dict, Any
from backend.repository import DatabaseRepository
from backend.utils.responce_types import ResponseStatus


class ForeignKeySearchService:
    """Сервис для поиска значений по внешним ключам. Отделен от UI-логики."""

    def search(
        self, table: str, display_col: str, id_col: str, query: str, limit: int = 30
    ) -> List[Dict[str, Any]]:
        """Выполняет поиск по внешнему ключу в указанной таблице."""
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

    def get_display_value(
        self, table: str, display_col: str, id_col: str, id_value: Any
    ) -> str:
        """Получает отображаемое значение по ID."""
        repo = DatabaseRepository()
        response = repo.get_table_data(
            table_name=table,
            columns_list=[id_col, display_col],
            filters_dict={
                id_col: id_value
            },  # TODO: Переименовать в where (для Rezar от Вовы)
            limit=1,
        )

        if response.status == ResponseStatus.SUCCESS and response.data:
            return str(response.data[0].get(display_col, id_value))
        return str(id_value)
