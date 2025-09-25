from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLayout

Children = list[QWidget]


def add_children(layout: QLayout, children: Children):
    for child in children:
        layout.addWidget(child)


def clean(layout: QLayout):
    if layout is not None:
        for i in reversed(range(layout.count())):
            child = layout.takeAt(i)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clean(child.layout())  # Clear nested layout


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
