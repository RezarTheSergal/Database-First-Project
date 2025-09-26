from typing import Dict, Any
from .base import BaseFilterWidget
from .foreign_key_filter import ForeignKeyFilterWidget
from .string_filter import StringFilterWidget
from .numeric_filter import IntegerFilterWidget, FloatFilterWidget
from .bool_filter import BooleanFilterWidget
from .date_filter import DateFilterWidget
from .enum_filter import EnumFilterWidget

class FilterWidgetFactory:
    """Фабрика для создания виджетов фильтров"""
    
    @staticmethod
    def create_filter_widget(column_name: str, column_info: Dict[str, Any]) -> BaseFilterWidget:
        """
        Создает подходящий виджет фильтра на основе информации о колонке
        """
        # 1. ENUM - выпадающий список
        if column_info.get("enum_values"):
            return EnumFilterWidget(column_name, column_info)
        
        # 2. FOREIGN KEY - поиск с автодополнением
        elif column_info.get("foreign_keys"):
            return ForeignKeyFilterWidget(column_name, column_info)
        
        # 3. Стандартные типы
        else:
            col_type_upper = (column_info.get("type") or "").upper()
            
            if any(t in col_type_upper for t in ("TEXT", "VARCHAR", "CHAR", "STRING")):
                return StringFilterWidget(column_name, column_info)
            
            elif any(t in col_type_upper for t in ("INTEGER", "BIGINT", "SERIAL")):
                return IntegerFilterWidget(column_name, column_info)
            
            elif any(t in col_type_upper for t in ("NUMERIC", "DECIMAL", "FLOAT", "REAL")):
                return FloatFilterWidget(column_name, column_info)
            
            elif "BOOLEAN" in col_type_upper:
                return BooleanFilterWidget(column_name, column_info)
            
            elif any(t in col_type_upper for t in ("DATE", "DATETIME", "TIMESTAMP")):
                return DateFilterWidget(column_name, column_info)
            
            else:
                # Fallback для неизвестных типов
                return StringFilterWidget(column_name, column_info)