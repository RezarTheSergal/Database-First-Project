# Содержит функции или классы, которые реализуют все запросы к базе (чтение, запись, обновление, удаление).

from collections import defaultdict
from backend.utils.exception_handler import ExceptionHandler
from database.models import Base
from database.database import Database
from sqlalchemy import Tuple, and_, asc, desc, select
from typing import Dict, List, Optional, Any


@ExceptionHandler()
def get_model_by_tablename(table_name: str) -> Base | None:
    """
    Получение класса таблицы по её имени
    """
    for cls in Base.registry.mappers:
        if cls.class_.__tablename__ == table_name:
            return cls.class_  # type: ignore
    return None


@ExceptionHandler()
def get_tablenames() -> List[str]:
    """
    Получение списка имён таблиц
    """
    return [cls.class_.__tablename__ for cls in Base.registry.mappers]


@ExceptionHandler()
def get_table_columns(table_name: str) -> Dict[str, type]:
    """
    Даёт возможность получать названия полей в таблице
    """
    result: Dict[str, type] = defaultdict()
    model = get_model_by_tablename(table_name)
    for column in model.__table__.columns:
        result[column.key] = column.type

    return result


@ExceptionHandler()
def get_table_data(
    table_name: str,
    columns_list: Optional[List] = [],
    filters_dict: Optional[Dict[str, Any]] = None,
    order_by: Optional[Dict[str, str]] = None,
) -> Tuple:
    """
    Получение данных из таблицы по столбцам с фильтрами, сортировками
    """
    model = get_model_by_tablename(table_name)

    columns_intersected = set([key for key in get_table_columns(table_name).keys()]).intersection(columns_list)  # type: ignore

    if columns_intersected:
        select_columns = [getattr(model, column) for column in columns_intersected]
    else:
        select_columns = [model]

    query = select(*select_columns)

    if filters_dict is not None:
        filters = [getattr(model, key) == value for key, value in filters_dict.items()]
        query = select(model).where(and_(*filters))

    if order_by:
        order_criteria = []
        for col_name, direction in order_by.items():
            col = getattr(model, col_name)
            if direction.lower() == "asc":
                order_criteria.append(asc(col))
            elif direction.lower() == "desc":
                order_criteria.append(desc(col))
        if order_criteria:
            query = query.order_by(*order_criteria)

    with Database().get_db_session() as session:
        result = session.execute(query)
        if columns_intersected:
            return result.all()  # кортежи значений выбранных колонок
        else:
            return result.scalars().all()  # ORM-объекты модели
