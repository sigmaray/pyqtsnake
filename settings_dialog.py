from lib import validateSettings
import sys
from munch import Munch, unmunchify

from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QLineEdit,
    QWidget,
    QDialogButtonBox,
    QVBoxLayout,
    QDialog,
    QCheckBox,
    QMessageBox
)


class SettingsDialog(QDialog):
    settings = None

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        # self.resize(270, 110)
        # Create a QFormLayout instance
        dlgLayout = QVBoxLayout()

        formLayout = QFormLayout()
        self.elIntervalMilliseconds = QLineEdit()
        formLayout.addRow("Interval (milliseconds) (> 0):",
                          self.elIntervalMilliseconds)
        self.elCellNum = QLineEdit()
        formLayout.addRow("Cell Num (>= 2):", self.elCellNum)
        self.elCheckIsOut = QCheckBox()
        formLayout.addRow("Check is Out", self.elCheckIsOut)
        self.elCheckIsColliding = QCheckBox()
        formLayout.addRow("Check is Colliding", self.elCheckIsColliding)

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.button_box.accepted.connect(self.onAccept)
        # self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.onReject)

        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(self.button_box)

        # Set the layout on the application's window
        self.setLayout(dlgLayout)

    def showWarning(self):
        QMessageBox.warning(self, "Validation error",
                            "Please enter correct values")

    def onAccept(self):
        try:
            settings = Munch()
            settings.intervalMilliseconds = int(
                self.elIntervalMilliseconds.text())
            settings.cellNum = int(self.elCellNum.text())
            settings.checkIsOut = self.elCheckIsOut.isChecked()
            settings.checkIsColliding = self.elCheckIsColliding.isChecked()            
            if (validateSettings(settings)):
                self.settings = settings
                self.accept()
            else:
                raise ValueError
        except ValueError:
            self.showWarning()

    def onReject(self):
        self.reject()

    @staticmethod
    def run(parent=None):
        # dialog = SettingsDialog(parent)
        dialog = SettingsDialog()
        result = dialog.exec_()
        # date = dialog.dateTime()
        # return (date.date(), date.time(), result == QDialog.Accepted)
        # settings = None
        return (dialog.settings, result == QDialog.Accepted)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = SettingsDialog()
    dlg.show()
    sys.exit(app.exec_())
