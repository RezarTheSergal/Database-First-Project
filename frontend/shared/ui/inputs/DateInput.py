from PySide6.QtWidgets import QDateEdit
from .utils.DateTime import DateTime
from .utils.Date import Date
from .utils.Time import Time


class DateInput(QDateEdit):
    is_nullable: bool
    display_format: str

    def __init__(
        self,
        display_format: str = "yyyy-MM-dd",
        year: int = 2025,
        month: int = 1,
        day: int = 1,
    ):
        super().__init__()
        self.setCalendarPopup(True)
        self.setDisplayFormat("yyyy-MM-dd")
        self.setDateTime(DateTime(Date(year, month, day), Time()))

        self.display_format = display_format

    def get_value(self) -> str:
        return str(self.text())

    def is_value_valid(self) -> bool:
        return True  # Can't be invalid. Put here to prevent type errors
