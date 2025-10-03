from pprint import pprint
from typing import Any
from frontend.shared.ui.inputs import (
    ComboBox,
    ForeignKeySearchBox,
    StringInput,
    IntInput,
    FloatInput,
    BoolInput,
    DateInput
)


class InputWidgetFactory:
    """Фабрика для создания инпутов"""

    @staticmethod
    def create(meta: dict[str, Any]) -> Any:
        """
        Создает подходящий инпут на основе информации о колонке
        """
        pprint(meta)
        # 1. ENUM - выпадающий список
        if meta.get("enum_values"):
            return ComboBox(**meta)

        # 2. FOREIGN KEY - поиск с автодополнением
        elif meta.get("foreign_keys"):
            meta["column_info"] = meta
            meta["column_name"] = meta.get("column_name")
            return ForeignKeySearchBox(**meta)

        # 3. Стандартные типы
        else:
            column_type = (meta.get("type") or "").upper()

            if any(t in column_type for t in ("TEXT", "VARCHAR", "CHAR", "STRING")):
                return StringInput(**meta)
            elif any(t in column_type for t in ("INTEGER", "BIGINT", "SERIAL")):
                return IntInput(**meta)
            elif any(t in column_type for t in ("NUMERIC", "DECIMAL", "FLOAT", "REAL")):
                return FloatInput(**meta)
            elif "BOOLEAN" in column_type:
                return BoolInput(**meta)
            elif any(t in column_type for t in ("DATE", "DATETIME", "TIMESTAMP")):
                return DateInput(**meta)
            else:
                # Fallback для неизвестных типов
                return StringInput(**meta)
