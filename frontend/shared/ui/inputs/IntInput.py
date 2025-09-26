from PySide6.QtWidgets import QDoubleSpinBox
from backend.utils.logger import logging

logger = logging.getLogger()


class IntInput(QDoubleSpinBox):

    def __init__(self, min: float = -(10.0**10), max: float = 10.0**10, **kwargs):
        super().__init__()
        if range:
            self.setRange(min, max)

    def get_value(self) -> int:
        if "," in self.text():
            logger.warning(
                "Given value is not an integer, but a double. Forcing cast to integer."
            )
        return int(
            self.text().split(",")[0]
        )  # Replacing comma with dot to prevent conversion errors for int() type
