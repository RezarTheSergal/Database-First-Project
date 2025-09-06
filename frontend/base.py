# 2.2.1. Главное окно с кнопками: (vladcheck)
# - «Создать схему и таблицы» (запуск скрипта CREATE ...);
# - «Внести данные» — открывает модальное окно ввода (родительское окно
# заблокировано на время ввода);
# - «Показать данные» — открывает отдельное окно (можно немодальное) со
# сводной таблицей (например, EXPERIMENTS/RUNS с JOIN).


from PySide6.QtCore import Qt, QDate, QAbstractTableModel, QModelIndex
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSpinBox,
    QDateEdit, QComboBox, QCheckBox, QTextEdit, QTableView, QGroupBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()