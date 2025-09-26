import json
from backend.settings import LOCALES_PATH
from backend.utils.join_path import join_path

ru = open(
    join_path(LOCALES_PATH, "locales/ru.json").__str__(),
    "r",
    encoding="utf8",
)

translations = json.load(ru)

def translate(value: str) -> str:
    """
    Возвращает перевод фразы с английского на русский.
    Если перевода нет, возвращает фразу на английском.
    """
    return translations.get(value.lower(), value)
