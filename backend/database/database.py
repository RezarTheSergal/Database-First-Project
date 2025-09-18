from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from backend.settings import PgConfig

# Получение конфигурации базы данных из настроек
pg_config = PgConfig()

def create_database_engine():
    """
    Создание движка SQLAlchemy с использованием настроек PgConfig
    """
    database_url = pg_config.database_url()
    
    engine = create_engine(
        database_url,
        echo=pg_config.echo if hasattr(pg_config, 'echo') else False,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True  # Проверка соединений перед использованием
    )
    
    return engine

# Создание движка и фабрики сессий
engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db_session():
    """
    Контекстный менеджер для сессий базы данных с автоматическим управлением транзакциями
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Транзакция отменена из-за ошибки: {e}")
        raise
    finally:
        session.close()

def get_engine():
    """
    Получить экземпляр движка базы данных
    """
    return engine

def get_database_url():
    """
    Получить URL базы данных из PgConfig
    """
    return pg_config.database_url()
