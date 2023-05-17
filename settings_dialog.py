"""Settings dialog"""

import sys
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
from munch import Munch
from lib import validateSettings
from constants import DEFAULT_SETTINGS
import type_declarations as t


class SettingsDialog(QDialog):
    """PyQt dialog that is being opened from snake game"""
    settings: t.Settings

    # Put all inputs inside the scope
    widgets = Munch()

    def __init__(self, existingSettings):
        super().__init__()

        # self.setModal(True)

        self.setWindowTitle("Settings")

        # self.resize(270, 110)

        vLayout = QVBoxLayout()

        formLayout = QFormLayout()
        self.widgets.intervalMilliseconds = QLineEdit()
        self.widgets.intervalMilliseconds.setText(
            str(existingSettings.intervalMilliseconds))
        formLayout.addRow("Interval (milliseconds) (> 0):",
                          self.widgets.intervalMilliseconds)
        self.widgets.cellNum = QLineEdit()
        self.widgets.cellNum.setText(str(existingSettings.cellNum))
        formLayout.addRow("Cell Num (>= 2):", self.widgets.cellNum)
        self.widgets.checkIsOut = QCheckBox()
        self.widgets.checkIsOut.setChecked(existingSettings.checkIsOut)
        formLayout.addRow("Check is Out", self.widgets.checkIsOut)
        self.widgets.checkIsColliding = QCheckBox()
        self.widgets.checkIsColliding.setChecked(existingSettings.checkIsColliding)
        formLayout.addRow("Check is Colliding", self.widgets.checkIsColliding)

        buttonBox = QDialogButtonBox()
        buttonBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        buttonBox.accepted.connect(self.onAccept)
        buttonBox.rejected.connect(self.onReject)

        vLayout.addLayout(formLayout)
        vLayout.addWidget(QLabel(
            "Clicking Ok button will reset game progress and restart the application"))
        vLayout.addWidget(buttonBox)

        self.setLayout(vLayout)

    def showValidationErrorWarning(self):
        """Inform user that he inputted wrong values"""
        QMessageBox.warning(self, "Validation error",
                            "Please enter correct values")

    def onAccept(self):
        "When users clicks Ok button or presses Enter"
        try:
            settings = t.Settings(
                intervalMilliseconds=int(
                    self.widgets.intervalMilliseconds.text()),
                cellNum=int(self.widgets.cellNum.text()),
                checkIsOut=self.widgets.checkIsOut.isChecked(),
                checkIsColliding=self.widgets.checkIsColliding.isChecked()
            )
            if validateSettings(settings):
                self.settings = settings
                self.accept()
            else:
                raise ValueError
        except ValueError:
            self.showValidationErrorWarning()

    def onReject(self):
        "When users clicks Cancel button or presses Esc"
        self.reject()

    @staticmethod
    def run(existingSettings):
        """Show dialog and return its result"""
        dialog = SettingsDialog(existingSettings)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        result = dialog.exec_()
        return (dialog.settings, result == QDialog.Accepted)


if __name__ == "__main__":
    # Show dialog if this file is run directly (for testing purposes)
    app = QApplication(sys.argv)
    dlg = SettingsDialog(DEFAULT_SETTINGS)
    dlg.show()
    sys.exit(app.exec_())
