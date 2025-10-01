from typing import Any, Dict
from backend.utils.responce_types import ResponseStatus
from frontend.modals.AddEntryModal.FormRow import FormRow
from frontend.shared.ui import ComboBox, Widget, PushButton, VLayout
from backend.repository import DatabaseRepository, logging, DatabaseResponse
from frontend.shared.ui.inputs import ComboBox, IntInput, FloatInput
from frontend.shared.lib import translate
from frontend.utils.MessageFactory import MessageFactory
from frontend.shared.ui.inputs.InputFactory import InputFactory
from frontend.shared.ui.filters.ForeignKeyFilterWidget import ForeignKeyFilterWidget
from .lib import get_allowed_values, got_columns, get_element_by_type, is_foreign_key
from pprint import pprint

logger = logging.getLogger(__name__)
database = DatabaseRepository()


class AddEntryForm(Widget):
    def __init__(self):
        super().__init__(layout=VLayout())

        self.table_name_combo_box = ComboBox(
            items=database.get_tablenames().data, callback=self._set_inputs_by_table  # type: ignore
        )
        self.inputs_container = Widget(VLayout())
        self.submit_button = PushButton("Подтвердить", callback=self._request_entry_PUT)

        self.layout.set_children(
            [self.table_name_combo_box, self.inputs_container, self.submit_button]
        )

    def _set_inputs_by_table(self):
        if not self.table_name_combo_box.get_value():
            return

        response: DatabaseResponse = database.get_table_columns(
            self.table_name_combo_box.get_value()
        )

        MessageFactory.show_response_message(response, self, True)

        if got_columns(response):
            MessageFactory._show_error(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message=f"Колонки не были получены {response.error}",
                ),
                self,
            )
            logger.error("Колонки не были получены", response.error)
            return
        else:
            logger.info([x["type"] for x in response.data.values()])  # type: ignore
            self.inputs_container.layout.clean()

        columns: dict = response.data  # type: ignore
        pprint(columns)
        self._setup_form_rows(columns)

    def _request_entry_PUT(self):
        data = {}

        for child in self.inputs_container.children():
            if isinstance(child, FormRow):
                label_text = child.get_label("en")
                input = child.input

                if not isinstance(input, ComboBox) and not input.is_value_valid():
                    MessageFactory._show_error(
                        DatabaseResponse(
                            status=ResponseStatus.ERROR,
                            message=f"Предоставленное значение {label_text} инвалидно! (Внести: '{input.text()}')",
                        ),
                        self,
                    )
                    logger.error(
                        f"Given value of {label_text} is invalid! (input: '{input.text()}')"
                    )
                    return

                data[label_text] = input.get_value()

        table_name = self.table_name_combo_box.get_value()
        insert_responce = database.insert_into_table(table_name, data)
        MessageFactory.show_response_message(insert_responce, self, True)

    def _setup_form_rows(self, columns: Dict[str, Dict[str, Any]]):
        rows = []
        table = self.table_name_combo_box.get_value()

        for [key, data] in columns.items():
            if data["primary_key"] == True:
                continue

            name = data["name"]
            input = InputFactory.create_filter_widget(name, data)

            if not isinstance(input, ComboBox):
                input.is_nullable = data["nullable"]
            else:
                input.set_items(get_allowed_values(table, name))

            if isinstance(input, (IntInput, FloatInput)):
                input.can_be_negative = False  # FIXME: Проверять check_constraints

            if not data.get("foreign_keys"):
                row = FormRow(input, key)
            else:
                row = input
            rows.append(row)

        self.inputs_container.layout.set_children(rows)
