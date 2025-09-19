"""
Модуль инициализации базы данных
Содержит функцию для полной настройки БД
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, text

# Добавляем путь для импортов
sys.path.append(str(Path(__file__).parent.parent))

from .database import get_engine
from .models import Base
from backend.settings import PgConfig

def create_database_if_not_exists():
    """Создает базу данных, если она не существует"""
    try:
        pg_config = PgConfig()
        
        # Получаем параметры подключения к серверу PostgreSQL
        db_url = pg_config.database_url()
        base_url = '/'.join(db_url.split('/')[:-1]) + '/postgres'
        
        # Создаем engine с autocommit для создания БД
        engine = create_engine(base_url, isolation_level="AUTOCOMMIT")
        
        # Используем правильные атрибуты из PgConfig
        db_name = pg_config.dbname 
        db_user = pg_config.user  
        
        # Проверяем существование базы данных
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            exists = result.scalar()
            
            if not exists:
                print(f"Создание базы данных '{db_name}'...")
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"База данных '{db_name}' успешно создана")
                
                # Даем права пользователю
                conn.execute(text(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}"))
                print(f"Права доступа предоставлены пользователю '{db_user}'")
            else:
                print(f"База данных '{db_name}' уже существует")
                
        return True
        
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
        return False

def create_tables():
    """Создает все таблицы в базе данных"""
    try:
        engine = get_engine()
        Base.metadata.create_all(bind=engine)
        print("Все таблицы успешно созданы")
        
        # Выводим список созданных таблиц
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            
            tables = result.fetchall()
            if tables:
                print("Список созданных таблиц:")
                for table in tables:
                    print(f"   - {table[0]}")
                    
        return True
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        return False

def init_database():
    """
    Основная функция инициализации базы данных
    Создает БД (если не существует) и все таблицы
    Возвращает True при успехе, False при ошибке
    """
    print("Инициализация базы данных...")
    
    # Создаем базу данных, если не существует
    if not create_database_if_not_exists():
        return False
    
    # Создаем таблицы
    if not create_tables():
        return False
    
    print("База данных успешно инициализирована!")
    return True
