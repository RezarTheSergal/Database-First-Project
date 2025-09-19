import subprocess
import os
from sqlalchemy import create_engine, text
from backend.database.models import Base
from backend.database.database import get_engine
from backend.settings import PgConfig

class SchemaCreator:
    """
    Класс для создания схемы базы данных с поддержкой Alembic
    """
    @staticmethod
    def create_database():
        """
        Создать саму базу данных, если она не существует
        """
        try:
            print("Проверка существования базы данных...")
            pg_config = PgConfig()
            
            # Разбор URL базы данных для получения деталей подключения
            db_url_parts = pg_config.database_url().split('/')
            database_name = db_url_parts[-1]  # Последняя часть - имя базы данных
            
            # Создание URL подключения без имени базы данных (подключение к базе 'postgres')
            base_url = '/'.join(db_url_parts[:-1]) + '/postgres'
            
            # Создание движка для подключения к базе данных postgres
            temp_engine = create_engine(base_url, isolation_level='AUTOCOMMIT')
            
            with temp_engine.connect() as conn:
                # Проверка существования базы данных
                result = conn.execute(text(
                    f"SELECT 1 FROM pg_database WHERE datname = '{database_name}'"
                ))
                
                if result.fetchone() is None:
                    print(f"База данных '{database_name}' не найдена. Создание...")
                    conn.execute(text(f"CREATE DATABASE \"{database_name}\""))
                    print(f"База данных '{database_name}' создана успешно!")
                    return {"status": "success", "message": f"База данных '{database_name}' создана"}
                else:
                    print(f"База данных '{database_name}' уже существует!")
                    return {"status": "success", "message": f"База данных '{database_name}' уже существует"}
                    
        except Exception as e:
            print(f"Ошибка создания базы данных: {e}")
            return {"status": "error", "message": f"Ошибка создания базы данных: {str(e)}"}
    
    @staticmethod
    def create_schema_with_alembic():
        """
        Создать схему базы данных с использованием миграций Alembic
        """
        try:
            print("Создание схемы базы данных с помощью Alembic...")
            
            # Запуск alembic upgrade для создания/обновления схемы
            result = subprocess.run(['alembic', 'upgrade', 'head'], 
                                  capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                print("Схема базы данных создана успешно с помощью Alembic!")
                print("Вывод Alembic:", result.stdout)
                return {"status": "success", "message": "Схема создана с помощью Alembic"}
            else:
                print("Ошибка выполнения миграций Alembic:")
                print("Вывод ошибки:", result.stderr)
                return {"status": "error", "message": f"Ошибка Alembic: {result.stderr}"}
                
        except FileNotFoundError:
            print("Alembic не найден. Убедитесь, что Alembic установлен и настроен.")
            return {"status": "error", "message": "Alembic не найден"}
        except Exception as e:
            print(f"Ошибка создания схемы с помощью Alembic: {e}")
            return {"status": "error", "message": str(e)}
    
    @staticmethod
    def create_schema_direct():
        """
        Создать схему базы данных напрямую (резервный метод)
        """
        try:
            print("Создание схемы базы данных напрямую...")
            engine = get_engine()
            Base.metadata.create_all(bind=engine)
            print("Таблицы базы данных созданы успешно!")
            return {"status": "success", "message": "Схема создана напрямую"}
        except Exception as e:
            print(f"Ошибка создания таблиц базы данных: {e}")
            return {"status": "error", "message": str(e)}
    
    @staticmethod

    def init_db():
        """
        Инициализация базы данных - сначала пробует Alembic, затем прямое создание
        """
        # Сначала пробуем Alembic
        result = SchemaCreator.create_schema_with_alembic()
        
        if result["status"] == "success":
            return result
        
        # Резервный вариант - прямое создание
        print("Переход к прямому созданию схемы...")
        return SchemaCreator.create_schema_direct()
    
    @staticmethod
    def create_initial_migration():
        """
        Создать начальную миграцию Alembic
        """
        try:
            print("Создание начальной миграции Alembic...")
            
            result = subprocess.run(['alembic', 'revision', '--autogenerate', '-m', 'Initial migration'], 
                                  capture_output=True, text=True, cwd='.')
            
            if result.returncode == 0:
                print("Начальная миграция создана успешно!")
                return {"status": "success", "message": "Начальная миграция создана"}
            else:
                print("Ошибка создания миграции:")
                print("Вывод ошибки:", result.stderr)
                return {"status": "error", "message": f"Ошибка миграции: {result.stderr}"}
                
        except Exception as e:
            print(f"Ошибка создания миграции: {e}")
            return {"status": "error", "message": str(e)}


# Основные функции для внешнего использования
def init_db():
    """Инициализация схемы базы данных - основная точка входа для создания схемы"""
    return SchemaCreator.init_db()

def create_migration():
    """Создать новую миграцию Alembic"""
    return SchemaCreator.create_initial_migration()

