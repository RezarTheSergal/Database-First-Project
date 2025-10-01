from backend.repository import DatabaseRepository
from backend.utils.responce_types import ResponseStatus


def populate_with_suggestions(foreign_key_search_box):
    if foreign_key_search_box.count() == 0:
        resp = DatabaseRepository.search_foreign_key(
            table=foreign_key_search_box.target_table,
            display_col=foreign_key_search_box.display_column,
            id_col=foreign_key_search_box.id_column,
            query="",  # пустой запрос → можно вернуть первые N
            limit=10,
        )
        if resp.status == ResponseStatus.SUCCESS and resp.data is not None:
            for item in resp.data:
                foreign_key_search_box.addItem(str(item["display"]), userData=item["id"])