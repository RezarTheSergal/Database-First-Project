from abc import ABC, abstractmethod
from typing import Any, Dict
from PySide6.QtWidgets import QWidget, QLabel
from frontend.shared.ui import HLayout

class BaseFilterWidget(QWidget):
    """Базовый класс для всех типов фильтров"""
    
    def __init__(self, column_name: str, column_info: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.column_name = column_name
        self.column_info = column_info
        self._setup_ui()
        self._setup_connections()
    
    def _setup_ui(self):
        """Настройка базового UI"""
        self.hor_layout = HLayout()
        self.setLayout(self.hor_layout)
        
        self.label = QLabel(f"{self.column_name}:")
        self.label.setMinimumWidth(120)
        self.hor_layout.addWidget(self.label)
        
        self.input_widget = self._create_input_widget()
        if self.input_widget:
            self.hor_layout.addWidget(self.input_widget)
    
    @abstractmethod
    def _create_input_widget(self) -> QWidget:
        """Создает виджет ввода для конкретного типа фильтра"""
        pass
    
    @abstractmethod
    def get_filter_value(self) -> Any:
        """Возвращает текущее значение фильтра"""
        pass
    
    @abstractmethod
    def clear_value(self):
        """Очищает значение фильтра"""
        pass
    
    def _setup_connections(self):
        """Настройка соединений сигналов (переопределяется в наследниках)"""
        pass
    
    def is_empty(self) -> bool:
        """Проверяет, пустой ли фильтр"""
        value = self.get_filter_value()
        return value is None or value == "" or value == 0 or value == False
