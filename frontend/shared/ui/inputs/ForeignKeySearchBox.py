from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QLineEdit
from frontend.shared.ui.inputs import AutoComplete, ComboBox
from backend.repository import DatabaseRepository

class ForeignKeySearchBox(ComboBox):
    """Pure UI component for foreign key search - handles only UI and search logic"""

    # Add a signal for when selection changes
    selection_changed = Signal(object)

    def __init__(self, column_name: str, column_info: dict, parent=None):
        super().__init__()
        self.setParent(parent)
        self.column_name = column_name
        self.column_info = column_info

        # Extract foreign key info from column metadata
        self._extract_foreign_key_info()
        self.selected_id = None
        self.repository = DatabaseRepository()

        self._setup_ui()
        self._setup_connections()

    def _extract_foreign_key_info(self):
        """Extract foreign key information from column metadata"""
        foreign_keys = self.column_info.get("foreign_keys", [])
        if not foreign_keys:
            raise ValueError(f"No foreign key info for column {self.column_name}")

        fk_info = foreign_keys[0]
        self.target_table = fk_info.get("target_table", "")
        self.display_column = fk_info.get("display_column", "name")
        self.id_column = fk_info.get("id_column", "id")

    def _setup_ui(self):
        """Setup UI components"""
        self.setLineEdit(QLineEdit())
        self.lineEdit().setPlaceholderText("Поиск...") # type: ignore
        self.setEditable(True)
        self.setInsertPolicy(ComboBox.InsertPolicy.NoInsert)
        self.setCompleter(AutoComplete())

    def _setup_connections(self):
        """Setup signal connections"""
        self.editTextChanged.connect(self.debounce)
        self.currentIndexChanged.connect(self._on_selection_changed)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._perform_search)

    def debounce(self, text: str):
        """Debounce search requests"""
        self.timer.start(300)

    def _perform_search(self):
        """Perform search based on current text"""
        text = self.currentText().strip()
        if len(text) < 2:
            return

        try:
            results = self.repository.search_foreign_key(
                table=self.target_table,
                display_col=self.display_column,
                id_col=self.id_column,
                query=text,
                limit=30,
            )

            if results.data:
                self.blockSignals(True)
                self.clear()
                for item in results.data:
                    display_text = str(item.get(self.display_column, ""))
                    item_id = item.get(self.id_column)
                    self.addItem(display_text, userData=item_id)
                self.blockSignals(False)

        except Exception as e:
            print(f"Error fetching suggestions: {e}")
            self.clear()

    def on_focus(self):
        """Load initial suggestions when focused"""
        try:
            results = self.repository.search_foreign_key(
                table=self.target_table,
                display_col=self.display_column,
                id_col=self.id_column,
                query="",
                limit=10,
            )

            if results.data:
                self.blockSignals(True)
                self.clear()
                for item in results.data:
                    display_text = str(item.get(self.display_column, ""))
                    item_id = item.get(self.id_column)
                    self.addItem(display_text, userData=item_id)
                self.blockSignals(False)

        except Exception as e:
            print(f"Error loading initial suggestions: {e}")

    def _on_selection_changed(self, index: int):
        """Handle selection change"""
        if index >= 0:
            self.selected_id = self.itemData(index)
        else:
            self.selected_id = None

        # Emit signal for external components to listen to
        self.selection_changed.emit(self.selected_id)

    def get_filter_value(self):
        """Get current selected ID"""
        return self.selected_id

    def set_selected_value(self, value_id, display_text: str = ""):
        """Programmatically set selected value"""
        if value_id is None:
            self.clear()
            self.selected_id = None
            return

        # Try to find existing item
        index = -1
        for i in range(self.count()):
            if self.itemData(i) == value_id:
                index = i
                break

        if index >= 0:
            self.setCurrentIndex(index)
            self.selected_id = value_id
        else:
            # Item not in current list, add it
            if not display_text:
                # Fetch display text from database
                try:
                    response = self.repository.get_table_data(
                        table_name=self.target_table,
                        columns_list=[self.id_column, self.display_column],
                        filters_dict={self.id_column: value_id},
                        limit=1
                    )
                    if response.data:
                        display_text = str(response.data[0].get(self.display_column, value_id))
                    else:
                        display_text = str(value_id)
                except Exception:
                    display_text = str(value_id)

            self.addItem(display_text, userData=value_id)
            self.setCurrentIndex(self.count() - 1)
            self.selected_id = value_id