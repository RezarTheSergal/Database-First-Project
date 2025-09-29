from backend.utils.responce_types import DatabaseResponse


def got_columns(response: DatabaseResponse) -> bool:
    return (
        response.status == "error"
        or response.data is None
        or response.data.values() is None
    )
