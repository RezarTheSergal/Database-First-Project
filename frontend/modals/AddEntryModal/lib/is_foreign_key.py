def is_foreign_key(name: str) -> bool:
    """Возвращает True, если название свойства заканчивается на _id"""
    return name.endswith("_id")
