from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', default=True)
HOST = env.str('DB_HOST', default='localhost')
PORT = env.str('DB_PORT', default='5432')
USER = env.str('DB_USER', default='postgres')
NAME = env.str('DB_NAME', default='university')
PASSWORD = env.str('DB_PASSWORD')

@dataclass
class PgBase:
    host: str = HOST
    port: int = PORT
    dbname: str = NAME
    user: str = USER
    password: str = PASSWORD
    sslmode: str = "prefer"       # для psycopg2/psycopg
    connect_timeout: int = 5      # секунды
    driver: str = "psycopg2"      # psycopg2 | psycopg | pg8000

class PgConfig(PgBase):
    def database_url(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

