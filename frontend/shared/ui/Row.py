from .StringInput import StringInput
from .BoolInput import BoolEdit
from .IntInput import IntInput
from .DateInput import DateInput
from .FloatInput import FloatInput
from .Widget import Widget
from .Layouts import HLayout
from .Text import Text
from .Font import Font
from ..lib.utils import setClass

font = Font(12)


def isIntType(type: str) -> bool:
    return type == "INTEGER" or "NUMERIC" in type


def return_element_by_type(type: str, *args, **kwargs):
    if isIntType(type):
        return IntInput(*args, **kwargs)

    match (type):
        case "TEXT":
            return StringInput(*args, **kwargs)
        case "FLOAT":
            return FloatInput(*args, **kwargs)
        case "BOOL" | "BOOLEAN":
            return BoolEdit(*args, **kwargs)
        case "DATE":
            return DateInput(*args, **kwargs)
        case _:
            return StringInput(*args, **kwargs)


class Row(Widget):
    _layout = HLayout()

    def __init__(self, en_label: str, ru_label: str, type: str, placeholder: str = ""):
        super().__init__()
        self.en_label = en_label
        self.ru_label = ru_label
        self.setLayout(self._layout)

        setClass(self, "row")
        self.label = Text(ru_label, font=font)
        self.input = return_element_by_type(type, placeholder)

        self.add_children([self.label, self.input])

    def get_label(self, locale: str) -> str:
        if locale == "en":
            return self.en_label
        elif locale == "ru":
            return self.ru_label
        else:
            return self.en_label

    def get_input_value(self):
        return self.input.get_value()
