"""
Модуль инициализации базы данных
Содержит функцию для полной настройки БД
"""

import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine, text, inspect 
from backend.utils.database_exception_handler import DatabaseErrorHandler
from backend.utils.responce_types import DatabaseResponse, ErrorCode
# Добавляем путь для импортов
sys.path.append(str(Path(__file__).parent.parent))

from .database import Database
from .models import Base
from backend.settings import PgConfig
import logging

db_engine = Database().get_engine()
logger = logging.getLogger()

@DatabaseErrorHandler()
def create_database_if_not_exists() -> DatabaseResponse:
    """Создает базу данных, если она не существует"""

    pg_config = PgConfig()
        
    # Используем правильные атрибуты из PgConfig
    db_name = pg_config.dbname 
    db_user = pg_config.user  
    creational_url = f"postgresql+psycopg2://{db_user}:{pg_config.password}@{pg_config.host}:{pg_config.port}/postgres"
    creational_engine = create_engine(creational_url, isolation_level='AUTOCOMMIT')

    # Проверяем существование базы данных
    with creational_engine.connect() as conn:
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
        exists = result.scalar()
            
        if not exists:
            logger.info(f"Создание базы данных '{db_name}'...")
            conn.execute(text(f"CREATE DATABASE {db_name}"))
            logger.info(f"База данных '{db_name}' успешно создана")
                
            # Даем права пользователю
            conn.execute(text(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}"))
            logger.info(f"Права доступа предоставлены пользователю '{db_user}'")
        else:
            logger.info(f"База данных '{db_name}' уже существует")
                
    return DatabaseResponse.success()

    

@DatabaseErrorHandler()
def create_tables() -> DatabaseResponse:
    """Создает все таблицы в базе данных"""

    metadata_tables = set(Base.metadata.tables.keys())
    db_tables = set(inspect(db_engine).get_table_names())

    # if len(metadata_tables.intersection(db_tables)) == len(metadata_tables):
    #     logger.info("Все таблицы уже существуют!")
    #     return DatabaseResponse.success()

    Base.metadata.create_all(bind=db_engine)
    logger.info("Все таблицы успешно созданы!")

    # Выводим список созданных таблиц
    with db_engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
            
        tables = result.fetchall()
        if tables:
            logger.info("Список созданных таблиц:")
            for table in tables:
                print(f"   - {table[0]}")
        # with open(r"db_test_data.sql", encoding="utf-8") as f:
        #     sql = f.read()
        # conn.execute(text(sql))
        # conn.commit()
    return DatabaseResponse.success()
                    
    
@DatabaseErrorHandler()
def init_database() -> DatabaseResponse:
    """
    Основная функция инициализации базы данных
    Создает БД (если не существует) и все таблицы
    Возвращает True при успехе, False при ошибке
    """
    logger.info("Инициализация базы данных...")
    created_db = create_database_if_not_exists().to_dict()
    # Создаем базу данных, если не существует
    if created_db.get("status", "success") == "error":
        return DatabaseResponse.error(
            error_code=created_db.get("error_code", ErrorCode.UNKNOWN_ERROR),
            message="Не удалось создать базу данных",
            error_details=created_db.get("error_details", {})
        )
    
    created_tables = create_tables().to_dict()
    # Создаем таблицы
    if created_tables.get("status", "success") == "error":
        return DatabaseResponse.error(
            error_code=created_tables.get("error_code", ErrorCode.UNKNOWN_ERROR),
            message="Не удалось создать таблицы",
            error_details=created_tables.get("error_details", {})
        )
    
    logger.info("База данных успешно инициализирована!")
    return DatabaseResponse.success()
