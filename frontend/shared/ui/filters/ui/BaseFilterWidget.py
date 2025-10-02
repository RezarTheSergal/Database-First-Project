from PySide6.QtCore import Signal
from typing import Any, Dict
from frontend.shared.ui import HLayout, Widget, Text
from frontend.shared.lib import translate


class BaseFilterWidget(Widget):
    """Базовый класс для всех фильтров. Содержит общий интерфейс."""

    value_changed = Signal(object)  # Сигнал изменения значения
    column_info: Dict[str, Any]
    column_name: str
    input_widget: Any
    label: Text

    def __init__(self, column_name: str, column_info: Dict[str, Any], parent=None):
        super().__init__(HLayout())
        self.setMinimumWidth(400)
        self.column_name = column_name
        self.column_info = column_info
        self._value = None

        if parent:
            self.setParent(parent)

        # Create label for the filter
        display_text = column_info.get("display_name", column_name) or column_name
        if not display_text or display_text.strip() == "":
            import logging

            logger = logging.getLogger(__name__)
            logger.error(
                f"Display text is missing for column '{column_name}', using default 'Unknown'"
            )
            display_text = "Unknown"
        else:
            display_text = translate(display_text)

        self.label = Text(display_text + ":")  # Add colon for better readability
        self.layout.addWidget(self.label)

        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Создает и настраивает UI-компоненты (абстрактный метод)"""
        raise NotImplementedError("_setup_ui must be implemented")

    def _setup_connections(self):
        """Общие соединения сигналов"""
        pass

    def get_filter_value(self) -> Any:
        """Возвращает текущее значение фильтра"""
        return self._value

    def set_value(self, value: Any):
        """Устанавливает значение фильтра программно"""
        self._value = value
        self._update_ui_value(value)

    def is_empty(self) -> bool: # type: ignore
        pass

    def clear_value(self):
        """Очищает значение фильтра"""
        self._value = None
        self._update_ui_value(None)

    def _update_ui_value(self, value: Any):
        """Обновляет UI-компонент по значению"""
        pass
