from backend.utils.responce_types import ResponseStatus
from frontend.shared.utils import DatabaseMiddleware


def populate_with_suggestions(foreign_key_search_box):
    if foreign_key_search_box.count() == 0:
        resp = DatabaseMiddleware.search_all(
            foreign_key_search_box.target_table,
            foreign_key_search_box.display_column,
            foreign_key_search_box.id_column,
        )

        if resp and resp.status == ResponseStatus.SUCCESS and resp.data:
            for item in resp.data:
                foreign_key_search_box.addItem(
                    str(item["display"]), userData=item["id"]
                )
