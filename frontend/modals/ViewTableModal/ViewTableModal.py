from .Table import Table
from .TableControlPanel import TableControlPanel
from frontend.shared.ui import Modal, Size, VLayout


class ViewTableModal(Modal):
    def __init__(self):
        super().__init__(title="Просмотр таблиц", max_size=Size(800, 600), x=200)
        self.setLayout(VLayout())
        self.add(TableControlPanel())
        self.add(Table())
