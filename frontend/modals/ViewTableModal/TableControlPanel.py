from collections import defaultdict
from typing import List, Dict, Any
from PySide6.QtWidgets import QWidget, QScrollArea
from PySide6.QtCore import Signal, Qt
from backend.repository import DatabaseRepository
from backend.utils.responce_types import ResponseStatus
from frontend.shared.ui import PushButton, Widget, VLayout, HLayout
from frontend.shared.ui.FilterBlock import FilterBlockClass
import logging

logger = logging.getLogger()
database = DatabaseRepository()

class TableControlPanel(QWidget):
    """Панель управления фильтрами для таблиц с поддержкой множественных блоков"""
    
    # Сигналы для уведомления об изменениях
    filters_changed = Signal(dict)  # {table_name: {col: value, ...}, ...}
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocks: List[FilterBlockClass] = []
        self.table_names = []
        
        self._setup_ui()
        self._load_table_names()
        self._add_initial_filter_block()
    
    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_layout = VLayout()
        self.setLayout(main_layout)
        
        # Заголовок
        title_layout = HLayout()
        
        # Кнопки управления
        self.add_button = PushButton(
            text="➕ Добавить фильтр", 
            callback=self._add_filter_block
        )
        self.clear_button = PushButton(
            text="🗑️ Очистить все",
            callback=self._clear_all_filters
        )
        self.apply_button = PushButton(
            text="✅ Применить фильтры",
            callback=self._apply_filters
        )
        
        title_layout.addWidget(self.add_button)
        title_layout.addWidget(self.clear_button)
        title_layout.addWidget(self.apply_button)
        title_layout.addStretch()
        
        main_layout.addLayout(title_layout)
        
        # Скроллируемый контейнер для блоков фильтров
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        self.blocks_container = Widget(VLayout())
        scroll_area.setWidget(self.blocks_container)
        
        main_layout.addWidget(scroll_area)
    
    def _load_table_names(self):
        """Загружает список имен таблиц из БД"""
        try:
            response = database.get_tablenames()
            if response.status == ResponseStatus.SUCCESS and response.data:
                self.table_names = response.data
                logger.info(f"Загружено {len(self.table_names)} таблиц")
            else:
                logger.error(f"Ошибка загрузки таблиц: {response.error}")
                self.table_names = []
        except Exception as e:
            logger.error(f"Исключение при загрузке таблиц: {e}")
            self.table_names = []
    
    def _add_initial_filter_block(self):
        """Добавляет первоначальный блок фильтров"""
        if self.table_names:
            self._add_filter_block()
    
    def _add_filter_block(self):
        """Добавляет новый блок фильтров"""
        try:
            block = FilterBlockClass(initial_tables=self.table_names)
            
            # Создаем контейнер для блока с кнопкой удаления
            block_container = Widget(HLayout())
            
            # Добавляем блок
            block_container.layout().addWidget(block)
            
            # Кнопка удаления (показывается только если блоков больше одного)
            if len(self.blocks) > 0:  # Если это не первый блок
                remove_button = PushButton(
                    text="❌",
                    callback=lambda: self._remove_filter_block(block, block_container)
                )
                remove_button.setMaximumWidth(30)
                block_container.layout().addWidget(remove_button)
            
            # Добавляем в список и в UI
            self.blocks.append(block)
            self.blocks_container.layout().addWidget(block_container)
            
            logger.info(f"Добавлен блок фильтров #{len(self.blocks)}")
            
        except Exception as e:
            logger.error(f"Ошибка добавления блока фильтров: {e}")
    
    def _remove_filter_block(self, block: FilterBlockClass, container: QWidget):
        """Удаляет блок фильтров"""
        try:
            # Удаляем из списка
            if block in self.blocks:
                self.blocks.remove(block)
            
            # Удаляем из UI
            self.blocks_container.layout().removeWidget(container)
            container.deleteLater()
            
            logger.info(f"Удален блок фильтров, осталось {len(self.blocks)}")
            
            # Обновляем фильтры после удаления
            self._apply_filters()
            
        except Exception as e:
            logger.error(f"Ошибка удаления блока фильтров: {e}")
    
    def _clear_all_filters(self):
        """Очищает все фильтры во всех блоках"""
        try:
            for block in self.blocks:
                block.reset_filters()
            
            logger.info("Все фильтры очищены")
            self._apply_filters()
            
        except Exception as e:
            logger.error(f"Ошибка очистки фильтров: {e}")
    
    def _apply_filters(self):
        """Применяет текущие фильтры и отправляет сигнал"""
        try:
            filters = self.get_all_filters()
            self.filters_changed.emit(filters)
            logger.info(f"Применены фильтры: {filters}")
            
        except Exception as e:
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
                last_block = self.blocks[-1]
                # Найдем контейнер для этого блока и удалим
                for i in range(self.blocks_container.layout().count()):
                    item = self.blocks_container.layout().itemAt(i)
                    if item and item.widget():
                        container = item.widget()
                        # Проверяем, содержит ли контейнер наш блок
                        for j in range(container.layout().count() if hasattr(container, 'layout') else 0):
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
                current_block._on_table_changed(table_name)  # Принудительно обновляем фильтры
                
                # Устанавливаем значения фильтров
                for col_name, value in table_filters.items():
                    current_block.set_filter_value(col_name, value)
                
                block_index += 1
            
            logger.info(f"Установлены фильтры: {filters_dict}")
            
        except Exception as e:
            logger.error(f"Ошибка установки фильтров: {e}")
    
    def get_active_tables(self) -> List[str]:
        """Возвращает список активных таблиц (с установленными фильтрами)"""
        return list(self.get_all_filters().keys())
    
    def has_active_filters(self) -> bool:
        """Проверяет, есть ли активные фильтры"""
        return bool(self.get_all_filters())
