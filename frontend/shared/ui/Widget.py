from PySide6.QtWidgets import QWidget
from frontend.shared.ui import HLayout, VLayout

class Widget(QWidget):
    def __init__(self, layout: HLayout | VLayout | None = None):
        super().__init__()
        self._layout = None  # Переместили сюда!
        
        if layout is not None:
            self._layout = layout
            self.setLayout(self._layout)

    def add_children(self, children: list[QWidget]):
        if self._layout is not None:
            self._layout.add_children(children)
        else:
            print(
                "[Warning] You tried to interact with a QWidget that doesn't have a layout."
            )

    def clean(self):
        if self._layout is not None:
            self._layout.clean()
        else:
            print(
                "[Warning] You tried to interact with a QWidget that doesn't have a layout."
            )