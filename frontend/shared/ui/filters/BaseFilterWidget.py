from abc import abstractmethod
from typing import Any, Dict
from PySide6.QtWidgets import QWidget, QLabel
from frontend.shared.ui import HLayout
from frontend.shared.ui.inputs import (
    StringInput,
    IntInput,
    FloatInput,
    BoolInput,
    ComboBox,
    DateInput,
)
from frontend.shared.lib import get_element_by_type
from backend.utils.logger import logging

logger = logging.getLogger("frontend")


class BaseFilterWidget(QWidget):
    """Базовый класс для всех типов фильтров"""

    input_widget: StringInput | IntInput | FloatInput | BoolInput | ComboBox | DateInput

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

        self.input_widget = self._create_input_widget(self.column_info["type"])
        if self.input_widget:
            self.hor_layout.addWidget(self.input_widget)

    @abstractmethod
    def _create_input_widget(self, type: str):
        """Создает виджет ввода для конкретного типа фильтра"""
        return get_element_by_type(type)

    @abstractmethod
    def get_filter_value(self):
        """Возвращает текущее значение фильтра"""
        return self.input_widget.get_value()

    @abstractmethod
    def clear_value(self) -> None:
        if isinstance(self.input_widget, StringInput):
            self.input_widget.setText("")
        elif isinstance(self.input_widget, (FloatInput, IntInput)):
            self.input_widget.setValue(0)
        else:
            logger.error("Can't ")

    def _setup_connections(self):
        """Настройка соединений сигналов (переопределяется в наследниках)"""
        pass

    def is_empty(self) -> bool:
        """Проверяет, пустой ли фильтр"""
        value = self.get_filter_value()
        return value in [None, "", 0, False]
