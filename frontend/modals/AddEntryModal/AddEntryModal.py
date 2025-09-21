from frontend.shared.ui import Modal
from .AddEntryForm import AddEntryForm


class AddEntryModal(Modal):
    def __init__(self):
        super().__init__(title="Добавление данных")
        self.add(AddEntryForm())
