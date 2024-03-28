from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QGridLayout, QSpacerItem, QSizePolicy, QLayout


class Arsenal(QWidget):
    """
    The arsenal is made up of two `inventory` widgets which display items
    """

    def __init__(self):
        super().__init__()
        self.imageAssets = {
                item: QPixmap(f"./assets/{item}.jpg")
                for item in ["sword", "spear", "shield", "gloves"]
                }

        self.setStyleSheet("background-color: black;")
        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def spacer(self, height: int) -> QSpacerItem:
        return QSpacerItem(0, height, QSizePolicy.Fixed, QSizePolicy.Fixed)

    def create_inventory(self, label: str, items: list[dict]) -> QWidget:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        row = 0

        lbl = QLabel(label)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("color: white;")
        layout.addWidget(lbl, row, 1)
        row += 1
        layout.addItem(self.spacer(10), row, 1)
        row += 1

        for item in items:
            name = QLabel(item['name'])
            name.setAlignment(Qt.AlignCenter)
            name.setStyleSHeet("color: white;")
            layout.addWidget(name, row, 1)
            row += 1

            layout.addItem(self.spacer(10), row, 1)
            row += 1

            image = QLabel("")
            image.setAlignment(Qt.AlignCenter)
            image.setPixmap(item['image'])
            layout.addWidget(image, row, 1)
            row += 1

            layout.addItem(self.spacer(10), row, 1)
            row += 1

            properties = QLabel(f"H: {item['KEY'][0]}\nM: {item['KEY'][1]}\nMech: {item['KEY'][2]}")
            properties.setStyleSheet("color: white;")
            layout.addWidget(properties, row, 1)
            row += 1

            layout.addItem(self.spacer(40), row, 1)
            row += 1
