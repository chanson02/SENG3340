from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QKeyEvent
from PySide6.QtWidgets import QWidget
import dunwoody_disaster as DD
from typing import Callable

class Credits(QWidget):
    def __init__(self):
        super().__init__()
        self._finishCallback = DD.unimplemented
        self.text_lines = [
            "<Credits go here>",
            "",
            "Cooper",
            "",
            "Noah",
            "",
            "John",
            "",
            "Mitch",
            "<Credits end here>"
        ]
        self.line_spacing = 30
        self.scroll_speed = 0.55  # Adjust the scrolling speed as needed
        self.scroll_position = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Story Crawl")
        self.setGeometry(100, 100, 1920, 1080)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateScroll)
        self.timer.start(10)  # Adjust the interval for smoother or faster scrolling
        self.show()

    def updateScroll(self):
        self.scroll_position += self.scroll_speed
        if (
            self.scroll_position
            >= len(self.text_lines) * self.line_spacing + self.height()
        ):
            self.endCreditScreen()  # Once scrolling is done, callback and go to next screen.
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.fillRect(self.rect(), Qt.black)

        font = QFont("Arial", 20)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))

        y = self.height() - self.scroll_position

        for line in self.text_lines:
            text_width = painter.fontMetrics().horizontalAdvance(line)
            x = (self.width() - text_width) / 2
            painter.drawText(x, y, line)
            y += self.line_spacing

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.endCreditScreen()

    def endCreditScreen(self):
        self.timer.stop()
        self._finishCallback
        # Call the callback function to go to the next screen
        if self._finishCallback:
            self._finishCallback()
        self.deleteLater()

    def onFinishCredits(self, callback: Callable):
        self._finishCallback = callback
