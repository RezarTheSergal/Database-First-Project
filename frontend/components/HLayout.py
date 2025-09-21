from PySide6.QtWidgets import QHBoxLayout, QWidget


class HLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()

    def add_children(self, children: list[QWidget]):
        for child in children:
            self.addWidget(child)
