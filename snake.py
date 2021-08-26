import sys

from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QCheckBox
)

from PyQt5.QtCore import (
    QTimer
)

BOARD_SIZE = 20
pos = {"x": 0, "y": 0}

class Window(QWidget):

    def update(self):
        if pos["x"] < BOARD_SIZE:
            pos["x"] += 1
        else:
            pos["x"] = 0

        # print(pos)
        # print("l29")
        self.render_point()

    def render_point(self):
        # for row in self.checkboxes:
        for y,row in enumerate(self.checkboxes):
            for x,c in enumerate(row):
                # [pos["y"]][pos["x"]]
                # print([y,x])
                if y == pos["y"] and x == pos["x"]:
                    c.setEnabled(True)
                    c.setChecked(True)
                else:
                    c.setChecked(False)
                    c.setEnabled(False)
                    



    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.checkboxes = []
        for _ in range(BOARD_SIZE):
            row = []
            # vl = QVBoxLayout()
            hl = QHBoxLayout()

            for _ in range(BOARD_SIZE):
                c = QCheckBox()
                c.setEnabled(False)
                hl.addWidget(c)
                row.append(c)

            self.checkboxes.append(row)
            layout.addLayout(hl)

        # Set the layout on the application's window
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.update)        
        timer.start(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
