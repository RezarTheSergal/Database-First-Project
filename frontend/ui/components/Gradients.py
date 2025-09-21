from PySide6.QtGui import QLinearGradient, QRadialGradient
from . import Point


class LinearGradient(QLinearGradient):
    def __init__(self, p1: Point, p2: Point):
        super().__init__(p1, p2)


class RadialGradient(QRadialGradient):
    def __init__(self, p: Point, radius: int):
        super().__init__(p, radius)
