from ..settings import Path


# Valdemar_check: Добавлено для удобства
def join_path(*path_parts):
    res: str = ""
    for part in path_parts:
        res = (Path(res).parent.resolve() / part).__str__()
    return res
