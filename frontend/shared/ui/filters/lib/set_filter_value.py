from typing import Any
from frontend.shared.ui.filters.ui.BaseFilterWidget import BaseFilterWidget


def set_filter_value(filter_widget: BaseFilterWidget, value: Any):
    # Пытаемся вызвать set_value, если метод существует
    if hasattr(filter_widget, "set_value"):
        filter_widget.set_value(value)
    elif hasattr(filter_widget, "input_widget"):
        # Для случаев, когда нужно напрямую установить значение во внутренний виджет
        input_widget = filter_widget.input_widget
        if hasattr(input_widget, "setValue"):
            input_widget.setValue(value)
        elif hasattr(input_widget, "setText"):
            input_widget.setText(str(value) if value is not None else "")
        elif hasattr(input_widget, "setChecked"):
            input_widget.setChecked(bool(value))
        elif hasattr(input_widget, "setCurrentText"):
            input_widget.setCurrentText(str(value) if value is not None else "")
        # Обновляем внутреннее значение фильтра
        filter_widget._value = value
