from PySide6.QtWidgets import QLineEdit
from .GenericInput import GenericInput


class StringInput(GenericInput, QLineEdit):
    def __init__(
        self, allowed_values: list[str] | None = None, *args, **kwargs
    ) -> None:
        super().__init__()
        self.setMaximumHeight(30)
        if allowed_values is not None:
            self.set_allowed_values(allowed_values)

    def get_value(self) -> str:
        return self.text()
