from .Text import Text
from .Font import Font
from ...lib.utils import setId
from PySide6.QtGui import QLinearGradient, QBrush, QPalette
from PySide6.QtCore import Qt


class H1(Text):
    def __init__(self, text: str):
        super().__init__(text)
        self.setFont(Font(64, family="RubikWetPaint"))
        setId(self, "h1")

        # Create a gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)  # Left to right gradient
        gradient.setColorAt(0.0, "red")  # Start color
        gradient.setColorAt(0.5, "yellow")  # Middle color
        gradient.setColorAt(1.0, "blue")  # End color

        # Create a brush from the gradient
        brush = QBrush(gradient)

        # Get the current palette and set the text brush
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Text, brush)

        # Apply the palette to the label
        self.setPalette(palette)

        # Ensure the label updates when resized
        self.resizeEvent = lambda event: self.update_gradient(self, event)

    def update_gradient(self, label, event):
        """Update gradient when label is resized"""
        gradient = QLinearGradient(0, 0, label.width(), 0)
        gradient.setColorAt(0.0, "red")
        gradient.setColorAt(0.5, "yellow")
        gradient.setColorAt(1.0, "blue")
        brush = QBrush(gradient)
        palette = label.palette()
        palette.setBrush(QPalette.ColorRole.Text, brush)
        label.setPalette(palette)
        event.accept()
