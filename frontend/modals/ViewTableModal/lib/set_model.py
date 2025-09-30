from sqlalchemy.orm import DeclarativeBase
from backend.repository import DatabaseRepository
from backend.utils.responce_types import ResponseStatus


def set_model(table, model_class: type[DeclarativeBase]):
    """Устанавливает модель SQLAlchemy и настраивает колонки"""
    table._model_class = model_class
    table_name = model_class.__tablename__

    # Получаем метаданные колонок
    repo = DatabaseRepository()
    col_resp = repo.get_table_columns(table_name)
    if col_resp.status != ResponseStatus.SUCCESS:
        raise ValueError(
            f"Не удалось загрузить колонки для {table_name}: {col_resp.message}"
        )

    table._column_info = col_resp.data
    table._setup_columns()
    table._preload_foreign_key_data()
