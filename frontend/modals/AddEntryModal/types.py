class ColumnEntry:
    type: str
    nullable: bool
    primary_key: bool
    foreign_keys: list[str]
    default: None | str
