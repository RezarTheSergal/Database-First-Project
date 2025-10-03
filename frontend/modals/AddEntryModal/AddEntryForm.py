from backend.utils.responce_types import ResponseStatus
from frontend.modals.AddEntryModal.FormRow import FormRow
from frontend.shared.ui import Widget, PushButton, VLayout
from backend.repository import DatabaseRepository, logging, DatabaseResponse
from frontend.shared.ui.inputs.ForeignKeySearchBox import ForeignKeySearchBox
from frontend.shared.ui.inputs import ComboBox, IntInput, FloatInput
from frontend.shared.utils.MessageFactory import MessageFactory
from frontend.shared.lib import translate
from .lib import got_columns, get_element_by_type, is_foreign_key

logger = logging.getLogger(__name__)
database = DatabaseRepository()


class AddEntryForm(Widget):
    rows: list[FormRow] = []
    selectors: list[ComboBox | ForeignKeySearchBox] = []

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

        MessageFactory.show(response, True)

        if got_columns(response):
            MessageFactory.show(
                DatabaseResponse(
                    status=ResponseStatus.ERROR,
                    message=f"Колонки не были получены {response.error}",
                ),
            )
            logger.error("Колонки не были получены", response.error)
        elif response.data is None:
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

        table_name = self.table_name_combo_box.get_value()
        insert_responce = database.insert_into_table(table_name, data)
        MessageFactory.show(insert_responce, True)

    def _clean(self) -> None:
        self.rows = []
        self.selectors = []

    def _setup_form_rows(self, columns: dict) -> None:
        # target_table = self.table_name_combo_box.get_value()

        for [key, data] in columns.items():
            if data["primary_key"]:
                continue

            if is_foreign_key(data):
                input = ForeignKeySearchBox(key,data)
                self.selectors.append(input)
            else:
                input = get_element_by_type(data["type"])

            if not isinstance(input, ComboBox) and not isinstance(input,ForeignKeySearchBox):
                input.is_nullable = data["nullable"]

            if isinstance(input, (IntInput, FloatInput)):
                input.can_be_negative = False  # FIXME: Проверять check_constraints

            row = FormRow(input, key, translate(key))
            self.rows.append(row)

        self.inputs_container.layout.set_children(self.rows)
