from ..lib.utils import setClass
from .Widget import Widget
from .Size import Size


class Hr(Widget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(Size(100, 10))
        setClass(self, "hr")
