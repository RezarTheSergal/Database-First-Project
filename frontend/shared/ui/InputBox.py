from PySide6.QtWidgets import QTextEdit


class InputBox(QTextEdit):
    def __init__(self, placeholder: str = "") -> None:
        super().__init__(
            undoRedoEnabled=True, readOnly=False, placeholderText=placeholder
        )
        self.setMaximumHeight(30)
