from backend.utils.responce_types import DatabaseResponse, ResponseStatus
from frontend.shared.ui import PromptBox
from PySide6.QtWidgets import QMessageBox


class MessageFactory:
    """Фабрика для показа сообщений пользователю"""

    @staticmethod
    def show(response: DatabaseResponse | None) -> bool:
        """
        Показывает сообщение в зависимости от статуса ответа.
        Возвращает True, если сообщение является типа ERROR
        """
        if not response:
            MessageFactory._show_error(
                DatabaseResponse(status=ResponseStatus.ERROR, message="Нет ответа")
            )
            return True
        elif response.status == ResponseStatus.ERROR:
            MessageFactory._show_error(response)
            return True
        elif response.status == ResponseStatus.WARNING:
            MessageFactory._show_warning(response)
            return False
        elif response.status == ResponseStatus.SUCCESS:
            MessageFactory._show_success(response)
            return False
        else:
            return False

    @staticmethod
    def _show_error(response: DatabaseResponse) -> None:
        """Показывает сообщение об ошибке"""
        error_details = ""

        msg = PromptBox()
        msg.setIcon(PromptBox.Icon.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes)
        msg.button(QMessageBox.StandardButton.Yes).setText("Ок")

        if response.error_details:
            details_str = "\n".join(
                [f"{k}: {v}" for k, v in response.error_details.items()]
            )
            error_details = f"\n\nДетали ошибки:\n{details_str}"
        if response.error_code:
            msg.setInformativeText(
                f"Код ошибки: {response.error_code.value}{error_details}"
            )
        else:
            msg.setInformativeText(f"Код ошибки: неизвестен{error_details}")

        msg.exec()

    @staticmethod
    def _show_warning(response: DatabaseResponse):
        """Показывает предупреждение"""
        msg = PromptBox()
        msg.setIcon(PromptBox.Icon.Warning)
        msg.setWindowTitle("Предупреждение")
        msg.setText(response.message)
        msg.exec()

    @staticmethod
    def _show_success(response: DatabaseResponse):
        """Показывает сообщение об успехе (только для модальных окон)"""
        msg = PromptBox()
        msg.setIcon(PromptBox.Icon.Information)
        msg.setWindowTitle("Успех")
        msg.setText(response.message)
        if response.message and response.message != "Операция выполнена успешно":
            msg.setInformativeText(response.message)

        msg.exec()
