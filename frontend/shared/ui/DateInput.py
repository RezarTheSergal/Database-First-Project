from PySide6.QtWidgets import QDateEdit


class DateInput(QDateEdit):
    def __init__(self, placeholder: str = ""):
        super().__init__()

    def get_value(self) -> str:
         return self.date().toString("yyyy-MM-dd") #возвращаем сразу правильный формат для обработки бд
