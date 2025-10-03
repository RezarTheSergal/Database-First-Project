from collections import defaultdict
from typing import List, Dict, Any
from PySide6.QtWidgets import QLayoutItem, QScrollArea, QWidget
from PySide6.QtCore import Qt
from backend.utils.responce_types import DatabaseResponse, ResponseStatus
from frontend.modals.ViewTableModal.ui.DynamicTable import DynamicTable
from frontend.shared.ui import PushButton, Widget, VLayout, HLayout
from frontend.shared.ui.filters import FilterBlockWidget
from backend.database.models import Base
from frontend.shared.utils.DatabaseMiddleware import DatabaseMiddleware
from frontend.shared.utils.MessageFactory import MessageFactory
import logging

logger = logging.getLogger(__name__)


class TableControlPanel(Widget):
    """Панель управления фильтрами для таблиц с поддержкой множественных блоков"""

    def __init__(self) -> None:
        super().__init__(VLayout())
        self.blocks: List[FilterBlockWidget] = []
        self.table_names = []

        self._setup_ui()
        self._load_table_names()
        self._add_initial_filter_block()

    def _setup_ui(self) -> None:
        """Настройка пользовательского интерфейса"""
        # Заголовок
        title_layout = HLayout()

        # Кнопки управления
        self.add_button = PushButton(
            text="+ Добавить фильтр", callback=self._add_filter_block
        )
        self.clear_button = PushButton(
            text="X Очистить все", callback=self._clear_all_filters
        )
        self.apply_button = PushButton(
            text="o Применить фильтры", callback=self._apply_filters
        )

        title_layout.addWidget(self.add_button)
        title_layout.addWidget(self.clear_button)
        title_layout.addWidget(self.apply_button)
        title_layout.addStretch()

        self.layout.addLayout(title_layout)

        # Контейнер со скроллом для блоков фильтров
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.blocks_container = Widget(VLayout())
        scroll_area.setWidget(self.blocks_container)

        self.layout.addWidget(scroll_area)

        self.table_widget = DynamicTable()
        self.table_widget.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.table_widget.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.layout.addWidget(self.table_widget)

    def _load_table_names(self):
        """Загружает список имен таблиц из БД"""
        response = DatabaseMiddleware.get_table_names()
        MessageFactory.show(response, True)
        if response and response.status == ResponseStatus.SUCCESS and response.data:
            self.table_names = response.data
            logger.info(f"Загружено {len(self.table_names)} таблиц")
        else:
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message=f"Ошибка загрузки таблиц: {response.error}",  # type: ignore
                ),
            )
            logger.error(f"Ошибка загрузки таблиц: {response.error}")  # type: ignore
            self.table_names = []

    def _add_initial_filter_block(self):
        """Добавляет первоначальный блок фильтров"""
        if self.table_names:
            self._add_filter_block()

    def _add_filter_block(self):
        """Добавляет новый блок фильтров"""
        try:
            block = FilterBlockWidget(initial_tables=self.table_names)

            # Создаем контейнер для блока с кнопкой удаления
            block_container = Widget(HLayout())

            # Добавляем блок
            block_container.layout.addWidget(block)

            # Кнопка удаления (показывается только если блоков больше одного)
            if len(self.blocks) > 0:  # Если это не первый блок
                remove_button = PushButton(
                    text="❌",
                    callback=lambda: self._remove_filter_block(block, block_container),
                )
                remove_button.setMaximumWidth(30)
                block_container.layout.addWidget(remove_button)

            # Добавляем в список и в UI
            self.blocks.append(block)
            self.blocks_container.layout.addWidget(block_container)

            logger.info(f"Добавлен блок фильтров #{len(self.blocks)}")

        except Exception as e:
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message=f"Ошибка добавления блока фильтров: {e}",
                ),
            )
            logger.error(f"Ошибка добавления блока фильтров: {e}")

    def _remove_filter_block(self, block: FilterBlockWidget, container: QWidget):
        """Удаляет блок фильтров"""
        try:
            # Удаляем из списка
            if block in self.blocks:
                self.blocks.remove(block)

            # Удаляем из UI
            self.blocks_container.layout.removeWidget(container)
            container.deleteLater()

            logger.info(f"Удален блок фильтров, осталось {len(self.blocks)}")

            # Обновляем фильтры после удаления
            self._apply_filters()

        except Exception as e:
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message=f"Ошибка удаления блока фильтров: {e}",
                ),
            )
            logger.error(f"Ошибка удаления блока фильтров: {e}")

    def _clear_all_filters(self):
        """Очищает все фильтры во всех блоках"""
        try:
            for block in self.blocks:
                block.reset_filters()

            logger.info("Все фильтры очищены")
            self._apply_filters()

        except Exception as e:
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR, message=f"Ошибка очистки фильтров: {e}"
                ),
            )
            logger.error(f"Ошибка очистки фильтров: {e}")

    def get_selected_table(self) -> str:
        return self.blocks[0].get_selected_table()

    def _apply_filters(self):
        """Применяет текущие фильтры и отправляет сигнал"""
        try:
            filters: Dict[str, Dict[str, Any]] = self.get_all_filters()
            table_name: str = self.get_selected_table()

            model_response = DatabaseMiddleware().get_table_schema(table_name)
            if not model_response or model_response.data is None:
                return

            model: type[Base] = model_response.data
            table_data_response = DatabaseMiddleware.get_where(table_name, filters)
            if not table_data_response or table_data_response.data is None or MessageFactory.show(
                table_data_response, True
            ):
                logger.error(
                    f"Ошибка получения данных таблицы: {table_data_response.error}"
                )
                return

            data = table_data_response.data

            self.table_widget.set_model(model)
            self.table_widget.load_data([data])
            logger.info(f"Применены фильтры: {filters}")

        except Exception as e:
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message=f"Ошибка применения фильтров: {e}",
                ),
            )
            logger.error(f"Ошибка применения фильтров: {e}")

    def get_all_filters(self) -> Dict[str, Dict[str, Any]]:
        """
        Возвращает все фильтры в виде {table_name: {col: value, ...}, ...}
        Объединяет фильтры для одинаковых таблиц из разных блоков
        """
        result = defaultdict(dict)

        for block in self.blocks:
            table = block.get_selected_table()
            if table:
                filters = block.get_filters()
                if filters:  # Только если есть непустые фильтры
                    # Объединяем фильтры для одной таблицы
                    result[table].update(filters)

        return dict(result)

    def set_filters(self, filters_dict: Dict[str, Dict[str, Any]]):
        """
        Программно устанавливает фильтры
        filters_dict: {table_name: {column_name: value, ...}, ...}
        """
        try:
            # Очищаем текущие блоки (кроме первого)
            while len(self.blocks) > 1:
                last_block: FilterBlockWidget = self.blocks[-1]
                # Найдем контейнер для этого блока и удалим
                for i in range(self.blocks_container.layout.count()):
                    item: QLayoutItem = self.blocks_container.layout.itemAt(i)
                    if item and item.widget():
                        container: QWidget = item.widget()

                        # Проверяем, содержит ли контейнер наш блок
                        for j in range(
                            container.layout().count()
                            if hasattr(container, "layout")
                            else 0
                        ):
                            child_item = container.layout().itemAt(j)
                            if child_item and child_item.widget() == last_block:
                                self._remove_filter_block(last_block, container)
                                break

            # Настраиваем фильтры
            block_index = 0
            for table_name, table_filters in filters_dict.items():
                # Создаем новый блок если нужен
                if block_index >= len(self.blocks):
                    self._add_filter_block()

                current_block = self.blocks[block_index]

                # Устанавливаем таблицу
                current_block.table_combo.setCurrentText(table_name)
                current_block._on_table_changed(
                    table_name
                )  # Принудительно обновляем фильтры

                # Устанавливаем значения фильтров
                for col_name, value in table_filters.items():
                    current_block.set_filter_value(col_name, value)

                block_index += 1

            logger.info(f"Установлены фильтры: {filters_dict}")

        except Exception as e:
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message=f"Ошибка установки фильтров: {e}",
                ),
            )
            logger.error(f"Ошибка установки фильтров: {e}")

    def get_active_tables(self) -> List[str]:
        """Возвращает список активных таблиц (с установленными фильтрами)"""
        return list(self.get_all_filters().keys())

    def has_active_filters(self) -> bool:
        """Проверяет, есть ли активные фильтры"""
        return bool(self.get_all_filters())
