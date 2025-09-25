TRANSLATIONS = {
    "flavor": "Вкус",
    "name": "Название",
    "description": "Описание",
    "localtion": "Место",
    "unit": "Мера измерения",
    "temperature": "Температура",
    "noise": "Шум",
    "pressure": "Давление",
    "vibration": "Вибрация",
    "type": "Тип",
    "volume_ml": "Объем, мл",
    "price": "Цена, руб.",
    "ingredients": "Состав",
    "value": "Значение",
    "timestamp": "Точное время",
    "location": "Место",
    "install_date": "Дата установки",
    "status": "Статус",
    "last_service": "Дата последнего обслуживания",
}


def translate(value: str) -> str:
    return TRANSLATIONS.get(value.lower(), value)
