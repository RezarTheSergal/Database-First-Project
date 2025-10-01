from PySide6.QtCore import QTimer
from typing import Any


class Timer(QTimer):
    def __init__(
        self,
        is_singleshot: bool = False,
        on_timeout: Any = None,
    ):
        super().__init__()
        self.setSingleShot(is_singleshot)
        if on_timeout != None:
            self.timeout.connect(on_timeout)
