from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBSession:
    _engine = None
    _SessionLocal = None

    @classmethod
    def init(self, db_url):
        self._engine = create_engine(db_url, echo=True, future=True)
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

    @classmethod
    def get_session(self):
        if self._SessionLocal is None:
            raise Exception("DBSession not initialized.")
        return self._SessionLocal()