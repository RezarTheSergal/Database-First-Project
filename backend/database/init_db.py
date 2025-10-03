"""
Модуль инициализации базы данных
Содержит функцию для полной настройки БД
"""
import logging
from pathlib import Path
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
from backend.utils.database_exception_handler import DatabaseErrorHandler
from backend.utils.responce_types import DatabaseResponse, ErrorCode
from backend.settings import PgConfig
from psycopg2 import connect, sql

# Предполагаем, что импорты настроены правильно (без sys.path.append)
from .database import Database
from .models import Base

db_engine = Database().get_engine()
logger = logging.getLogger(__name__)


@DatabaseErrorHandler()
def create_database_if_not_exists() -> DatabaseResponse:
    """Создает базу данных, если она не существует"""
    pg_config = PgConfig()
    db_name = pg_config.dbname
    db_user = pg_config.user
    creational_url = f"postgresql+psycopg2://{db_user}:{pg_config.password}@{pg_config.host}:{pg_config.port}/postgres"
    creational_engine = create_engine(creational_url, isolation_level='AUTOCOMMIT')
    
    with creational_engine.connect() as conn:
        # Параметризованный запрос для проверки существования
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :db_name LIMIT 1"),
            {"db_name": db_name}
        )
        exists = result.scalar() is not None
        
        if not exists:
            logger.info(f"Создание базы данных '{db_name}'...")
            # Используем psycopg2 для безопасного CREATE и GRANT
            pg_conn = connect(
                host=pg_config.host,
                port=pg_config.port,
                user=db_user,
                password=pg_config.password,
                database='postgres'
            )
            try:
                with pg_conn.cursor() as cur:
                    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                    cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
                        sql.Identifier(db_name), sql.Identifier(db_user)
                    ))
                    pg_conn.commit()
                logger.info(f"База данных '{db_name}' успешно создана")
                logger.info(f"Права доступа предоставлены пользователю '{db_user}'")
            except Exception as e:
                pg_conn.rollback()
                raise
            finally:
                pg_conn.close()
        else:
            logger.info(f"База данных '{db_name}' уже существует")
    
    return DatabaseResponse.success()


def _get_table_counts(engine) -> dict[str, int]:
    """Внутренняя функция: получает количество строк во всех таблицах (отдельные запросы для простоты)"""
    inspector = inspect(engine)
    table_names = [t for t in inspector.get_table_names(schema='public') if t in Base.metadata.tables]
    counts = {}
    
    if not table_names:
        return counts
    
    with engine.connect() as conn:
        for table_name in table_names:
            try:
                result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                counts[table_name] = result.scalar() or 0
                logger.debug(f"Подсчёт для {table_name}: {counts[table_name]}")
            except Exception as e:
                logger.warning(f"Ошибка подсчета в {table_name}: {e}")
                counts[table_name] = 0
    
    return counts


@DatabaseErrorHandler()
def print_table_row_counts() -> None:
    """Выводит количество строк в каждой таблице"""
    counts = _get_table_counts(db_engine)
    if counts:
        logger.info("Количество записей в таблицах:")
        for table_name in sorted(counts):
            count = counts[table_name]
            logger.info(f" - {table_name}: {count} записей")
    else:
        logger.info("Таблицы отсутствуют или пусты")


