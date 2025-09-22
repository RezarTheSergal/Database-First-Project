from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLayout

Children = list[QWidget]


def add_children(layout: QLayout, children: Children):
    for child in children:
        layout.addWidget(child)


class VLayout(QVBoxLayout):
    def __init__(self, children: Children | None = None, gap_px: int = 10):
        super().__init__()
        self.setSpacing(gap_px)
        if children:
            add_children(self, children)

    def add_children(self, children: Children):
        add_children(self, children)


class HLayout(QHBoxLayout):
    def __init__(self, children: Children | None = None, gap_px: int = 10):
        super().__init__()
        self.setSpacing(gap_px)
        if children:
            add_children(self, children)

    def add_children(self, children: Children):
        add_children(self, children)


class GridLayout(QGridLayout):
    def __init__(self, children: Children | None = None, gap_px: int = 10):
        super().__init__()
        self.setSpacing(gap_px)
        if children:
            add_children(self, children)

    def add_children(self, children: Children):
        add_children(self, children)
