from frontend.shared.ui import Widget, VLayout, Icon


class MainWindow(Widget):
    def __init__(self, title: str, icon: Icon):
        super().__init__(VLayout())
        self.setWindowTitle(title)
        self.setWindowIcon(icon)
