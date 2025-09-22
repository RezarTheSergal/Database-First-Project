from frontend.shared.ui import Modal, Size
from .AddEntryForm import AddEntryForm


class AddEntryModal(Modal):
    def __init__(self):
        super().__init__(title="Добавление данных", max_size=Size(600, 1000), x=1400)
        self.setMinimumSize(Size(400, 200))
        self.add(AddEntryForm())
