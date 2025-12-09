import json
from anki.decks import DeckId
from aqt import QWidget
from aqt.deckchooser import DeckChooser
from aqt.utils import showInfo
from aqt.qt import (
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QHBoxLayout,
    QAbstractItemView,
)
from aqt.operations.deck import set_current_deck

from .helpers import get_table_data


class CardBuilderWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.mw = parent

        self.setWindowTitle("Card Builder")
        self.setMinimumSize(1200, 700)

        # Create main layout
        layout = QVBoxLayout()

        layout.addLayout(self._create_toolbar())

        # Create table widget
        self.table = self._create_table()
        layout.addWidget(self.table)

        # Create bottom buttons layout
        bottom_layout = self._create_bottom_buttons()
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def _create_toolbar(self) -> QHBoxLayout:
        toolbar_layout = QHBoxLayout()

        # Add "Add Row" button
        add_button = QPushButton("+")
        add_button.setDefault(False)
        add_button.setAutoDefault(False)
        add_button.clicked.connect(self._add_new_row)
        toolbar_layout.addWidget(add_button)

        toolbar_layout.addStretch()

        # Add "Import json" button
        import_json_button = QPushButton("Import from json")
        import_json_button.setDefault(False)
        import_json_button.setAutoDefault(False)
        import_json_button.clicked.connect(self._import_json)
        toolbar_layout.addWidget(import_json_button)

        # Add "Import image" button
        import_image_button = QPushButton("Import from image")
        import_image_button.setDefault(False)
        import_image_button.setAutoDefault(False)
        import_image_button.clicked.connect(self._import_image)
        toolbar_layout.addWidget(import_image_button)

        return toolbar_layout

    def _create_bottom_buttons(self) -> QHBoxLayout:
        """Create the bottom buttons layout with More Info and Generate buttons."""
        bottom_layout = QHBoxLayout()

        deck_area = QWidget()
        deck_area.setFixedWidth(200)

        self._deck_chooser = DeckChooser(
            self.mw,
            deck_area,
            on_deck_changed=self.on_deck_changed,
            dyn=True,
        )

        bottom_layout.addWidget(deck_area)

        bottom_layout.addStretch()

        # Add "Generate" button on the right
        generate_button = QPushButton("Generate")
        generate_button.setDefault(False)
        generate_button.setAutoDefault(False)
        generate_button.clicked.connect(self._generate)
        bottom_layout.addWidget(generate_button)

        return bottom_layout

    def _create_table(self) -> QTableWidget:
        table = QTableWidget()
        table.setColumnCount(4)  # Added one column for delete button
        table.setHorizontalHeaderLabels(["Term", "Example", "Additional Context", ""])

        if header := table.horizontalHeader():
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            # Set fixed width for the Actions column
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
            header.setDefaultSectionSize(20)  # Fixed width for delete button column

        # Set selection behavior to select entire rows
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        return table

    def _add_new_row(self):
        """Add a new empty row to the table."""

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)

        # Add empty items to the new row
        self.table.setItem(row_count, 0, QTableWidgetItem(""))
        self.table.setItem(row_count, 1, QTableWidgetItem(""))
        self.table.setItem(row_count, 2, QTableWidgetItem(""))

        # Add delete button to the new row
        delete_button = QPushButton("X")
        delete_button.clicked.connect(lambda _, row=row_count: self._delete_row(row))
        self.table.setCellWidget(row_count, 3, delete_button)

        # Scroll to the new row
        self.table.scrollToItem(self.table.item(row_count, 0))

        # Remove row index column (vertical header)
        if vertical_header := self.table.verticalHeader():
            vertical_header.setVisible(False)

    def _delete_row(self, row: int) -> None:
        """Delete the specified row from the table."""
        if row < 0 or row >= self.table.rowCount():
            return

        self.table.removeRow(row)

        # Update delete button connections after row deletion.
        for table_row in range(self.table.rowCount()):
            if delete_button := self.table.cellWidget(table_row, 3):
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

        table_data = get_table_data(self.table)
        deck_id = self._deck_chooser.selected_deck_id
        deck_name = self._deck_chooser.selected_deck_name()
        showInfo(f"deck_id:\n\n{deck_id} - {deck_name}")

        # Convert to JSON and display
        json_data = json.dumps(table_data, indent=2, ensure_ascii=False)
        showInfo(f"Table data as JSON:\n\n{json_data}")
        self.close()
