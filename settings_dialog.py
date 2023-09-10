"""Settings dialog."""

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
    """PyQt dialog that is being opened from snake game."""

    settings: t.Settings = None

    # Put all inputs inside the scope
    inputs = Munch()

    def __init__(self, existingSettings):
        """
        Create UI elements and connect them to handler functions.

        @param existingSettings: existing settings read from disk
        """
        super().__init__()

        # self.setModal(True)

        self.setWindowTitle("Settings")

        # self.resize(270, 110)

        vLayout = QVBoxLayout()

        formLayout = QFormLayout()
        self.inputs.intervalMilliseconds = QLineEdit()
        self.inputs.intervalMilliseconds.setText(
            str(existingSettings.intervalMilliseconds))
        formLayout.addRow("Interval (milliseconds) (> 0):",
                          self.inputs.intervalMilliseconds)
        self.inputs.cellNum = QLineEdit()
        self.inputs.cellNum.setText(str(existingSettings.cellNum))
        formLayout.addRow("Cell Num (>= 2):", self.inputs.cellNum)
        self.inputs.checkIsOut = QCheckBox()
        self.inputs.checkIsOut.setChecked(existingSettings.checkIsOut)
        formLayout.addRow("Check is Out", self.inputs.checkIsOut)
        self.inputs.checkIsColliding = QCheckBox()
        self.inputs.checkIsColliding.setChecked(existingSettings.checkIsColliding)
        formLayout.addRow("Check is Colliding", self.inputs.checkIsColliding)
        self.inputs.disableTimer = QCheckBox()
        self.inputs.disableTimer.setChecked(existingSettings.disableTimer)
        formLayout.addRow("Disable timer", self.inputs.disableTimer)

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
        """Inform user that he inputted wrong values."""
        QMessageBox.warning(self, "Validation error",
                            "Please enter correct values")

    def onAccept(self):
        """When users clicks Ok button or presses Enter."""
        try:
            settings = t.Settings(
                intervalMilliseconds=int(
                    self.inputs.intervalMilliseconds.text()),
                cellNum=int(self.inputs.cellNum.text()),
                checkIsOut=self.inputs.checkIsOut.isChecked(),
                checkIsColliding=self.inputs.checkIsColliding.isChecked(),
                disableTimer=self.inputs.disableTimer.isChecked()
            )
            if validateSettings(settings):
                self.settings = settings
                self.accept()
            else:
                raise ValueError
        except ValueError:
            self.showValidationErrorWarning()

    def onReject(self):
        """When users clicks Cancel button or presses Esc."""
        self.reject()

    @staticmethod
    def run(existingSettings):
        """
        Show dialog and return its result.

        @param existingSettings: existing settings read from disk
        """
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
