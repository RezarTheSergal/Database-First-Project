from frontend.shared.ui import Modal, Size
from .AddEntryForm import AddEntryForm


class AddEntryModal(Modal):

    def __init__(self, parent):
        super().__init__(parent, title="Добавление данных")

        self.setMinimumSize(Size(600, 500))
        self.setMaximumSize(Size(2000, 1000))

        self.layout.add_children([AddEntryForm()])
