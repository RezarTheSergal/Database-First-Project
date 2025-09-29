from frontend.shared.ui import Spinner, Widget, PushButton, VLayout, Row, Size
from backend.repository import DatabaseRepository, logging
from frontend.shared.lib import translate

logger = logging.getLogger()
database = DatabaseRepository()

class AddEntryForm(Widget):
    def __init__(self):
        super().__init__(layout=VLayout())

        self.table_name_spinner_box = Spinner(
            database.get_tablenames().data, callback=self._set_inputs_by_table  # type: ignore
        )
        self.inputs_container = Widget(VLayout())
        self.submit_button = PushButton("Подтвердить", callback=self._request_entry_PUT)

        self.add_children(
            [self.table_name_spinner_box, self.inputs_container, self.submit_button]
        )

    def _set_inputs_by_table(self):
        if not self.table_name_spinner_box.get_current_item_text():
            return

        response = database.get_table_columns(
            self.table_name_spinner_box.get_current_item_text()
        )

        if response.status == "error" or response.data is None:
            logger.error("Колонки не были получены", response.error)
            return
        print([x["type"] for x in response.data.values()])
        columns: dict[str, dict] = response.data

        self.inputs_container.clean()
        for [key, data] in columns.items():
            if data["primary_key"] == True:
                continue
            row = Row(key, translate(key), type=data["type"])
            self.inputs_container.add_children([row])

    def _request_entry_PUT(self):
        data = {}

        for child in self.inputs_container.children():
            if isinstance(child, Row):
                data[child.get_label("en")] = child.get_input_value()

        table_name = self.table_name_spinner_box.get_current_item_text()
        database.insert_into_table(table_name, data)
