from frontend.shared.ui import Spinner, Widget, PushButton, VLayout, Row, Size
from backend.repository import DatabaseRepository, logging, DatabaseResponse
from frontend.shared.lib import translate
from .const import allowed_values_per_type

logger = logging.getLogger()
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

        self.table_name_spinner_box = Spinner(
            database.get_tablenames().data, callback=self._set_inputs_by_table  # type: ignore
        )
        self.inputs_container = Widget(VLayout())
        self.submit_button = PushButton("Подтвердить", callback=self._request_entry_PUT)

        self.set_children(
            [self.table_name_spinner_box, self.inputs_container, self.submit_button]
        )

    def _set_inputs_by_table(self):
        if not self.table_name_spinner_box.get_current_item_text():
            return

        response: DatabaseResponse = database.get_table_columns(
            self.table_name_spinner_box.get_current_item_text()
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
            if isinstance(child, Row):
                input_label = child.get_label("en")
                input = child.input

                if hasattr(input, "is_value_valid") and not input.is_value_valid():
                    logger.error(
                        f"Given value is invalid! Valid values for {input_label} are {input.allowed_values}"
                    )
                    return

                data[input_label] = input.get_value()

        table_name = self.table_name_spinner_box.get_current_item_text()
        database.insert_into_table(table_name, data)

    def _setup_form_rows(self, columns: dict):
        rows = []

        for [key, data] in columns.items():
            if data["primary_key"] == True or key.lower().endswith("_id"):
                continue
            allowed_values = allowed_values_per_type.get(data["type"], None)
            row = Row(
                key, translate(key), type=data["type"], allowed_values=allowed_values
            )
            rows.append(row)

        self.inputs_container.set_children(rows)
