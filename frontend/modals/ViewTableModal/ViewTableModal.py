from .ui.TableControlPanel import TableControlPanel
from frontend.shared.ui import Modal, Size


class ViewTableModal(Modal):

    def __init__(self, parent):
        super().__init__(parent, title="Просмотр таблиц")
        self.setMinimumSize(Size(1000, 700))
        self.layout.add_children([TableControlPanel()])
