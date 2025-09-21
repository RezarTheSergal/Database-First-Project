from PySide6.QtWidgets import QTableWidget
from PySide6.QtCore import Qt
from .TableItem import TableItem

SortOrder = Qt.SortOrder
TableRow = list[TableItem]


class Table(QTableWidget):
    def __init__(self):
        super().__init__()
        self.set_size(5, 5)
        for _ in range(5):
            self.append_row([TableItem("1"), TableItem("2"), TableItem("3")])

    def get_last_row_index(self) -> int:
        return self.rowCount() - 1

    def set_size(self, row_count: int, col_count: int):
        self.setRowCount(row_count)
        self.setColumnCount(col_count)

    def add_row(self, row_index: int, entry: TableRow):
        if row_index >= 0 and row_index <= self.get_last_row_index():
            i = 0
            while i < len(entry):
                self.setItem(row_index, i, entry[i])
                i += 1

    def append_row(self, entry: TableRow):
        self.add_row(self.get_last_row_index(), entry)

    def remove_row(self, i: int):
        if i >= 0 and i <= self.get_last_row_index():
            self.removeRow(i)

    def remove_column(self, i: int):
        if i >= 0 and i <= self.columnCount() - 1:
            self.removeColumn(i)

    def sort_by_column(
        self, columnIndex: int, order: SortOrder = SortOrder.AscendingOrder
    ):
        self.sortByColumn(columnIndex, order)
