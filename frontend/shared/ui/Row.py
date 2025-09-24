from .InputBox import InputBox
from .Widget import Widget
from .Layouts import HLayout
from .Text import Text
from .Font import Font
from ..lib.utils import setClass

font = Font(12)


class Row(Widget):
    _layout = HLayout()

    def __init__(self, en_label: str, ru_label: str, placeholder: str = ""):
        super().__init__()
        self.en_label = en_label
        self.ru_label = ru_label
        self.setLayout(self._layout)

        setClass(self, "row")
        self.label = Text(ru_label, font=font)
        self.input = InputBox(placeholder)

        self.add_children([self.label, self.input])

    def get_label(self, locale: str) -> str:
        if locale == "en":
            return self.en_label
        elif locale == "ru":
            return self.ru_label
        else:
            return self.en_label

    def get_input_value(self) -> str:
        return self.input.toPlainText()
