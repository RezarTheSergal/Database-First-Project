from typing import List, Dict, Any, Optional
from PySide6.QtCore import Signal
from backend.repository import DatabaseRepository
from frontend.shared.lib.i18n.i18n import translate
from frontend.shared.ui.inputs import ComboBox, AutoComplete
from backend.utils.responce_types import ResponseStatus
from .BaseFilterWidget import BaseFilterWidget
import logging

logger = logging.getLogger(__name__)
INPUT_CANDIDATES = [
    "name",
    "title",
    "label",
    "model",
    "type",
    "description",
]


class ForeignKeyFilterWidget(BaseFilterWidget):
    """Виджет фильтра для foreign key с поиском по вводу"""

    value_changed = Signal(object)  # Сигнал изменения значения
    target_table = None
    target_column = None
    display_column = None
    selected_id = None
    search_timer: Timer | None = None
    is_updating: bool = False  # Флаг для предотвращения рекурсии

    def __init__(self, column_name: str, column_info: Dict[str, Any], parent=None):

        # Извлекаем информацию о foreign key
        self._extract_foreign_key_info(column_info)
        self.en_locale = column_name
        self.ru_locale = translate(column_name)
        super().__init__(self.ru_locale, column_info, parent)

    def _extract_foreign_key_info(self, column_info: Dict[str, Any]):
        """Извлекает информацию о foreign key из метаданных колонки"""
        foreign_keys = column_info.get("foreign_keys", [])
        if not foreign_keys:
            raise ValueError(f"Column {self.column_name} is not a foreign key")

        fk = foreign_keys[0]  # Берем первый FK
        self.target_table = fk["target_table"]
        self.target_column = fk["target_column"]

        # Определяем колонку для отображения
        self.display_column = self._determine_display_column()

    def _determine_display_column(self) -> str:
        """Определяет наилучшую колонку для отображения значений"""
        display_column = self.target_column  # По умолчанию используем ID колонку

        try:
            columns_resp = DatabaseRepository.get_table_columns(self.target_table)
            if columns_resp.status == ResponseStatus.SUCCESS:
                cols = columns_resp.data
                # Ищем подходящие текстовые колонки
                for candidate in INPUT_CANDIDATES:
                    if candidate in cols:
                        col_type = (cols[candidate].get("type") or "").upper()
                        if any(
                            t in col_type for t in ("TEXT", "VARCHAR", "CHAR", "STRING")
                        ):
                            display_column = candidate
                            break
        except Exception as e:
            logger.warning(
                f"Не удалось определить display column для {self.target_table}: {e}"
            )

        return display_column

    def _create_input_widget(self) -> ComboBox:
        """Создает ComboBox для поиска foreign key"""
        combo = ComboBox()
        combo.setEditable(True)
        combo.setInsertPolicy(ComboBox.InsertPolicy.NoInsert)

        # КРИТИЧНО: отключаем автозаполнение
        combo.setCompleter(AutoComplete())
        # combo.lineEdit().setProperty("autocomplete", "off")

        # Настройка плейсхолдера
        # combo.lineEdit().setPlaceholderText(f"Поиск в {self.target_table}...")

        return combo

    def _setup_connections(self):
        """Настраивает соединения сигналов"""
        if not self.input_widget:
            logger.error("Нет инпута", self)
            return

        # Таймер для debounce поиска
        self.search_timer = Timer(is_singleshot=True, on_timeout=self._perform_search)

        # Соединения
        self.input_widget.editTextChanged.connect(self._on_text_changed)
        self.input_widget.currentIndexChanged.connect(self._on_selection_changed)
        self.input_widget.lineEdit().returnPressed.connect(self._on_enter_pressed)

    def _on_text_changed(self, text: str):
        """Обработчик изменения текста"""
        if self.is_updating or self.search_timer == None:
            return

        # Сбрасываем выбранный ID если текст изменился вручную
        if not self.is_updating:
            self.selected_id = None

        # Запускаем поиск с задержкой
        self.search_timer.stop()
        if len(text.strip()) >= 2:  # Минимум 2 символа для поиска
            self.search_timer.start(300)  # 300ms задержка
        else:
            self._clear_suggestions()

    def _on_selection_changed(self, index: int):
        """Обработчик изменения выбранного элемента"""
        if self.is_updating:
            return

        if index >= 0:
            self.selected_id = self.input_widget.itemData(index)
            self.value_changed.emit(self.selected_id)
        else:
            self.selected_id = None
            self.value_changed.emit(None)

    def _on_enter_pressed(self):
        """Обработчик нажатия Enter - выбирает первый элемент если он есть"""
        if self.input_widget.count() > 0:
            self.input_widget.setCurrentIndex(0)

    def _perform_search(self):
        """Выполняет поиск по введенному тексту"""
        query_text = self.input_widget.currentText().strip()
        if len(query_text) < 2:
            return

        try:
            response = DatabaseRepository.search_foreign_key(
                table=self.target_table,
                display_col=self.display_column,
                id_col=self.target_column,
                query=query_text,
                limit=30,
            )

            if response.status == ResponseStatus.SUCCESS:
                self._update_suggestions(response.data)
            else:
                logger.error(f"Ошибка поиска FK: {response.error}")
                self._clear_suggestions()

        except Exception as e:
            logger.error(f"Исключение при поиске FK: {e}")
            self._clear_suggestions()

    def _update_suggestions(self, suggestions: List[Dict[str, Any]]):
        """Обновляет список предложений"""
        if self.is_updating:
            return

        self.is_updating = True
        try:
            current_text = self.input_widget.currentText()

            # Очищаем и заполняем новыми данными
            self.input_widget.clear()

            for item in suggestions:
                display_text = str(item.get("display", ""))
                item_id = item.get("id")
                self.input_widget.addItem(display_text, userData=item_id)

            # Восстанавливаем введенный текст
            self.input_widget.setEditText(current_text)

            # Показываем выпадающий список если есть элементы
            if suggestions:
                self.input_widget.showPopup()

        finally:
            self.is_updating = False

    def _clear_suggestions(self):
        """Очищает список предложений"""
        if self.is_updating:
            return

        self.is_updating = True
        try:
            current_text = self.input_widget.currentText()
            self.input_widget.clear()
            self.input_widget.setEditText(current_text)
        finally:
            self.is_updating = False

    def get_filter_value(self) -> Optional[Any]:
        """Возвращает выбранный ID или None"""
        return self.selected_id

    def clear_value(self):
        """Очищает значение фильтра"""
        self.is_updating = True
        try:
            self.selected_id = None
            self.input_widget.clear()
            self.input_widget.setEditText("")
        finally:
            self.is_updating = False

    def set_value(self, value_id: Any, display_text: str = None):
        """Устанавливает значение фильтра программно"""
        self.is_updating = True
        try:
            self.selected_id = value_id

            if display_text:
                self.input_widget.clear()
                self.input_widget.addItem(display_text, userData=value_id)
                self.input_widget.setCurrentIndex(0)
            else:
                # Если нет display_text, пытаемся найти запись
                self._load_value_by_id(value_id)
        finally:
            self.is_updating = False

    def _load_value_by_id(self, value_id: Any):
        """Загружает запись по ID для отображения"""
        try:
            # Здесь можно добавить метод в DatabaseRepository для получения записи по ID
            # Пока просто показываем ID
            self.input_widget.clear()
            self.input_widget.addItem(str(value_id), userData=value_id)
            self.input_widget.setCurrentIndex(0)
        except Exception as e:
            logger.error(f"Ошибка загрузки значения по ID {value_id}: {e}")
