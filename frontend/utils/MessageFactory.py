from PySide6.QtWidgets import QMessageBox
from backend.utils.responce_types import DatabaseResponse, ResponseStatus

class MessageFactory:
    """Фабрика для показа сообщений пользователю"""
    
    @staticmethod
    def show_response_message(response: DatabaseResponse, is_modal: bool = False):
        """Показывает сообщение в зависимости от статуса ответа"""
        if response.status == ResponseStatus.ERROR:
            MessageFactory._show_error(response)
        elif response.status == ResponseStatus.WARNING:
            MessageFactory._show_warning(response)
        elif response.status == ResponseStatus.SUCCESS and is_modal:
            MessageFactory._show_success(response)
    
    @staticmethod
    def _show_error(response: DatabaseResponse):
        """Показывает сообщение об ошибке"""
        error_details = ""
        if response.error_details:
            details_str = "\n".join([f"{k}: {v}" for k, v in response.error_details.items()])
            error_details = f"\n\nДетали ошибки:\n{details_str}"
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText(f"{response.message}")
        if response.error_code:
            msg.setInformativeText(f"Код ошибки: {response.error_code.value}{error_details}")
        else:
            msg.setInformativeText(f"Код ошибки: неизвестен{error_details}")
        msg.exec()
    
    @staticmethod
    def _show_warning(response: DatabaseResponse):
        """Показывает предупреждение"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Предупреждение")
        msg.setText(response.message)
        msg.exec()
    
    @staticmethod
    def _show_success(response: DatabaseResponse):
        """Показывает сообщение об успехе (только для модальных окон)"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Успех")
        msg.setText("Операция выполнена успешно!")
        if response.message and response.message != "Операция выполнена успешно":
            msg.setInformativeText(response.message)
        msg.exec()