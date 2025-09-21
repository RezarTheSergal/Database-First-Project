from PySide6.QtWidgets import QVBoxLayout, QWidget


class VLayout(QVBoxLayout):
    def __init__(self, children: list[QWidget] | None = None, gap_px: int = 10):
        super().__init__()
        self.setSpacing(gap_px)
        if children:
            self.add_children(children)

    def add_children(self, children: list[QWidget]):
        for child in children:
            self.addWidget(child)
