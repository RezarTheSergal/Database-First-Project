from PySide6.QtGui import QFont


class Font(QFont):
    def __init__(
        self,
        point_size_px=12,
        isBold=False,
        isItalic=False,
        hasKerning=False,
        isUnderlined=False,
    ):
        super().__init__()
        self.setPointSize(point_size_px)
        self.setBold(isBold)
        self.setItalic(isItalic)
        self.setKerning(hasKerning)
        self.setUnderline(isUnderlined)
