# Содержит функции или классы, которые реализуют все запросы к базе (чтение, запись, обновление, удаление).
from datetime import datetime, date
from collections import defaultdict
import logging
from backend.utils.database_exception_handler import DatabaseErrorHandler
from backend.utils.exception_handler import ExceptionHandler
from backend.utils.responce_types import DatabaseResponse, ErrorCode, ResponseStatus
from backend.database.models import Base
from backend.database.database import Database
from sqlalchemy import (
    CheckConstraint, TextClause, Tuple, and_, asc, delete, desc, 
    select, insert, update, text
)
from typing import Dict, List, Optional, Any
from sqlalchemy import Enum as SQLEnum

db_engine = Database().get_engine()
logger = logging.getLogger()


class DatabaseRepository:
    """Репозиторий для работы с базой данных"""
    
    # Кэш для метаданных таблиц
    _columns_cache: Dict[str, Dict[str, Any]] = {}
    _cache_enabled: bool = True

    @classmethod
    @DatabaseErrorHandler()
    def get_model_by_tablename(cls, table_name: str) -> DatabaseResponse:
        """Получение класса таблицы по её имени"""
        if table_name is None or not isinstance(table_name, str):
            return DatabaseResponse.error(
                ErrorCode.INVALID_PARAMETERS,
                "Некорректное имя таблицы"
            )

        for mapper in Base.registry.mappers:
            if mapper.class_.__tablename__ == table_name:
                logger.info(f"Таблица '{table_name}' успешно найдена")
                return DatabaseResponse.success(
                    data=mapper.class_,
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
            tables = [mapper.class_.__tablename__ for mapper in Base.registry.mappers]
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
    def get_table_columns(cls, table_name: str, use_cache: bool = True) -> DatabaseResponse:
        """Получение полной информации о колонках таблицы, включая типы, внешние ключи, enum-значения и ограничения."""
        
        # Проверяем кэш
        if use_cache and cls._cache_enabled and table_name in cls._columns_cache:
            return DatabaseResponse.success(
                data=cls._columns_cache[table_name],
                message=f"Найдено {len(cls._columns_cache[table_name])} колонок в таблице '{table_name}' (из кэша)"
            )
        
        model_response = cls.get_model_by_tablename(table_name)
        if model_response.status != ResponseStatus.SUCCESS:
            return model_response

        model = model_response.data
        columns_info: Dict[str, Dict[str, Any]] = {}

        try:
            # Собираем check constraints на уровне таблицы
            table_check_constraints: Dict[str, List[str]] = {}
            for constraint in model.__table__.constraints:
                if isinstance(constraint, CheckConstraint):
                    sql_text = str(constraint.sqltext) if isinstance(constraint.sqltext, TextClause) else str(constraint.sqltext.compile())
                    for col in model.__table__.columns:
                        if col.name in sql_text:
                            table_check_constraints.setdefault(col.name, []).append(sql_text)

            for column in model.__table__.columns:
                col_info = {
                    'name': column.name,
                    'type': str(column.type),
                    'nullable': column.nullable,
                    'primary_key': column.primary_key,
                    'default': None,
                    'foreign_keys': [],
                    'check_constraints': table_check_constraints.get(column.name, []),
                    'enum_values': None
                }

                # Обработка default
                if column.default is not None:
                    if hasattr(column.default, 'arg'):
                        col_info['default'] = str(column.default.arg)
                    else:
                        col_info['default'] = str(column.default)

                # Обработка foreign keys
                for fk in column.foreign_keys:
                    col_info['foreign_keys'].append({
                        'target_table': fk.column.table.name,
                        'target_column': fk.column.name
                    })

                # Обработка Enum
                if isinstance(column.type, SQLEnum):
                    if hasattr(column.type, 'enums') and column.type.enums:
                        col_info['enum_values'] = list(column.type.enums)

                columns_info[column.name] = col_info

            # Сохраняем в кэш
            if cls._cache_enabled:
                cls._columns_cache[table_name] = columns_info

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
        offset: Optional[int] = None,
        join_config: Optional[List[Dict[str, Any]]] = None
    ) -> DatabaseResponse:
        """
        Получение данных из таблицы с расширенными фильтрами
        
        Новый формат filters_dict:
        {
            "column_name": value,                    # простое равенство
            "column_name__gt": value,               # больше чем
            "column_name__lt": value,               # меньше чем
            "column_name__gte": value,              # больше или равно
            "column_name__lte": value,              # меньше или равно
            "column_name__like": value,             # LIKE '%value%'
            "column_name__ilike": value,            # ILIKE '%value%' (регистронезависимо)
            "column_name__in": [value1, value2],    # IN списка
            "column_name__between": [min, max],     # BETWEEN
            "column_name__is_null": True/False,     # IS NULL / IS NOT NULL
            "column_name__neq": value,              # не равно
        }
        """

        # Получаем основную модель
        model_response = cls.get_model_by_tablename(table_name)
        if model_response.status != ResponseStatus.SUCCESS:
            return model_response

        main_model = model_response.data

        try:
            with Database().get_db_session() as session:
                # Базовый запрос
                joined_models = {table_name: main_model}
                
                if columns_list:
                    # Используем колонки моделей вместо text()
                    select_columns = []
                    
                    for col_spec in columns_list:
                        if '.' in col_spec:
                            table_part, column_part = col_spec.split('.', 1)
                            if table_part in joined_models:
                                model_obj = joined_models[table_part]
                                if hasattr(model_obj, column_part):
                                    select_columns.append(getattr(model_obj, column_part).label(col_spec))
                        else:
                            if hasattr(main_model, col_spec):
                                select_columns.append(getattr(main_model, col_spec))
                    
                    if not select_columns:
                        return DatabaseResponse.error(
                            ErrorCode.COLUMN_NOT_FOUND,
                            "Ни одна из указанных колонок не найдена"
                        )
                    
                    query = select(*select_columns)
                else:
                    query = select(main_model)

                # Применяем JOIN
                if join_config:
                    for join_item in join_config:
                        join_table_name = join_item["table"]
                        join_type = join_item.get("type", "inner").lower()
                        join_on = join_item["on"]
                        
                        join_model_response = cls.get_model_by_tablename(join_table_name)
                        if join_model_response.status != ResponseStatus.SUCCESS:
                            return join_model_response
                        
                        join_model = join_model_response.data
                        joined_models[join_table_name] = join_model
                        
                        # Построение условия JOIN
                        if isinstance(join_on, dict) and "condition" in join_on:
                            logger.warning(f"Используется raw SQL условие для JOIN: {join_on['condition']}")
                            join_condition = text(join_on["condition"])
                        else:
                            join_conditions = []
                            for main_col, join_col in join_on.items():
                                if '.' not in main_col:
                                    main_col = f"{table_name}.{main_col}"
                                if '.' not in join_col:
                                    join_col = f"{join_table_name}.{join_col}"
                                
                                main_table, main_col_name = main_col.split('.')
                                join_table, join_col_name = join_col.split('.')
                                
                                if main_table in joined_models and join_table in joined_models:
                                    main_col_obj = getattr(joined_models[main_table], main_col_name)
                                    join_col_obj = getattr(joined_models[join_table], join_col_name)
                                    join_conditions.append(main_col_obj == join_col_obj)
                            
                            if not join_conditions:
                                return DatabaseResponse.error(
                                    ErrorCode.INVALID_JOIN_CONDITION,
                                    "Неверное условие JOIN"
                                )
                            
                            join_condition = and_(*join_conditions)
                        
                        # Применяем JOIN
                        if join_type == "left":
                            query = query.join(join_model, join_condition, isouter=True)
                        elif join_type == "right":
                            # RIGHT JOIN реализуется через изменение порядка таблиц
                            logger.warning("RIGHT JOIN конвертирован в LEFT JOIN с изменением порядка таблиц")
                            query = query.join(join_model, join_condition, isouter=True)
                        elif join_type == "full":
                            query = query.outerjoin(join_model, join_condition, full=True)
                        else:  # inner
                            query = query.join(join_model, join_condition)

                # Применяем расширенные фильтры
                if filters_dict:
                    filter_conditions = cls._build_filter_conditions(
                        filters_dict, joined_models, table_name
                    )
                    
                    if filter_conditions.status != ResponseStatus.SUCCESS:
                        return filter_conditions
                    
                    if filter_conditions.data:
                        query = query.where(and_(*filter_conditions.data))

                # Применяем сортировку
                if order_by:
                    order_conditions = []
                    
                    for order_col, order_dir in order_by.items():
                        col_obj = None
                        
                        if '.' in order_col:
                            table_part, column_part = order_col.split('.', 1)
                            if table_part in joined_models:
                                table_model = joined_models[table_part]
                                if hasattr(table_model, column_part):
                                    col_obj = getattr(table_model, column_part)
                        else:
                            if hasattr(main_model, order_col):
                                col_obj = getattr(main_model, order_col)
                        
                        if col_obj is not None:
                            if order_dir.lower() == "desc":
                                order_conditions.append(desc(col_obj))
                            else:
                                order_conditions.append(asc(col_obj))
                    
                    if order_conditions:
                        query = query.order_by(*order_conditions)

                # Применяем лимит и смещение
                if limit is not None:
                    query = query.limit(limit)
                if offset is not None:
                    query = query.offset(offset)

                # Выполняем запрос
                result = session.execute(query)
                
                if columns_list:
                    rows = result.fetchall()
                    data = []
                    for row in rows:
                        row_dict = {}
                        for i, col_name in enumerate(columns_list):
                            # Обработка различных типов данных
                            value = row[i]
                            if isinstance(value, (datetime, date)):
                                value = value.isoformat()
                            row_dict[col_name] = value
                        data.append(row_dict)
                else:
                    data = []
                    for obj in result.scalars().all():
                        obj_dict = {}
                        for column in obj.__table__.columns:
                            value = getattr(obj, column.key)
                            # Обработка различных типов данных
                            if isinstance(value, (datetime, date)):
                                value = value.isoformat()
                            obj_dict[column.key] = value
                        data.append(obj_dict)

                return DatabaseResponse.success(
                    data=data,
                    message=f"Получено {len(data)} записей"
                )

        except Exception as e:
            logger.error(f"Ошибка в get_table_data: {str(e)}")
            return DatabaseErrorHandler.handle_exception(e, f"get_table_data with extended filters for {table_name}")

    @classmethod
    def _build_filter_conditions(
        cls, 
        filters_dict: Dict[str, Any], 
        joined_models: Dict[str, Any], 
        main_table: str
    ) -> DatabaseResponse:
        """Построение условий фильтрации с поддержкой расширенных операторов"""
        
        conditions = []
        main_model = joined_models[main_table]
        
        for filter_key, filter_value in filters_dict.items():
            # Парсим имя колонки и оператор
            parts = filter_key.split('__')
            column_name = parts[0]
            operator = 'eq' if len(parts) == 1 else parts[1]
            
            # Определяем таблицу и модель
            if '.' in column_name:
                table_part, column_part = column_name.split('.', 1)
                if table_part not in joined_models:
                    return DatabaseResponse.error(
                        ErrorCode.INVALID_FILTER,
                        f"Таблица '{table_part}' не найдена в JOIN"
                    )
                table_model = joined_models[table_part]
                column_name = column_part
                table_name = table_part
            else:
                table_model = main_model
                table_name = main_table
            
            # Проверяем существование колонки
            if not hasattr(table_model, column_name):
                return DatabaseResponse.error(
                    ErrorCode.COLUMN_NOT_FOUND,
                    f"Колонка '{column_name}' не найдена в таблице '{table_name}'"
                )
            
            col_obj = getattr(table_model, column_name)
            
            # Получаем информацию о типе колонки для валидации
            col_info_response = cls._get_column_info(table_name, column_name)
            if col_info_response.status == ResponseStatus.SUCCESS:
                col_info = col_info_response.data
            else:
                col_info = None
            
            # Валидируем значение в зависимости от типа
            validation_result = cls._validate_filter_value(filter_value, operator, col_info)
            if validation_result.status != ResponseStatus.SUCCESS:
                return validation_result
            
            validated_value = validation_result.data
            
            # Строим условие в зависимости от оператора
            condition = cls._build_condition_for_operator(col_obj, operator, validated_value)
            if condition is not None:
                conditions.append(condition)
            else:
                return DatabaseResponse.error(
                    ErrorCode.INVALID_FILTER,
                    f"Неподдерживаемый оператор: {operator}"
                )
        
        return DatabaseResponse.success(data=conditions)

    @classmethod
    def _build_condition_for_operator(cls, column, operator: str, value: Any):
        """Создает SQL условие для конкретного оператора"""
        
        operators = {
            'eq': lambda: column == value,
            'neq': lambda: column != value,
            'gt': lambda: column > value,
            'gte': lambda: column >= value,
            'lt': lambda: column < value,
            'lte': lambda: column <= value,
            'like': lambda: column.like(f"%{value}%"),
            'ilike': lambda: column.ilike(f"%{value}%"),
            'startswith': lambda: column.like(f"{value}%"),
            'endswith': lambda: column.like(f"%{value}"),
            'in': lambda: column.in_(value) if value else column.in_([]),  # Пустой список = всегда False
            'not_in': lambda: ~column.in_(value) if value else column.is_not(None),
            'between': lambda: column.between(value[0], value[1]),
            'is_null': lambda: column.is_(None) if value else column.isnot(None),
        }
        
        if operator in operators:
            try:
                return operators[operator]()
            except Exception as e:
                logger.error(f"Ошибка при построении условия для оператора '{operator}': {str(e)}")
                return None
        return None

    @classmethod
    def _validate_filter_value(cls, value: Any, operator: str, col_info: Optional[Dict] = None) -> DatabaseResponse:
        """Валидация значений фильтров в зависимости от типа данных"""
        
        # Валидация для оператора IN
        if operator in ('in', 'not_in'):
            if not isinstance(value, (list, tuple)):
                return DatabaseResponse.error(
                    ErrorCode.INVALID_FILTER,
                    f"Оператор '{operator}' требует список значений, получен: {type(value).__name__}"
                )
        
        # Валидация для оператора BETWEEN
        if operator == 'between':
            if not isinstance(value, (list, tuple)) or len(value) != 2:
                return DatabaseResponse.error(
                    ErrorCode.INVALID_FILTER,
                    "Оператор 'between' требует список из двух значений [min, max]"
                )
            if value[0] is None or value[1] is None:
                return DatabaseResponse.error(
                    ErrorCode.INVALID_FILTER,
                    "Оператор 'between' не поддерживает None значения"
                )
        
        # Валидация для оператора IS_NULL
        if operator == 'is_null' and not isinstance(value, bool):
            return DatabaseResponse.error(
                ErrorCode.INVALID_FILTER,
                "Оператор 'is_null' требует булево значение"
            )
        
        # Валидация типов данных если есть информация о колонке
        if col_info and value is not None and operator not in ['is_null']:
            col_type = col_info['type'].lower()
            
            # Валидация числовых типов
            if any(num_type in col_type for num_type in ['int', 'numeric', 'decimal', 'float']):
                if operator in ['gt', 'gte', 'lt', 'lte', 'between', 'in']:
                    try:
                        if operator == 'between':
                            return DatabaseResponse.success(data=[float(value[0]), float(value[1])])
                        elif operator in ('in', 'not_in'):
                            return DatabaseResponse.success(data=[float(x) for x in value])
                        else:
                            return DatabaseResponse.success(data=float(value))
                    except (ValueError, TypeError) as e:
                        return DatabaseResponse.error(
                            ErrorCode.INVALID_FILTER,
                            f"Для числовой колонки ожидается число, получено: {value}"
                        )
            
            # Валидация дат
            elif any(date_type in col_type for date_type in ['date', 'timestamp', 'datetime']):
                if operator in ['gt', 'gte', 'lt', 'lte', 'between', 'in']:
                    try:
                        if operator == 'between':
                            dates = [
                                cls._parse_date(value[0]),
                                cls._parse_date(value[1])
                            ]
                            return DatabaseResponse.success(data=dates)
                        elif operator in ('in', 'not_in'):
                            dates = [cls._parse_date(x) for x in value]
                            return DatabaseResponse.success(data=dates)
                        else:
                            return DatabaseResponse.success(data=cls._parse_date(value))
                    except ValueError as e:
                        return DatabaseResponse.error(
                            ErrorCode.INVALID_FILTER,
                            f"Неверный формат даты: {str(e)}"
                        )
            
            # Валидация ENUM
            elif col_info.get('enum_values') and operator not in ['like', 'ilike']:
                enum_values = col_info['enum_values']
                if operator in ('in', 'not_in'):
                    invalid_values = [v for v in value if v not in enum_values]
                else:
                    invalid_values = [value] if value not in enum_values else []
                
                if invalid_values:
                    return DatabaseResponse.error(
                        ErrorCode.INVALID_FILTER,
                        f"Недопустимые значения для ENUM колонки: {invalid_values}. Допустимо: {enum_values}"
                    )
        
        return DatabaseResponse.success(data=value)

    @classmethod
    def _parse_date(cls, date_value) -> datetime:
        """Парсинг даты из различных форматов"""
        if isinstance(date_value, datetime):
            return date_value
        elif isinstance(date_value, date):
            return datetime.combine(date_value, datetime.min.time())
        elif isinstance(date_value, str):
            # Пробуем различные форматы дат
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d',
                '%d.%m.%Y %H:%M:%S',
                '%d.%m.%Y',
                '%Y-%m-%dT%H:%M:%S.%f'  # ISO формат с микросекундами
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_value, fmt)
                except ValueError:
                    continue
            
            raise ValueError(f"Неизвестный формат даты: {date_value}. Поддерживаемые форматы: {formats}")
        else:
            raise ValueError(f"Неподдерживаемый тип даты: {type(date_value).__name__}")

    @classmethod
    def _get_column_info(cls, table_name: str, column_name: str) -> DatabaseResponse:
        """Получение информации о конкретной колонке"""
        columns_response = cls.get_table_columns(table_name)
        if columns_response.status != ResponseStatus.SUCCESS:
            return columns_response
        
        columns_info = columns_response.data
        if column_name not in columns_info:
            return DatabaseResponse.error(
                ErrorCode.COLUMN_NOT_FOUND,
                f"Колонка '{column_name}' не найдена в таблице '{table_name}'"
            )
        
        return DatabaseResponse.success(data=columns_info[column_name])

    @classmethod
    @DatabaseErrorHandler()
    def get_related_tables(cls, table_name: str) -> DatabaseResponse:
        """Получение информации о таблицах, связанных с указанной через foreign keys"""

        model_response = cls.get_model_by_tablename(table_name)
        if model_response.status != ResponseStatus.SUCCESS:
            return model_response

        model = model_response.data
        related_tables = {}

        try:
            # Ищем внешние ключи из этой таблицы
            for column in model.__table__.columns:
                for fk in column.foreign_keys:
                    target_table = fk.column.table.name
                    if target_table not in related_tables:
                        related_tables[target_table] = {
                            'relationship_type': 'outgoing',
                            'columns': []
                        }
                    related_tables[target_table]['columns'].append({
                        'source_column': column.name,
                        'target_column': fk.column.name
                    })

            # Ищем внешние ключи, ссылающиеся на эту таблицу
            for mapper in Base.registry.mappers:
                other_model = mapper.class_
                if other_model.__tablename__ == table_name:
                    continue

                for column in other_model.__table__.columns:
                    for fk in column.foreign_keys:
                        if fk.column.table.name == table_name:
                            if other_model.__tablename__ not in related_tables:
                                related_tables[other_model.__tablename__] = {
                                    'relationship_type': 'incoming',
                                    'columns': []
                                }
                            related_tables[other_model.__tablename__]['columns'].append({
                                'source_column': column.name,
                                'target_column': fk.column.name
                            })

            return DatabaseResponse.success(
                data=related_tables,
                message=f"Найдено {len(related_tables)} связанных таблиц"
            )

        except Exception as e:
            return DatabaseResponse.error(
                ErrorCode.OPERATION_FAILED,
                f"Ошибка при получении связанных таблиц: {str(e)}"
            )

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

        columns_info = columns_response.data
        available_columns = set(columns_info.keys())

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

        # Проверяем обязательные поля (NOT NULL без default)
        missing_required = []
        for col_name, col_info in columns_info.items():
            if (not col_info['nullable'] and 
                col_info['default'] is None and 
                not col_info['primary_key'] and 
                col_name not in valid_params):
                missing_required.append(col_name)
        
        if missing_required:
            return DatabaseResponse.error(
                ErrorCode.INVALID_PARAMETERS,
                f"Отсутствуют обязательные поля: {', '.join(missing_required)}"
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
            logger.error(f"Ошибка при вставке в таблицу '{table_name}': {str(e)}")
            return DatabaseErrorHandler.handle_exception(e, f"insert_into_table for {table_name}")

    @classmethod
    @DatabaseErrorHandler()
    def update_table_data(
        cls,
        table_name: str,
        update_params: Dict[str, Any],
        filters_dict: Dict[str, Any],
    ) -> DatabaseResponse:
        """Обновление данных в таблице с поддержкой расширенных фильтров"""

        # Получаем модель таблицы
        model_response = cls.get_model_by_tablename(table_name)
        if model_response.status != ResponseStatus.SUCCESS:
            return model_response
        model = model_response.data

        # Получаем информацию о колонках
        columns_response = cls.get_table_columns(table_name)
        if columns_response.status != ResponseStatus.SUCCESS:
            return columns_response

        columns_info = columns_response.data
        available_columns = set(columns_info.keys())

        # Фильтруем update-параметры
        valid_params = {}
        invalid_params = []
        for key, value in update_params.items():
            if key in available_columns:
                valid_params[key] = value
            else:
                invalid_params.append(key)

        if not valid_params:
            return DatabaseResponse.error(
                ErrorCode.INVALID_PARAMETERS,
                "Не предоставлено ни одного корректного параметра для обновления",
                error_details={"invalid_parameters": invalid_params}
            )

        try:
            with Database().get_db_session() as session:
                query = update(model).values(valid_params)

                # Обработка фильтров
                if filters_dict:
                    joined_models = {table_name: model}
                    filter_conditions = cls._build_filter_conditions(
                        filters_dict, joined_models, table_name
                    )
                    if filter_conditions.status != ResponseStatus.SUCCESS:
                        return filter_conditions
                    if filter_conditions.data:
                        query = query.where(and_(*filter_conditions.data))

                result = session.execute(query)
                session.commit()

                response_data = {
                    "updated_data": valid_params,
                    "ignored_parameters": invalid_params if invalid_params else None
                }

                return DatabaseResponse.success(
                    data=response_data,
                    message=f"Обновлено {result.rowcount} записей в таблице '{table_name}'",
                    affected_rows=result.rowcount
                )

        except Exception as e:
            logger.error(f"Ошибка при обновлении таблицы '{table_name}': {str(e)}")
            return DatabaseErrorHandler.handle_exception(e, f"update_table_data for {table_name}")