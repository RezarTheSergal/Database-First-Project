from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from backend.settings import PgConfig
from backend.utils.exception_handler import ExceptionHandler


class Singleton(type):
    _instances = {}
    def __call__(self, *args, **kwds):
        if self not in self._instances:
            instance = super().__call__(*args, **kwds)
            self._instances[self] = instance
        return self._instances[self]

class Database(metaclass=Singleton):
    def __init__(self):
        # Получение конфигурации базы данных из настроек
        self._pg_config = PgConfig()
        # Создание движка и фабрики сессий
        self._engine = self.create_database_engine()
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    @ExceptionHandler()
    def create_database_engine(self) -> Engine:
        """
        Создание движка SQLAlchemy с использованием настроек PgConfig
        """
        database_url = self._pg_config.database_url()
        
        engine = create_engine(
            database_url,
            echo=self._pg_config.echo if hasattr(self._pg_config, 'echo') else False,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True  # Проверка соединений перед использованием
        )
        
        return engine



    @contextmanager
    @ExceptionHandler()
    def get_db_session(self):
        """
        Контекстный менеджер для сессий базы данных с автоматическим управлением транзакциями
        """
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Транзакция отменена из-за ошибки: {e}")
            raise
        finally:
            session.close()

    def get_engine(self) -> Engine:
        """
        Получить экземпляр движка базы данных
        """
        return self._engine

    def get_database_url(self) -> str:
        """
        Получить URL базы данных из PgConfig
        """
        return self._pg_config.database_url()
    
