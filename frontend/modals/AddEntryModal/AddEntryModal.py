from frontend.shared.ui import Modal, Size
from .AddEntryForm import AddEntryForm


class AddEntryModal(Modal):
    def __init__(self):
        super().__init__(title="Добавление данных", x=1400)

        self.setMinimumSize(Size(1000, 500))
        self.setMaximumSize(Size(2000, 1000))

        self.add_children([AddEntryForm()])
