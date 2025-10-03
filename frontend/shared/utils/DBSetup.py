from backend.database.init_db import init_database
from backend.utils.responce_types import DatabaseResponse
from .MessageFactory import MessageFactory
from frontend.shared.ui import Widget


def init_database_callback(parent: Widget) -> DatabaseResponse:
    # drpepperus666 ответ нужно проверить на наличие ошибок при выполнении запроса к API
    response = init_database()
    MessageFactory.show_response_message(response)
    return response
