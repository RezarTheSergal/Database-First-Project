from PySide6.QtCore import QDateTime


class DateTime(QDateTime):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
