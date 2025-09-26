from PySide6.QtWidgets import QMessageBox, QWidget
from backend.utils.responce_types import DatabaseResponse, ResponseStatus

class MessageFactory:
    """Фабрика для показа сообщений пользователю"""
    
    @staticmethod
    def show_response_message(response: DatabaseResponse, parent: QWidget, is_modal: bool = False):
        """Показывает сообщение в зависимости от статуса ответа"""
        if response.status == ResponseStatus.ERROR:
            MessageFactory._show_error(response, parent)
        elif response.status == ResponseStatus.WARNING:
            MessageFactory._show_warning(response, parent)
        elif response.status == ResponseStatus.SUCCESS and not is_modal:
            MessageFactory._show_success(response, parent)
    
    @staticmethod
    def _show_error(response: DatabaseResponse, parent: QWidget):
        """Показывает сообщение об ошибке"""
        error_details = ""
        if response.error_details:
            details_str = "\n".join([f"{k}: {v}" for k, v in response.error_details.items()])
            error_details = f"\n\nДетали ошибки:\n{details_str}"
        
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText(f"{response.message}")
        if response.error_code:
            msg.setInformativeText(f"Код ошибки: {response.error_code.value}{error_details}")
        else:
            msg.setInformativeText(f"Код ошибки: неизвестен{error_details}")
        msg.exec()
    
    @staticmethod
    def _show_warning(response: DatabaseResponse, parent: QWidget):
        """Показывает предупреждение"""
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Предупреждение")
        msg.setText(response.message)
        msg.exec()
    
    @staticmethod
    def _show_success(response: DatabaseResponse, parent: QWidget):
        """Показывает сообщение об успехе (только для модальных окон)"""
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Успех")
        msg.setText("Операция выполнена успешно!")
        if response.message and response.message != "Операция выполнена успешно":
            msg.setInformativeText(response.message)
        msg.exec()