import logging
from backend.database.init_db import init_database
from backend.utils.logger import setup_logging
from backend.settings import LOG_FILE_PATH
if __name__ == "__main__":
    setup_logging(level=logging.INFO, log_file=LOG_FILE_PATH, console_log=True) # Не убирать отсюда, всё логгирование держится на этом!
    init_database()
