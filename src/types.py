from typing import TypedDict


class _TableRowData(TypedDict, total=False):  # Optional part
    example: str
    additional_context: str


class TableRowData(_TableRowData):  # Required part
    term: str
