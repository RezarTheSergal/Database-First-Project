from sqlalchemy.orm import DeclarativeBase
from backend.utils.responce_types import ResponseStatus
from frontend.shared.utils.DatabaseMiddleware import DatabaseMiddleware


def set_model(table, model_class: type[DeclarativeBase]):
    """Устанавливает модель SQLAlchemy и настраивает колонки"""
    table._model_class = model_class
    table_name = model_class.__tablename__

    # Получаем метаданные колонок
    col_resp = DatabaseMiddleware.get_columns_by_table_name(table_name)
    if not col_resp or col_resp.status != ResponseStatus.SUCCESS:
        raise ValueError(
            f"Не удалось загрузить колонки для {table_name}: {col_resp}"
        )

    table._column_info = col_resp.data
    table._setup_columns()
    table._preload_foreign_key_data()
