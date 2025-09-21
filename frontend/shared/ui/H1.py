from .Text import Text
from .Font import Font
from ..lib.utils import setId


class H1(Text):
    def __init__(self, text: str):
        super().__init__(text)
        self.setFont(Font(36, family="RubikWetPaint"))
        setId(self, "h1")