@DatabaseErrorHandler()
def _load_test_data(sql_file_path: Path) -> None:
    """Внутренняя функция: загружает тестовые данные из SQL-файла (весь скрипт целиком)"""
    if not sql_file_path.exists():
        raise FileNotFoundError(f"Файл тестовых данных не найден: {sql_file_path}")
    
    logger.info("Загрузка тестовых данных из db_test_data.sql...")
    with open(sql_file_path, encoding="utf-8") as f:
        sql_script = f.read()
    
    logger.debug(f"Размер SQL-скрипта: {len(sql_script)} символов")
    
    # Проверяем наличие ENUM перед загрузкой
    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT 1 FROM pg_type WHERE typname = 'caffeine_level' LIMIT 1"))
        enum_exists = result.scalar() is not None
        logger.debug(f"ENUM 'caffeine_level' существует: {enum_exists}")
    
    # Выполняем весь скрипт в одной транзакции (psycopg2 поддерживает multi-statements)
    with db_engine.connect() as conn:
        with conn.begin():
            try:
                conn.execute(text(sql_script))
                logger.debug("SQL-скрипт выполнен успешно")
            except SQLAlchemyError as e:
                logger.error(f"КРИТИЧЕСКАЯ ОШИБКА в SQL-скрипте: {e}")
                # Дополнительно: логируем первые 200 символов скрипта для отладки
                logger.error(f"Начало скрипта: {sql_script[:200]}...")
                raise


@DatabaseErrorHandler()
def create_tables() -> DatabaseResponse:
    """Создает все таблицы в базе данных"""
    metadata_tables = set(Base.metadata.tables.keys())
    inspector = inspect(db_engine)
    db_tables = set(inspector.get_table_names(schema='public'))
    tables_to_create = metadata_tables - db_tables
    
    if tables_to_create:
        Base.metadata.create_all(bind=db_engine)
        logger.info(f"Созданы таблицы: {', '.join(sorted(tables_to_create))}")
    else:
        logger.info("Все таблицы уже существуют!")
    
    # Логируем список таблиц (без conn, используем inspector)
    tables = inspector.get_table_names(schema='public')
    if tables:
        logger.info("Список таблиц:")
        for table in sorted(tables):
            print(f" - {table}")
    else:
        logger.info("Таблицы отсутствуют")
    
    # Проверяем наличие данных (any >0)
    counts = _get_table_counts(db_engine)
    has_data = any(count > 0 for count in counts.values())
    logger.info(f"Есть данные в БД (хотя бы в одной таблице): {has_data}")
    
    if not has_data:
        sql_file_path = Path(__file__).parent / "db_test_data.sql"
        logger.info(f"Проверка файла тестовых данных: существует = {sql_file_path.exists()}")
        
        if sql_file_path.exists():
            try:
                _load_test_data(sql_file_path)
                logger.info("Тестовые данные успешно загружены!")
                # Немедленная проверка после загрузки
                post_load_counts = _get_table_counts(db_engine)
                logger.info(f"Подсчёт ПОСЛЕ загрузки: {post_load_counts}")
            except (FileNotFoundError, SQLAlchemyError) as e:
                logger.warning(f"Не удалось загрузить тестовые данные: {e}")
                # Не прерываем инициализацию
        else:
            logger.warning(f"Файл {sql_file_path} не найден. Тестовые данные не загружены.")
    else:
        logger.info("В БД уже есть данные, тестовые данные не загружаются")
    
    # Финальный вывод статистики
    print_table_row_counts()
    return DatabaseResponse.success()


@DatabaseErrorHandler()
def init_database() -> DatabaseResponse:
    """
    Основная функция инициализации базы данных
    Создает БД (если не существует) и все таблицы
    Возвращает DatabaseResponse с статусом
    """
    logger.info("Инициализация базы данных...")
    
    # Шаг 1: Создание БД
    db_response = create_database_if_not_exists()
    if db_response.status == "error":
        return DatabaseResponse.error(
            error_code=db_response.error_code or ErrorCode.UNKNOWN_ERROR,
            message="Не удалось создать базу данных",
            error_details=db_response.error_details or {}
        )
    
    # Шаг 2: Создание таблиц и данных
    tables_response = create_tables()
    if tables_response.status == "error":
        return DatabaseResponse.error(
            error_code=tables_response.error_code or ErrorCode.UNKNOWN_ERROR,
            message="Не удалось создать таблицы",
            error_details=tables_response.error_details or {}
        )

    logger.info("База данных успешно инициализирована!")
    return DatabaseResponse.success()