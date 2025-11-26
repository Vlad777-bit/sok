from typing import Any


def validation_errors_to_list(errors: list[dict[str, Any]]) -> list[dict[str, str]]:
    """
    Превращаем pydantic/fastapi errors() в короткий список для фронта.
    """
    out: list[dict[str, str]] = []
    for e in errors:
        loc = ".".join(str(x) for x in e.get("loc", []))
        msg = str(e.get("msg", "Invalid value"))
        out.append({"field": loc, "message": msg})
    return out
