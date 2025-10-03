from typing import Any
from frontend.shared.lib import translate


def convert_to_ui_value(column_meta: dict[str,Any],foreign_key_meta:dict[str,Any], col_name: str, value: Any) -> str:
    """Преобразует значение в строку для отображения в таблице"""
    if value is None:
        return ""

    col_info = column_meta.get(col_name, {})
    col_type = (col_info.get("type") or "").upper()

    # Обработка ENUM
    if col_info.get("enum_values"):
        return str(value)

    # Обработка внешних ключей
    if col_info.get("foreign_keys"):
        fk_data = foreign_key_meta.get(col_name, [])
        for id_val, display_val in fk_data:
            if id_val == value:
                return display_val
        return f"ID: {value}"

    # Обработка дат
    if "DATE" in col_type:
        if isinstance(value, str):
            return value
        return value.strftime("%Y-%m-%d")

    # Обработка чисел
    if "INTEGER" in col_type:
        return str(int(value)) if value is not None else ""
    if any(t in col_type for t in ("NUMERIC", "DECIMAL", "FLOAT", "REAL")):
        return str(float(value)) if value is not None else ""

    # Обработка булево
    if "BOOLEAN" in col_type:
        return translate("Yes") if value else translate("No")

    # По умолчанию
    return str(value) if value is not None else ""