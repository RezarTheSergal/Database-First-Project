from backend.repository import DatabaseRepository


def fetch_suggestions(foreign_key_search_box):
    text = foreign_key_search_box.currentText().strip()
    if len(text) < 2:
        return

    # Асинхронный запрос (в реальности — через QThread или async)
    results = DatabaseRepository().search_foreign_key(
        table=foreign_key_search_box.target_table,
        display_col=foreign_key_search_box.display_column,
        id_col=foreign_key_search_box.id_column,
        query=text,
        limit=30,
    )
    if results.data:
        foreign_key_search_box.blockSignals(True)
        foreign_key_search_box.clear()
        for item in results.data:
            foreign_key_search_box.addItem(
                item[foreign_key_search_box.display_column],
                item[foreign_key_search_box.id_column],
            )
        foreign_key_search_box.blockSignals(False)
