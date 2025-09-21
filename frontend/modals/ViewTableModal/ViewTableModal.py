from .Table import Table
from frontend.shared.ui import Modal, Size


class ViewTableModal(Modal):
    def __init__(self):
        super().__init__(title="Просмотр таблиц", max_size=Size(1000, 800))

        table = Table()
        self.add(table)
