from frontend.shared.ui.inputs import ComboBox


class EnumInput(ComboBox):
    """Для ENUM полей"""

    def __init__(self, enum_values):
        super().__init__()
        self.enum_values = enum_values

    def get_value(self) -> str:
        return self.currentText()

    def is_value_valid(self) -> bool:
        if self.currentText() not in self.enum_values:
            return False
        return True

    def clear_value(self):
        self.setCurrentIndex(0)  # Выбираем пустой элемент