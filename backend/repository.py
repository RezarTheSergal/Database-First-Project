# Содержит функции или классы, которые реализуют все запросы к базе (чтение, запись, обновление, удаление).

from collections import defaultdict
import logging
from backend.utils.database_exception_handler import DatabaseErrorHandler
from backend.utils.exception_handler import ExceptionHandler
from backend.utils.responce_types import DatabaseResponse, ErrorCode, ResponseStatus
from backend.database.models import Base
from backend.database.database import Database
from sqlalchemy import Tuple, and_, asc, delete, desc, select, insert, update
from typing import Dict, List, Optional, Any

db_engine = Database().get_engine()
logger = logging.getLogger()

class DatabaseRepository:
    """Репозиторий для работы с базой данных"""
    
    @classmethod
    @DatabaseErrorHandler()
    def get_model_by_tablename(cls, table_name: str) -> DatabaseResponse:
        """Получение класса таблицы по её имени"""
        if table_name is None or not isinstance(table_name, str):
            return DatabaseResponse.error(
                ErrorCode.INVALID_PARAMETERS,
                "Некорректное имя таблицы"
            )
        
        for cls in Base.registry.mappers:
            if cls.class_.__tablename__ == table_name:
                logger.info(f"Таблица '{table_name}' успешно найдена")
                return DatabaseResponse.success(
                    data=cls.class_,
                    message=f"Модель для таблицы '{table_name}' найдена"
                )
        
        logger.warning(f"Таблица '{table_name}' не была найдена")
        return DatabaseResponse.error(
            ErrorCode.TABLE_NOT_FOUND,
            f"Таблица '{table_name}' не найдена"
        )
    
    @classmethod
    @DatabaseErrorHandler()
    def get_tablenames(cls) -> DatabaseResponse:
        """Получение списка имён таблиц"""
        try:
            tables = [cls.class_.__tablename__ for cls in Base.registry.mappers]
            return DatabaseResponse.success(
                data=tables,
                message=f"Найдено {len(tables)} таблиц"
            )
        except Exception as e:
            return DatabaseResponse.error(
                ErrorCode.OPERATION_FAILED,
                f"Ошибка при получении списка таблиц: {str(e)}"
            )
    
    @classmethod
    @DatabaseErrorHandler()
    def get_table_columns(cls, table_name: str) -> DatabaseResponse:
        """Получение названий полей и их типов в таблице"""
        model_response = cls.get_model_by_tablename(table_name)
        if model_response.status != ResponseStatus.SUCCESS:
            return model_response
        
        model = model_response.data
        columns_info = {}
        
        try:
            for column in model.__table__.columns:
                columns_info[column.key] = {
                    'type': str(column.type),
                    'nullable': column.nullable,
                    'primary_key': column.primary_key,
                    'foreign_keys': [str(fk) for fk in column.foreign_keys],
                    'default': str(column.default) if column.default else None
                }
            
            return DatabaseResponse.success(
                data=columns_info,
                message=f"Найдено {len(columns_info)} колонок в таблице '{table_name}'"
            )
            
        except Exception as e:
            return DatabaseResponse.error(
                ErrorCode.OPERATION_FAILED,
                f"Ошибка при получении колонок таблицы '{table_name}': {str(e)}"
            )
    
    @classmethod
    @DatabaseErrorHandler()
    def get_table_data(
        cls,
        table_name: str,
        columns_list: Optional[List[str]] = None,
        filters_dict: Optional[Dict[str, Any]] = None,
        order_by: Optional[Dict[str, str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> DatabaseResponse:
        """Получение данных из таблицы с фильтрами и сортировкой"""
        
        # Получаем модель
        model_response = cls.get_model_by_tablename(table_name)
        if model_response.status != ResponseStatus.SUCCESS:
            return model_response
        
        model = model_response.data
        
        # Получаем информацию о колонках
        columns_response = cls.get_table_columns(table_name)
        if columns_response.status != ResponseStatus.SUCCESS:
            return columns_response
        
        # Проверяем запрашиваемые колонки
        if columns_list:
            invalid_columns = set(columns_response).difference(columns_list)
            if invalid_columns:
                return DatabaseResponse.error(
                    ErrorCode.COLUMN_NOT_FOUND,
                    f"Колонки не найдены: {', '.join(invalid_columns)}",
                    error_details={"invalid_columns": list(invalid_columns)}
                )
            
            select_columns = [getattr(model, column) for column in columns_list]
        else:
            select_columns = [model]
        
        try:
            with Database().get_db_session() as session:
                query = select(*select_columns)
                
                # Применяем фильтры
                if filters_dict:
                    invalid_filter_columns = set(columns_response).difference(filters_dict.keys())
                    if invalid_filter_columns:
                        return DatabaseResponse.error(
                            ErrorCode.INVALID_FILTER,
                            f"Некорректные колонки в фильтре: {', '.join(invalid_filter_columns)}"
                        )
                    
                    filters = [getattr(model, key) == value for key, value in filters_dict.items()]
                    query = query.where(and_(*filters))
                
                # Применяем сортировку
                if order_by:
                    invalid_order_columns = set(columns_response).difference(order_by.keys())
                    if invalid_order_columns:
                        return DatabaseResponse.error(
                            ErrorCode.INVALID_ORDER_BY,
                            f"Некорректные колонки в сортировке: {', '.join(invalid_order_columns)}"
                        )
                    
                    order_criteria = []
                    for col_name, direction in order_by.items():
                        col = getattr(model, col_name)
                        if direction.lower() == "asc":
                            order_criteria.append(asc(col))
                        elif direction.lower() == "desc":
                            order_criteria.append(desc(col))
                        else:
                            return DatabaseResponse.error(
                                ErrorCode.INVALID_ORDER_BY,
                                f"Некорректное направление сортировки: {direction}. Используйте 'asc' или 'desc'"
                            )
                    
                    if order_criteria:
                        query = query.order_by(*order_criteria)
                
                # Применяем лимит и смещение
                if limit is not None:
                    query = query.limit(limit)
                if offset is not None:
                    query = query.offset(offset)
                
                result = session.execute(query)
                
                if columns_list:
                    data = [dict(zip(columns_list, row)) for row in result.all()]
                else:
                    # Преобразуем ORM объекты в словари
                    data = []
                    for obj in result.scalars().all():
                        obj_dict = {column.key: getattr(obj, column.key) 
                                  for column in obj.__table__.columns}
                        data.append(obj_dict)
                
                return DatabaseResponse.success(
                    data=data,
                    message=f"Получено {len(data)} записей из таблицы '{table_name}'"
                )
                
        except Exception as e:
            return DatabaseErrorHandler.handle_exception(e, f"get_table_data for {table_name}")
    
    @classmethod
    @DatabaseErrorHandler()
    def insert_into_table(cls, table_name: str, params: Dict[str, Any]) -> DatabaseResponse:
        """Вставка значений в таблицу"""
        
        # Получаем модель
        model_response = cls.get_model_by_tablename(table_name)
        if model_response.status != ResponseStatus.SUCCESS:
            return model_response
        
        model = model_response.data
        
        # Получаем информацию о колонках
        columns_response = cls.get_table_columns(table_name)
        if columns_response.status != ResponseStatus.SUCCESS:
            return columns_response
        
        available_columns = set(columns_response.data.keys())
        
        # Фильтруем параметры
        valid_params = {}
        invalid_params = []
        
        for key, value in params.items():
            if key in available_columns:
                valid_params[key] = value
            else:
                invalid_params.append(key)
        
        if not valid_params:
            return DatabaseResponse.error(
                ErrorCode.INVALID_PARAMETERS,
                "Не предоставлено ни одного корректного параметра",
                error_details={"invalid_parameters": invalid_params}
            )
        
        if invalid_params:
            logger.warning(f"Игнорируем некорректные параметры: {invalid_params}")
        
        try:
            with Database().get_db_session() as session:
                query = insert(model).values(valid_params)
                result = session.execute(query)
                session.commit()
                
                response_data = {
                    "inserted_data": valid_params,
                    "ignored_parameters": invalid_params if invalid_params else None
                }
                
                return DatabaseResponse.success(
                    data=response_data,
                    message=f"Запись успешно добавлена в таблицу '{table_name}'",
                    affected_rows=result.rowcount
                )
                
        except Exception as e:
            return DatabaseErrorHandler.handle_exception(e, f"insert_into_table for {table_name}")
    
    @classmethod
    @DatabaseErrorHandler()
    def update_table_data(
        cls, 
        table_name: str, 
        update_params: Dict[str, Any], 
        filters_dict: Dict[str, Any]
    ) -> DatabaseResponse:
        """Обновление данных в таблице"""
        
        # Получаем модель
        model_response = cls.get_model_by_tablename(table_name)
        if model_response.status != ResponseStatus.SUCCESS:
            return model_response
        
        model = model_response.data
        
        # Получаем информацию о колонках
        columns_response = cls.get_table_columns(table_name)
        if columns_response.status != ResponseStatus.SUCCESS:
            return columns_response
        
        available_columns = set(columns_response.data.keys())
        
        # Проверяем параметры обновления
        invalid_update_params = set(update_params.keys()) - available_columns
        if invalid_update_params:
            return DatabaseResponse.error(
                ErrorCode.COLUMN_NOT_FOUND,
                f"Некорректные колонки для обновления: {', '.join(invalid_update_params)}"
            )
        
        # Проверяем фильтры
        invalid_filter_params = set(filters_dict.keys()) - available_columns
        if invalid_filter_params:
            return DatabaseResponse.error(
                ErrorCode.INVALID_FILTER,
                f"Некорректные колонки в фильтре: {', '.join(invalid_filter_params)}"
            )
        
        try:
            with Database().get_db_session() as session:
                filters = [getattr(model, key) == value for key, value in filters_dict.items()]
                query = update(model).where(and_(*filters)).values(update_params)
                result = session.execute(query)
                session.commit()
                
                return DatabaseResponse.success(
                    data={
                        "updated_data": update_params,
                        "filters": filters_dict
                    },
                    message=f"Обновлено записей: {result.rowcount}",
                    affected_rows=result.rowcount
                )
                
        except Exception as e:
            return DatabaseErrorHandler.handle_exception(e, f"update_table_data for {table_name}")
    
    @classmethod
    @DatabaseErrorHandler()
    def delete_from_table(cls, table_name: str, filters_dict: Dict[str, Any]) -> DatabaseResponse:
        """Удаление данных из таблицы"""
        
        # Получаем модель
        model_response = cls.get_model_by_tablename(table_name)
        if model_response.status != ResponseStatus.SUCCESS:
            return model_response
        
        model = model_response.data
        
        # Получаем информацию о колонках
        columns_response = cls.get_table_columns(table_name)
        if columns_response.status != ResponseStatus.SUCCESS:
            return columns_response
        
        available_columns = set(columns_response.data.keys())
        
        # Проверяем фильтры
        invalid_filter_params = set(filters_dict.keys()) - available_columns
        if invalid_filter_params:
            return DatabaseResponse.error(
                ErrorCode.INVALID_FILTER,
                f"Некорректные колонки в фильтре: {', '.join(invalid_filter_params)}"
            )
        
        if not filters_dict:
            return DatabaseResponse.error(
                ErrorCode.INVALID_PARAMETERS,
                "Фильтры обязательны для операции удаления (безопасность)"
            )
        
        try:
            with Database().get_db_session() as session:
                filters = [getattr(model, key) == value for key, value in filters_dict.items()]
                query = delete(model).where(and_(*filters))
                result = session.execute(query)
                session.commit()
                
                return DatabaseResponse.success(
                    data={"filters": filters_dict},
                    message=f"Удалено записей: {result.rowcount}",
                    affected_rows=result.rowcount
                )
                
        except Exception as e:
            return DatabaseErrorHandler.handle_exception(e, f"delete_from_table for {table_name}")
