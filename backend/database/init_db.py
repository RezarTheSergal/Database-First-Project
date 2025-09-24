"""
Модуль инициализации базы данных
Содержит функцию для полной настройки БД
"""

import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine, text, inspect 
from backend.utils.database_exception_handler import DatabaseErrorHandler
# Добавляем путь для импортов
sys.path.append(str(Path(__file__).parent.parent))

from .database import Database
from .models import Base
from backend.settings import PgConfig
import logging

db_engine = Database().get_engine()
logger = logging.getLogger()

@DatabaseErrorHandler()
def create_database_if_not_exists() -> True:
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
                
    return True

    

@DatabaseErrorHandler()
def create_tables() -> None:
    """Создает все таблицы в базе данных"""

    metadata_tables = set(Base.metadata.tables.keys())
    db_tables = set(inspect(db_engine).get_table_names())

    if len(metadata_tables.intersection(db_tables)) == len(metadata_tables):
        logger.info("Все таблицы уже существуют!")
        return

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
            logging.info("Список созданных таблиц:")
            for table in tables:
                print(f"   - {table[0]}")
                    
    
@DatabaseErrorHandler()
def init_database() -> bool:
    """
    Основная функция инициализации базы данных
    Создает БД (если не существует) и все таблицы
    Возвращает True при успехе, False при ошибке
    """
    logging.info("Инициализация базы данных...")
    
    # Создаем базу данных, если не существует
    if not create_database_if_not_exists():
        return False
    
    # Создаем таблицы
    if not create_tables():
        return False
    
    logger.info("База данных успешно инициализирована!")
    return True
