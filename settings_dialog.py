"""Settings dialog"""

import sys
from munch import Munch, munchify
from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
    QVBoxLayout,
    QDialog,
    QCheckBox,
    QMessageBox
)
from PyQt5 import QtCore
from lib import validateSettings
from constants import DEFAULT_SETTINGS


class SettingsDialog(QDialog):
    """PyQt dialog that is being opened from snake game"""
    settings = None

    def __init__(self, existingSettings):
        super().__init__()
        # self.setModal(True)
        self.setWindowTitle("Settings")
        # self.resize(270, 110)
        # Create a QFormLayout instance
        dlgLayout = QVBoxLayout()

        formLayout = QFormLayout()
        self.elIntervalMilliseconds = QLineEdit()
        self.elIntervalMilliseconds.setText(
            str(existingSettings.intervalMilliseconds))
        formLayout.addRow("Interval (milliseconds) (> 0):",
                          self.elIntervalMilliseconds)
        self.elCellNum = QLineEdit()
        self.elCellNum.setText(str(existingSettings.cellNum))
        formLayout.addRow("Cell Num (>= 2):", self.elCellNum)
        self.elCheckIsOut = QCheckBox()
        self.elCheckIsOut.setChecked(existingSettings.checkIsOut)
        formLayout.addRow("Check is Out", self.elCheckIsOut)
        self.elCheckIsColliding = QCheckBox()
        self.elCheckIsColliding.setChecked(existingSettings.checkIsColliding)
        formLayout.addRow("Check is Colliding", self.elCheckIsColliding)

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.button_box.accepted.connect(self.onAccept)
        # self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.onReject)

        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(QLabel(
            "Clicking Ok button will reset game progress and restart the application"))
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
            if validateSettings(settings):
                self.settings = settings
                self.accept()
            else:
                raise ValueError
        except ValueError:
            self.showWarning()

    def onReject(self):
        self.reject()

    @staticmethod
    def run(existingSettings):
        # dialog = SettingsDialog(parent)
        dialog = SettingsDialog(existingSettings)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        result = dialog.exec_()
        # date = dialog.dateTime()
        # return (date.date(), date.time(), result == QDialog.Accepted)
        # settings = None
        return (dialog.settings, result == QDialog.Accepted)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = SettingsDialog(munchify(DEFAULT_SETTINGS))
    dlg.show()
    sys.exit(app.exec_())
