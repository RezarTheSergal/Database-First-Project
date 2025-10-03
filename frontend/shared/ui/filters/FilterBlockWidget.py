from typing import Any, Dict, Optional

from PySide6.QtWidgets import QLayoutItem
from backend.utils.responce_types import DatabaseResponse, ResponseStatus
from frontend.shared.ui import VLayout, Widget, HLayout
from frontend.shared.ui.inputs.ComboBox import ComboBox
from backend.repository import DatabaseRepository
from .ui.FilterWidgetFactory import FilterWidgetFactory
from .ui.BaseFilterWidget import BaseFilterWidget
from .lib.set_filter_value import set_filter_value
import logging

logger = logging.getLogger()
database = DatabaseRepository()


class FilterBlockWidget(Widget):
    def __init__(self, initial_tables=None, parent: None | Widget = None):
        super().__init__(HLayout())
        if parent is not None:
            self.setParent(parent)

        # Основной layout
        self.layout.setContentsMargins(0, 0, 0, 0)

        # ComboBox для выбора таблицы
        self.table_combo = ComboBox(
            items=initial_tables or [], callback=self._on_table_changed
        )
        self.table_combo.setMinimumWidth(150)

        # Контейнер для фильтров
        self.filters_container = Widget(VLayout())

        # Словарь для хранения виджетов фильтров
        self.filter_widgets: Dict[str, BaseFilterWidget] = {}

        # Добавляем в layout
        self.layout.add_children([self.table_combo, self.filters_container])

    def _on_table_changed(self, table_name: str):
        """Обновляет фильтры под выбранную таблицу"""
        if not table_name:
            return

        self.clear_filters()

        columns_info = self._get_columns_info(table_name)
        if not columns_info:
            logger.error(
                f"Не удалось получить информацию о колонках для таблицы {table_name}"
            )
            return

        # Создаем фильтры для каждой колонки
        for col_name, col_meta in columns_info.items():
            try:
                filter_widget: BaseFilterWidget = FilterWidgetFactory.create_filter_widget(
                    col_name, col_meta
                )

                if filter_widget:
                    self.filter_widgets[col_name] = filter_widget
                    # Add the filter widget directly to the container layout
                    # Since each filter widget is a Widget with its own layout,
                    # we can add it directly
                    self.filters_container.layout.addWidget(filter_widget)

                    # Подключаем сигналы если нужно
                    if hasattr(filter_widget, "value_changed"):
                        filter_widget.value_changed.connect(
                            lambda value, col=col_name: self._on_filter_value_changed(
                                col, value
                            )
                        )

            except Exception as e:
                logger.error(f"Ошибка создания фильтра для колонки {col_name}: {e}")

    def _get_columns_info(self, table_name: str) -> Optional[Dict[str, dict]]:
        """Получает информацию о колонках таблицы"""
        try:
            response: DatabaseResponse = database.get_table_columns(table_name)

            if response.status == ResponseStatus.SUCCESS and response.data:
                return response.data
            else:
                logger.error(
                    f"Ошибка получения колонок для таблицы {table_name}: {response.error}"
                )
                return None

        except Exception as e:
            logger.error(
                f"Исключение при получении колонок для таблицы {table_name}: {e}"
            )
            return None

    def _on_filter_value_changed(self, column_name: str, value: Any):
        """Обработчик изменения значения фильтра"""
        logger.debug(f"Фильтр {column_name} изменен на: {value}")
        # Здесь можно добавить логику для реакции на изменения фильтров
        # Например, автоматическое обновление данных в таблице

    def clear_filters(self):
        """Очищает все фильтры"""
        # Удаляем все виджеты из layout
        layout: VLayout | HLayout = self.filters_container.layout
        while layout.count():
            child: QLayoutItem = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Очищаем словарь
        self.filter_widgets.clear()

    def get_filters(self) -> Dict[str, Any]:
        """
        Возвращает текущие значения фильтров в виде {column_name: value}
        Возвращает только непустые фильтры
        """
        result = {}

        for col_name, filter_widget in self.filter_widgets.items():
            if not filter_widget.is_empty():
                value = filter_widget.get_filter_value()
                if value is not None:
                    result[col_name] = value

        return result

    def get_selected_table(self) -> str:
        """Возвращает имя выбранной таблицы"""
        return self.table_combo.currentText()

    def set_filter_value(self, column_name: str, value: Any, display_text: str = "") -> None:
        """Программно устанавливает значение фильтра"""
        if column_name in self.filter_widgets:
            filter_widget: BaseFilterWidget = self.filter_widgets[column_name]

            # Если передан display_text, обновляем метку
            if display_text:
                filter_widget.label.setText(display_text + ":")

            set_filter_value(filter_widget, value)
