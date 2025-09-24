from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLayout

Children = list[QWidget]


def add_children(layout: QLayout, children: Children):
    for child in children:
        layout.addWidget(child)


def clean(layout: QLayout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()


class VLayout(QVBoxLayout):

    def __init__(
        self, children: Children | None = None, gap_px: int = 10, alignment=None
    ):
        super().__init__()

        self.setSpacing(gap_px)
        if alignment:
            self.setAlignment(alignment)
        if children:
            self.add_children(children)

    def add_children(self, children: Children):
        add_children(self, children)

    def clean(self):
        clean(self)


class HLayout(QHBoxLayout):

    def __init__(
        self, children: Children | None = None, gap_px: int = 10, alignment=None
    ):
        super().__init__()

        self.setSpacing(gap_px)
        if alignment:
            self.setAlignment(alignment)
        if children:
            self.add_children(children)

    def add_children(self, children: Children):
        add_children(self, children)

    def clean(self):
        clean(self)


class GridLayout(QGridLayout):

    def __init__(
        self, children: Children | None = None, gap_px: int = 10, alignment=None
    ):
        super().__init__()

        self.setSpacing(gap_px)
        if alignment:
            self.setAlignment(alignment)
        if children:
            self.add_children(children)

    def add_children(self, children: Children):
        add_children(self, children)

    def clean(self):
        clean(self)
