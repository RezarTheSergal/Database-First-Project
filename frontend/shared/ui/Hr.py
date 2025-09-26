from ..lib.utils import setClass
from .Widget import Widget
from .Size import Size
from .Layouts import HLayout

class Hr(Widget):
    def __init__(self):
        super().__init__(HLayout())
        self.setFixedSize(Size(100, 10))
        setClass(self, "hr")
