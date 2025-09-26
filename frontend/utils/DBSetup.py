from backend.database.init_db import init_database
from backend.utils.responce_types import DatabaseResponse

def init_database_callback() -> DatabaseResponse:
    # drpepperus666 ответ нужно проверить на наличие ошибок при выполнении запроса к API
    responce = init_database()
    return responce