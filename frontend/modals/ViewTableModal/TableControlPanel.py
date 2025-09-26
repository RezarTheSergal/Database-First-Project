from collections import defaultdict
from os import getcwd
from typing import Dict, List
from PySide6.QtWidgets import QWidget
from backend.repository import DatabaseRepository
from frontend.shared.ui import HLayout, PushButton, Icon, PushButton, Row, Widget, VLayout, HLayout
from frontend.shared.ui.ComboBox import ComboBoxClass
from frontend.shared.ui.FilterBlock import FilterBlockClass
import logging
from frontend.shared.lib import translate

logger = logging.getLogger()
database = DatabaseRepository()

class TableControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.blocks: List[FilterBlockClass] = []  # список FilterBlock

        table_names = database.get_tablenames().data or []

        main_layout = VLayout()
        self.setLayout(main_layout)

        self.blocks_container = Widget(VLayout())
        main_layout.addWidget(self.blocks_container)

        self.add_button = PushButton(text="➕", callback=self._add_filter_block)
        main_layout.addWidget(self.add_button)

        self._add_filter_block(initial_tables=table_names)

    def _add_filter_block(self, initial_tables=None):
        block = FilterBlockClass(initial_tables=initial_tables)
        self.blocks.append(block)
        self.blocks_container.layout().addWidget(block)

    def get_all_filters(self) -> dict:
        """Возвращает все фильтры в виде {table_name: {col: value, ...}, ...}"""
        result = defaultdict(dict)
        for block in self.blocks:
            table = block.get_selected_table()
            if table:
                filters = block.get_filters()
                if filters:
                    result[table].update(filters)
        return dict(result)
        

