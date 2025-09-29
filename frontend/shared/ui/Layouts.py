from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLayout

Children = list[QWidget]

def add_children(layout: QLayout, children: Children):
    for child in children:
        layout.addWidget(child)

def clean(layout: QLayout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                widget = child.widget()
                widget.setParent(None)
                widget.deleteLater()
            elif child.layout() is not None:
                clean(child.layout())
                child.layout().setParent(None)
                child.layout().deleteLater()

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
        self, children: Children | None = None, gap_px: int = 10, alignment=None, columns: int = 2
    ):
        super().__init__()
        self.setSpacing(gap_px)
        self.columns = columns
        if alignment:
            self.setAlignment(alignment)
        if children:
            self.add_children(children)

    def add_children(self, children: Children):
        # Добавляем виджеты в сетку по позициям
        for i, child in enumerate(children):
            row = i // self.columns
            col = i % self.columns
            self.addWidget(child, row, col)

    def clean(self):
        clean(self)