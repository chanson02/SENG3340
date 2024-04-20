"""
The entry point for the game
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap, QKeyEvent, QPainter, QMouseEvent

import dunwoody_disaster as DD

class MapScreen(QWidget):
    def __init__(self, character):
        super().__init__()
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.map_pixmap = QPixmap(DD.ASSETS['MainMap_Coop_bus'])
        self.map_widget = QLabel()
        self.map_widget.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.mainLayout.addWidget(self.map_widget)
        # overlay = QPixmap(DD.ASSETS['cooper']).scaledToWidth(80)
        # self.mainLayout.addWidget(lbl)
        #
        # painter = QPainter(map)
        # painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        # x = 100
        # y = 100
        # painter.drawPixmap(x, y, overlay)
        # painter.end()
        # lbl.setPixmap(map)


        # self.mapPic = QLabel("")
        # self.mapPic.setPixmap(QPixmap(self.imagePaths[0]))
        # self.mainLayout.addWidget(self.mapPic, 0, 0)

        # self.currImgIndex = 0

    def keyPressEvent(self, event: QKeyEvent):
        print("entering")
        if event.key() == Qt.Key.Key_Left:
            self.currImgIndex = (self.currImgIndex - 1) % len(self.imagePaths)
            self.mapPic.setPixmap(QPixmap(self.imagePaths[self.currImgIndex]))
            print("left")

        elif event.key() == Qt.Key.Key_Right:
            self.currImgIndex = (self.currImgIndex + 1) % len(self.imagePaths)
            self.mapPic.setPixmap(QPixmap(self.imagePaths[self.currImgIndex]))
            print("right")

    def move_character(self, x: int, y: int):
        map_pixmap = QPixmap(DD.ASSETS['MainMap_Coop_bus'])
        painter = QPainter(self.map_pixmap)
        overlay = QPixmap(DD.ASSETS['cooper']).scaledToWidth(80)
        painter.drawPixmap(x, y, overlay)
        self.map_widget.setPixmap(self.map_pixmap)
        self.repaint()


    def mousePressEvent(self, event: QMouseEvent):
        point = event.pos()
        print(point)
        self.move_character(point.x(), point.y())
        #import pdb; pdb.set_trace()
