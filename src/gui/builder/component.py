import json
from anki.decks import DeckId
from aqt.deckchooser import DeckChooser
from aqt.utils import showInfo
from aqt.qt import (
    QDialog,
    QTableWidgetItem,
    QPushButton,
)
from aqt.operations.deck import set_current_deck

from .form import CardBuilderWindowForm
from .helpers import get_table_data


class CardBuilderWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._mw = parent

        self.setWindowTitle("Card Builder")
        self.setMinimumSize(1200, 700)

        self._form = CardBuilderWindowForm(self)
        self._form.add_button.clicked.connect(self._add_new_row)
        self._form.import_json_button.clicked.connect(self._import_json)
        self._form.import_image_button.clicked.connect(self._import_image)
        self._form.generate_button.clicked.connect(self._generate)

        self._deck_chooser = DeckChooser(
            self._mw,
            self._form.deck_area,
            on_deck_changed=self.on_deck_changed,
            dyn=True,
        )

        self.setLayout(self._form.layout)

    def _add_new_row(self):
        """Add a new empty row to the table."""

        row_count = self._form.table.rowCount()
        self._form.table.insertRow(row_count)

        # Add empty items to the new row
        self._form.table.setItem(row_count, 0, QTableWidgetItem(""))
        self._form.table.setItem(row_count, 1, QTableWidgetItem(""))
        self._form.table.setItem(row_count, 2, QTableWidgetItem(""))

        # Add delete button to the new row
        delete_button = QPushButton("X")
        delete_button.clicked.connect(lambda _, row=row_count: self._delete_row(row))
        self._form.table.setCellWidget(row_count, 3, delete_button)

        # Scroll to the new row
        self._form.table.scrollToItem(self._form.table.item(row_count, 0))

        # Remove row index column (vertical header)
        if vertical_header := self._form.table.verticalHeader():
            vertical_header.setVisible(False)

    def _delete_row(self, row: int) -> None:
        """Delete the specified row from the table."""
        if row < 0 or row >= self._form.table.rowCount():
            return

        self._form.table.removeRow(row)

        # Update delete button connections after row deletion.
        for table_row in range(self._form.table.rowCount()):
            if delete_button := self._form.table.cellWidget(table_row, 3):
                if not isinstance(delete_button, QPushButton):
                    continue

                delete_button.clicked.disconnect()  # Disconnect all existing connections
                delete_button.clicked.connect(  # Reconnect with updated row index
                    lambda _, r=table_row: self._delete_row(r)
                )

    def _import_json(self):
        """Handle JSON import functionality."""

        # TODO: Implement JSON import logic
        showInfo("JSON import functionality will be implemented here.")

    def _import_image(self):
        """Handle image import functionality."""

        # TODO: Implement image import logic
        showInfo("Image import functionality will be implemented here.")

    def _more_info(self):
        """Handle More Info button functionality."""
        # TODO: Implement More Info logic
        showInfo("More Info functionality will be implemented here.")

    def on_deck_changed(self, deck_id: int) -> None:
        set_current_deck(parent=self, deck_id=DeckId(deck_id))

    def _generate(self):
        """Handle Generate button functionality."""

        table_data = get_table_data(self._form.table)
        deck_id = self._deck_chooser.selected_deck_id
        deck_name = self._deck_chooser.selected_deck_name()
        showInfo(f"deck_id:\n\n{deck_id} - {deck_name}")

        # Convert to JSON and display
        json_data = json.dumps(table_data, indent=2, ensure_ascii=False)
        showInfo(f"Table data as JSON:\n\n{json_data}")
        self.close()
