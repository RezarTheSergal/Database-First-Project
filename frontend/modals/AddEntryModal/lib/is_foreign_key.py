def is_foreign_key(entry: dict) -> bool:
    """Возвращает True, если название свойства заканчивается на _id"""
    return len(entry.get("foreign_keys",[])) > 0
