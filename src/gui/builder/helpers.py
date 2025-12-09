from aqt import QTableWidget

from ...types import TableRowData


def get_table_data(table: QTableWidget) -> list[TableRowData]:
    """Collect data from table."""

    row_count = table.rowCount()

    table_data: list[TableRowData] = []
    for row in range(row_count):
        term_column = table.item(row, 0)
        example_column = table.item(row, 1)
        additional_context_column = table.item(row, 2)

        term_text = term_column.text() if term_column else ""
        if not term_text:
            continue

        row_data: TableRowData = {"term": term_text}

        if example_column and (example_text := example_column.text()):
            row_data["example"] = example_text

        if additional_context_column and (
            context_text := additional_context_column.text()
        ):
            row_data["additional_context"] = context_text

        table_data.append(row_data)

    return table_data
