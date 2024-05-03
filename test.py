import sys
from dunwoody_disaster.views.AnimationWidget import AnimationWidget
from PySide6.QtWidgets import QApplication, QMainWindow
from dunwoody_disaster.animations.idle import IdleAnimation
from BattleSimulation_copy import Battle


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")

        idle = IdleAnimation()
        self.animation = AnimationWidget(idle)

        self.setCentralWidget(self.animation)
        self.animation.start()

    def closeEvent(self, event):
        _ = event  # silence unused warning
        self.animation.stop()


if __name__ == "__main__":
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
