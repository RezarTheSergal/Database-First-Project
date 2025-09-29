from PySide6.QtGui import QFont
from ..const import DEFAULT_FONT_FAMILY


class Font(QFont):

    def __init__(
        self,
        point_size_px=12,
        isBold=False,
        isItalic=False,
        hasKerning=False,
        isUnderlined=False,
        family=DEFAULT_FONT_FAMILY,
    ):
        super().__init__()

        self.setPointSize(point_size_px)
        self.setBold(isBold)
        self.setItalic(isItalic)
        self.setKerning(hasKerning)
        self.setUnderline(isUnderlined)
        self.setFamily(family)
