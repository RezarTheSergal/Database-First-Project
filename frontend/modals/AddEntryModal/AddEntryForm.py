from backend.utils.responce_types import ResponseStatus
from frontend.modals.AddEntryModal.FormRow import FormRow
from frontend.shared.ui import Widget, PushButton, VLayout
from backend.utils.logger import logging
from backend.repository import DatabaseResponse
from frontend.shared.ui.inputs import InputWidgetFactory,ComboBox, ForeignKeySearchBox
from frontend.shared.utils.DatabaseMiddleware import DatabaseMiddleware
from frontend.shared.utils.MessageFactory import MessageFactory
from frontend.shared.lib import translate

logger = logging.getLogger(__name__)


class AddEntryForm(Widget):
    rows: list[FormRow] = []
    selectors: list[ComboBox | ForeignKeySearchBox] = []

    def __init__(self):
        super().__init__(layout=VLayout())

        response = DatabaseMiddleware.get_table_names()
        if response and response.data:
            items = response.data
        else:
            items = []
        self.table_name_combo_box = ComboBox(
            items = items, callback = self._set_inputs_by_table
        )
        self.inputs_container = Widget(VLayout())
        self.submit_button = PushButton("Подтвердить", callback=self._request_entry_PUT)

        self.layout.set_children(
            [self.table_name_combo_box, self.inputs_container, self.submit_button]
        )

    def _set_inputs_by_table(self):
        if not self.table_name_combo_box.get_value():
            return

        response = DatabaseMiddleware.get_columns_by_table_name(
            self.table_name_combo_box.get_value()
        )

        MessageFactory.show(response)

        if not response:
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message="Нет ответа.",
                ),
            )
        elif response.status == ResponseStatus.ERROR or not response.data:
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message=f"Колонки не были получены {response.error}",
                ),
            )
            logger.error("Колонки не были получены", response.error)
        elif not response.data.values():
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message=f"Нет данных {response.error}",
                ),
            )
            logger.error("Нет данных", response.error)
        else:
            logger.info([x["type"] for x in response.data.values()])
            self.inputs_container.layout.clean()

            columns: dict = response.data  # type: ignore
            # pprint(columns)
            self._clean()
            self._setup_form_rows(columns)

    def _any_selector_value_not_set(self) -> bool:
        return any(selector.get_value() == "--не выбрано--" for selector in self.selectors)

    def _request_entry_PUT(self):
        if self._any_selector_value_not_set():
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message="Какой-то из селекторов не выбран!",
                ),
            )
            return

        data = {}

        for child in self.inputs_container.children():
            if isinstance(child, FormRow):
                label_text: str = child.get_label("en")
                input = child.input

                if not isinstance(input, ComboBox) and not input.is_value_valid():
                    MessageFactory.show(
                        DatabaseResponse(
                            status=ResponseStatus.ERROR,
                            message=f"Предоставленное значение {label_text} инвалидно! (Внести: '{input.text()}')",
                        ),
                    )
                    logger.error(
                        f"Given value of {label_text} is invalid! (input: '{input.text()}')"
                    )
                    return

                data[label_text] = input.get_value()

        table_name: str = self.table_name_combo_box.get_value()
        insert_responce = DatabaseMiddleware.put_data(table_name, data)
        MessageFactory.show(insert_responce)

    def _clean(self) -> None:
        self.rows = []
        self.selectors = []

    def _setup_form_rows(self, columns: dict) -> None:
        # target_table = self.table_name_combo_box.get_value()

        for [key, data] in columns.items():
            if data["primary_key"]:
                continue

            meta = data
            meta["column_name"] = key
            row = FormRow(InputWidgetFactory.create(meta), key, translate(key))
            self.rows.append(row)

        self.inputs_container.layout.set_children(self.rows)
