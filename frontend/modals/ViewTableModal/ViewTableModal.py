from .TableControlPanel import TableControlPanel
from frontend.shared.ui import Modal, Size, VLayout


class ViewTableModal(Modal):

    def __init__(self, parent):
        super().__init__(parent, title="Просмотр таблиц", max_size=Size(1800, 900))
        self.add_children([TableControlPanel()])
