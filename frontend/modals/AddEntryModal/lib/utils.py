from frontend.shared.ui.inputs import (
    IntInput,
    FloatInput,
    ComboBox,
    StringInput,
    BoolInput,
    DateInput,
)


def isIntType(type: str) -> bool:
    return type in ["INTEGER", "INT", "BIGINT"] or "NUMERIC" in type


def isFloatType(type: str) -> bool:
    return type in ["FLOAT", "DOUBLE"]


def isArrayType(type: str) -> bool:
    return "ARRAY" in type or "VARCHAR" in type


def isDateType(type: str) -> bool:
    return type in ["TIMESTAMP", "DATE", "DATETIME"]


def isBoolType(type: str) -> bool:
    return type == "BOOL" or type == "BOOLEAN"


def get_element_by_type(type: str):
    if isIntType(type):
        return IntInput()
    elif isFloatType(type):
        return FloatInput()
    elif isArrayType(type):
        return ComboBox([])
    elif isDateType(type):
        return DateInput()
    elif isBoolType(type):
        return BoolInput()
    else:
        return StringInput()
