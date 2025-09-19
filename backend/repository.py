# Содержит функции или классы, которые реализуют все запросы к базе (чтение, запись, обновление, удаление).

from database.models import Base
from database.database import Database
from sqlalchemy import select
from typing import Dict, List
def get_model_by_tablename(table_name: str) -> Base | None:
    """
    Получение класса таблицы по её имени
    """
    for cls in Base.registry.mappers:
        if cls.class_.__tablename__ == table_name:
            return cls.class_
    return None

def get_table_fields(table_name: str) -> Dict[str: type]:
    """
    Даёт возможность получать данные о полях в таблице
    """
    result: Dict[str: type]
    model = get_model_by_tablename(table_name)
    for column in model.__table__.columns:
        result[column.key] = column.type

    return result


def get_table_data(table_name: str, *args: str) -> List[str]:
    """
    Получение данных из таблицы по фильтрам
    """
    result: List[str]
    model = get_model_by_tablename(table_name)
    with Database().get_db_session() as session:
        raise NotImplementedError

            
        