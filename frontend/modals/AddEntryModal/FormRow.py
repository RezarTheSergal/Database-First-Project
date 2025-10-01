from frontend.shared.lib.i18n.i18n import translate
from frontend.shared.ui import Widget, HLayout, Text, Font
from frontend.shared.lib.utils import setClass

font = Font(12)


class FormRow(Widget):
    label: Text
    _layout = HLayout()

    def __init__(self, input, en_label: str):
        super().__init__(HLayout())
        self.en_label = en_label
        self.ru_label = translate(en_label)
        self.setLayout(self._layout)

        setClass(self, "row")
        self.label = Text(self.get_label("ru"), font=font)
        self.input = input

        self.layout.set_children([self.label, self.input])

    def get_label(self, locale: str) -> str:
        if locale == "en":
            return self.en_label
        elif locale == "ru":
            return self.ru_label
        else:
            return self.en_label

    def get_input_value(self):
        return self.input.get_value()
