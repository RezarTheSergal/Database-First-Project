from typing import Any, Dict, Optional
from backend.utils.responce_types import ResponseStatus
from frontend.shared.ui import VLayout, Widget, HLayout
from frontend.shared.ui.inputs.ComboBox import ComboBox
from backend.repository import DatabaseRepository
from frontend.shared.ui.filters.factory import FilterWidgetFactory
from frontend.shared.ui.filters.base import BaseFilterWidget
import logging

logger = logging.getLogger()
database = DatabaseRepository()


class FilterBlockClass(Widget):
    def __init__(self, initial_tables=None):
        super().__init__(HLayout())

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
        self.clear_filters()

        if not table_name:
            return

        columns_info = self._get_columns_info(table_name)
        if not columns_info:
            logger.warning(f"Не удалось получить информацию о колонках для таблицы {table_name}")
            return

        # Создаем фильтры для каждой колонки
        for col_name, col_meta in columns_info.items():
            try:
                filter_widget = FilterWidgetFactory.create_filter_widget(col_name, col_meta)

                if filter_widget:
                    self.filter_widgets[col_name] = filter_widget
                    self.filters_container.layout.addWidget(filter_widget)

                    # Подключаем сигналы если нужно
                    if hasattr(filter_widget, 'value_changed'):
                        filter_widget.value_changed.connect(
                            lambda value, col=col_name: self._on_filter_value_changed(col, value)
                        )

            except Exception as e:
                logger.error(f"Ошибка создания фильтра для колонки {col_name}: {e}")

    def _get_columns_info(self, table_name: str) -> Optional[Dict[str, dict]]:
        """Получает информацию о колонках таблицы"""
        try:
            response = database.get_table_columns(table_name)

            if response.status == ResponseStatus.SUCCESS and response.data:
                return response.data
            else:
                logger.error(f"Ошибка получения колонок для таблицы {table_name}: {response.error}")
                return None

        except Exception as e:
            logger.error(f"Исключение при получении колонок для таблицы {table_name}: {e}")
            return None

    def _on_filter_value_changed(self, column_name: str, value: Any):
        """Обработчик изменения значения фильтра"""
        logger.debug(f"Фильтр {column_name} изменен на: {value}")
        # Здесь можно добавить логику для реакции на изменения фильтров
        # Например, автоматическое обновление данных в таблице

    def clear_filters(self):
        """Очищает все фильтры"""
        # Удаляем все виджеты из layout
        layout = self.filters_container.layout

        while layout.count():
            child = layout.takeAt(0)
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
                if value is not None or value != "" or value != "--не выбрано--" :
                    result[col_name] = value

        return result

    def get_selected_table(self) -> str:
        """Возвращает имя выбранной таблицы"""
        return self.table_combo.currentText()

    def set_filter_value(self, column_name: str, value: Any, display_text: str = ""):
        """Программно устанавливает значение фильтра"""
        if column_name in self.filter_widgets:
            filter_widget = self.filter_widgets[column_name]

            # Для FK фильтров передаем дополнительную информацию
            if hasattr(filter_widget, 'set_value'):
                filter_widget.set_value(value, display_text)
            else:
                # Для простых фильтров (пока не реализовано)
                pass

    def reset_filters(self):
        """Сбрасывает все фильтры в начальное состояние"""
        for filter_widget in self.filter_widgets.values():
            filter_widget.clear_value()
