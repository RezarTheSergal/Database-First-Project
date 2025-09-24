from PySide6.QtWidgets import QWidget

def setId(element: QWidget, id: str):
    element.setObjectName(id)

def setClass(element: QWidget, cls: str):
    element.setProperty("class", cls)
