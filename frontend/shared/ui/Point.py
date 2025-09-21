from PySide6.QtCore import QPointF


class Point(QPointF):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
