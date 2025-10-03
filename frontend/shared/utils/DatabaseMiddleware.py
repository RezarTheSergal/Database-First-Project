from typing import Any, Dict, List
from backend.repository import DatabaseResponse, DatabaseRepository
from backend.utils.logger import logging
from backend.utils.responce_types import ResponseStatus
from .decorators.CatchError import CatchError

repo = DatabaseRepository()
logger = logging.getLogger("database-middleware")


class DatabaseMiddleware:

    @staticmethod
    @CatchError
    def get_table_names() -> DatabaseResponse:
        return repo.get_tablenames()


    @staticmethod
    @CatchError
    def get_columns_by_table_name(table_name: str) -> DatabaseResponse:
        return repo.get_table_columns(table_name)

    @staticmethod
    @CatchError
    def search(
        query: str,
        target_table: str,
        display_column: str,
        id_column: str,
        limit: int = 30,
    ) -> DatabaseResponse:
        return repo.search_foreign_key(
            table=target_table,
            display_col=display_column,
            id_col=id_column,
            query=query,
            limit=limit,
        )

    @staticmethod
    @CatchError
    def search_all(
        target_table: str, display_column: str, id_column: str, limit: int = 10
    ) -> DatabaseResponse:
        return repo.search_foreign_key(
            table=target_table,
            display_col=display_column,
            id_col=id_column,
            query="",
            limit=limit,
        )

    @staticmethod
    @CatchError
    def search_single(
        target_table: str, display_column: str, id_column: str, value_id: str
    ) -> DatabaseResponse:
        return repo.get_table_data(
            table_name=target_table,
            columns_list=[id_column, display_column],
            filters_dict={id_column: value_id},
            limit=1,
        )

    @staticmethod
    @CatchError
    def get_foreign_key_batch(
        target_table: str, target_col: str, display_col: str, limit: int = 100
    ) -> DatabaseResponse:
        return repo.get_table_data(
            table_name=target_table,
            columns_list=(
                [target_col, display_col] if display_col != target_col else [target_col]
            ),
            limit=limit,
        )

    @staticmethod
    @CatchError
    def put_data(table_name: str, data: Any) -> DatabaseResponse:
        return repo.insert_into_table(table_name, data)

    @staticmethod
    @CatchError
    def get_table_schema(table_name: str) -> DatabaseResponse:
        return repo.get_model_by_tablename(table_name)

    @staticmethod
    @CatchError
    def get_all(table_name: str) -> DatabaseResponse:
        return repo.get_table_data(table_name)

    @staticmethod
    @CatchError
    def get_where(table_name: str, filters = {}) -> DatabaseResponse:
        table_columns = DatabaseMiddleware.get_columns_by_table_name(table_name)
        return repo.get_table_data(
            table_name, table_columns, filters.get(table_name, "")
        )


    @staticmethod
    def get_foreign_key_display(
        table_name: str, display_col: str, id_col: str, id_value: Any
    ) -> str:
        """Получает отображаемое значение по ID для внешнего ключа"""
        response = repo.get_table_data(
            table_name=table_name,
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

    @staticmethod
    def get_display_value_by_id(table_name:str,id_col:str,display_col:str,id_value:Any):
        return repo.get_table_data(
            table_name=table_name,
            columns_list=[id_col, display_col],
            filters_dict={
                id_col: id_value
            },  # TODO: Переименовать в where (для Rezar от Вовы)
            limit=1,
        )