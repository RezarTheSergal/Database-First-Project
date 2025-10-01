from PySide6.QtCore import QDate
from backend.utils.logger import logging

logger = logging.getLogger("frontend-inputs")


class Date(QDate):
    year: int
    month: int
    day: int

    def __init__(self, year: int, month: int, day: int):
        super().__init__()
        self.setDate(year, month, day)
        self.year = year
        self.month = month
        self.day = day

    def set_year(self, year: int):
        if year > 0:
            self.setDate(year, self.month, self.day)
        else:
            logger.error(f"Incorrect year: {year}. Keeping {self.year}")

    def set_month(self, month: int):
        if 1 <= month <= 12:
            self.setDate(self.year, month, self.day)
        else:
            logger.error(f"Incorrect month: {month}. Keeping {self.month}")

    def set_day(self, day: int):
        if 1 <= day <= 31:
            self.setDate(self.year, self.month, day)
        else:
            logger.error(f"Incorrect day: {day}. Keeping {self.day}")
