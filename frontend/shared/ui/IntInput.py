from PySide6.QtWidgets import QDoubleSpinBox


class IntInput(QDoubleSpinBox):
    def __init__(self, placeholder: str, min: int = -(10**10), max: int = 10**10):
        super().__init__()
        if range:
            self.setRange(min, max)

    def get_value(self) -> int:
        return int(
            self.text().split(",")[0]
        )