from aqt.qt import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QHeaderView,
    QPushButton,
    QHBoxLayout,
    QAbstractItemView,
)


class CardBuilderWindowForm:
    def __init__(self, component: QDialog):
        # Create main layout
        self.layout = QVBoxLayout()

        self.layout.addLayout(self._create_toolbar())

        # Create table widget
        self.table = self._create_table()
        self.layout.addWidget(self.table)

        # Create bottom buttons layout
        bottom_layout = self._create_bottom_buttons()
        self.layout.addLayout(bottom_layout)

    def _create_toolbar(self) -> QHBoxLayout:
        toolbar_layout = QHBoxLayout()

        # Add "Add Row" button
        self.add_button = QPushButton("+")
        self.add_button.setDefault(False)
        self.add_button.setAutoDefault(False)
        toolbar_layout.addWidget(self.add_button)

        toolbar_layout.addStretch()

        # Add "Import json" button
        self.import_json_button = QPushButton("Import from json")
        self.import_json_button.setDefault(False)
        self.import_json_button.setAutoDefault(False)
        toolbar_layout.addWidget(self.import_json_button)

        # Add "Import image" button
        self.import_image_button = QPushButton("Import from image")
        self.import_image_button.setDefault(False)
        self.import_image_button.setAutoDefault(False)
        toolbar_layout.addWidget(self.import_image_button)

        return toolbar_layout

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

    def _create_bottom_buttons(self) -> QHBoxLayout:
        """Create the bottom buttons layout with More Info and Generate buttons."""
        bottom_layout = QHBoxLayout()

        self.deck_area = QWidget()
        self.deck_area.setFixedWidth(200)

        bottom_layout.addWidget(self.deck_area)

        bottom_layout.addStretch()

        # Add "Generate" button on the right
        self.generate_button = QPushButton("Generate")
        self.generate_button.setDefault(False)
        self.generate_button.setAutoDefault(False)
        bottom_layout.addWidget(self.generate_button)

        return bottom_layout
