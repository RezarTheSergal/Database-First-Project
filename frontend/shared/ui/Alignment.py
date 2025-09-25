from enum import Enum
from PySide6.QtCore import Qt


class Alignment(Enum):
    Left = Qt.AlignmentFlag.AlignLeft
    Right = Qt.AlignmentFlag.AlignRight
    Center = Qt.AlignmentFlag.AlignCenter
    SpaceBetween = Qt.AlignmentFlag.AlignJustify
