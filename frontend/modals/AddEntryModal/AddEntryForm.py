from frontend.modals.AddEntryModal.FormRow import FormRow
from frontend.shared.ui import ComboBox, Widget, PushButton, VLayout
from backend.repository import DatabaseRepository, logging, DatabaseResponse
from frontend.shared.ui.inputs import ComboBox, IntInput, FloatInput
from frontend.shared.lib import translate
from .lib.utils import get_element_by_type
from .lib.get_allowed_values import get_allowed_values

logger = logging.getLogger("frontend")
database = DatabaseRepository()


def got_columns(response: DatabaseResponse) -> bool:
    return (
        response.status == "error"
        or response.data is None
        or response.data.values() is None
    )


class AddEntryForm(Widget):
    def __init__(self):
        super().__init__(layout=VLayout())

        self.table_name_combo_box = ComboBox(
            items=database.get_tablenames().data, callback=self._set_inputs_by_table  # type: ignore
        )
        self.inputs_container = Widget(VLayout())
        self.submit_button = PushButton("Подтвердить", callback=self._request_entry_PUT)

        self.set_children(
            [self.table_name_combo_box, self.inputs_container, self.submit_button]
        )

    def _set_inputs_by_table(self):
        if not self.table_name_combo_box.get_current_item_text():
            return

        response: DatabaseResponse = database.get_table_columns(
            self.table_name_combo_box.get_current_item_text()
        )

        if got_columns(response):
            logger.error("Колонки не были получены", response.error)
            return
        else:
            logger.info([x["type"] for x in response.data.values()])  # type: ignore
            self.inputs_container.clean()

        columns: dict = response.data  # type: ignore
        self._setup_form_rows(columns)

    def _request_entry_PUT(self):
        data = {}

        for child in self.inputs_container.children():
            if isinstance(child, FormRow):
                label_text = child.get_label("en")
                input = child.input

                if not isinstance(input, ComboBox) and not input.is_value_valid():
                    logger.error(
                        f"Given value of {label_text} is invalid! (input: '{input.text()}')"
                    )
                    return

                data[label_text] = input.get_value()

        table_name = self.table_name_combo_box.get_current_item_text()
        database.insert_into_table(table_name, data)

    def _setup_form_rows(self, columns: dict):
        rows = []
        table = self.table_name_combo_box.get_current_item_text()

        for [key, data] in columns.items():
            if data["primary_key"] == True or key.lower().endswith("_id"):
                continue

            name = data["name"]
            input = get_element_by_type(data["type"])

            if not isinstance(input, ComboBox):
                input.is_nullable = data["nullable"]
            else:
                input.set_items(get_allowed_values(table, name))

            if isinstance(input, (IntInput, FloatInput)):
                input.can_be_negative = False  # FIXME: Проверять check_constraints

            row = FormRow(input, key, translate(key))
            rows.append(row)

        self.inputs_container.set_children(rows)
