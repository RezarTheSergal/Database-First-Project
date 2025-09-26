from .inputs.StringInput import StringInput
from .inputs.BoolInput import BoolEdit
from .inputs.IntInput import IntInput
from .inputs.DateInput import DateInput
from .inputs.FloatInput import FloatInput
from .Widget import Widget
from .Layouts import HLayout
from .text.Text import Text
from .text.Font import Font
from ..lib.utils import setClass

font = Font(12)


def isIntType(type: str) -> bool:
    return type == "INTEGER" or "NUMERIC" in type


def return_element_by_type(type: str, **kwargs):
    if isIntType(type):
        return IntInput(**kwargs)

    match (type):
        case "TEXT":
            return StringInput(**kwargs)
        case "FLOAT" | "DOUBLE":
            return FloatInput(**kwargs)
        case "BOOL" | "BOOLEAN":
            return BoolEdit(**kwargs)
        case "DATE":
            return DateInput(**kwargs)
        case _:
            return StringInput(**kwargs)


class Row(Widget):
    _layout = HLayout()

    def __init__(
        self,
        en_label: str,
        ru_label: str,
        type: str,
        placeholder: str = "",
        allowed_values: list | None = None,
    ):
        super().__init__(HLayout())
        self.en_label = en_label
        self.ru_label = ru_label
        self.setLayout(self._layout)

        setClass(self, "row")
        self.label = Text(ru_label, font=font)
        self.input = return_element_by_type(
            type=type, placeholder=placeholder, allowed_values=allowed_values
        )

        self.set_children([self.label, self.input])

    def get_label(self, locale: str) -> str:
        if locale == "en":
            return self.en_label
        elif locale == "ru":
            return self.ru_label
        else:
            return self.en_label

    def get_input_value(self):
        return self.input.get_value()
