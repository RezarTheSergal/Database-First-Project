class GenericInput:
    allowed_values = None

    def set_allowed_values(self, values: list):
        self.allowed_values = values

    def is_value_valid(self, is_case_sensitive: bool = True) -> bool:
        value = self.get_value()

        if self.allowed_values is None:
            return True
        elif is_case_sensitive:
            return value in self.allowed_values
        else:
            return str(value).lower() in [v.lower() for v in self.allowed_values]

    def get_value(self):
        pass
