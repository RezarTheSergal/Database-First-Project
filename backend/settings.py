from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
load_dotenv(".env")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', default=True)

# Logging file setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, 'logs', 'latest.log')
Path(LOG_FILE_PATH).parent.mkdir(exist_ok=True, parents=True)

# Styles path (frontend)
STYLESHEET_PATH = (
    Path(BASE_DIR).parent.resolve() / "frontend" / "styles" / "style.qss"
).__str__()

# Icon path (frontend)
ICON_PATH = (
    Path(BASE_DIR).parent.resolve() / "frontend" / "images" / "favicon.ico"
).__str__()

# Postgres env setup
HOST = os.getenv('DB_HOST', default='localhost')
PORT = os.getenv('DB_PORT', default='5432')
USER = os.getenv('DB_USER', default='postgres')
NAME = os.getenv('DB_NAME', default='university')
PASSWORD = os.getenv("DB_PASSWORD")

if not PASSWORD:
    print("No database password given, check your /.env")
    exit(1)

@dataclass
class PgBase:
    host: str = HOST
    port: int = int(PORT)
    dbname: str = NAME
    user: str = USER
    password: str = PASSWORD
    sslmode: str = "prefer"       # для psycopg2/psycopg
    connect_timeout: int = 5      # секунды
    driver: str = "psycopg2"      # psycopg2 | psycopg | pg8000

class PgConfig(PgBase):
    def database_url(self):
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
