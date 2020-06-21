from PyQt5.QtWidgets import (QPushButton, QDialog, QDialogButtonBox, QFormLayout, QGroupBox, QLabel,
                             QCheckBox, QVBoxLayout, QFileDialog, QRadioButton)
from util.Constants import Constants


class Settings(QDialog):

    def __init__(self, config):
        super(Settings, self).__init__()
        self.config = config
        self.createFormGroupBox()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Settings")

    def accept(self):
        self.config.debug = self.debugChb.isChecked()
        self.config.siamese_nn_weights = self.siamWeightsLabel.text()
        self.config.mask_rcnn_weights = self.maskWeightsLabel.text()

        if self.siamActive.isChecked():
            self.config.active_solution = Constants.DETECTOR_SOLUTION_SIAM
        else:
            self.config.active_solution = Constants.DETECTOR_SOLUTION_MASK
        self.close()

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox(Constants.Settings.TXT_SETTINGS)
        layout = QFormLayout()

        self.debugChb = QCheckBox(self.config.debug)
        if self.config.debug == Constants.Settings.AKTIV:
            self.debugChb.setChecked(True)
        layout.addRow(QLabel(Constants.Settings.TXT_DEBUG), self.debugChb)

        self.siamWeightsLabel = QLabel(self.config.siamese_nn_weights)
        layout.addRow(QLabel(Constants.Settings.TXT_SIAM_WEIGHTS), self.siamWeightsLabel)
        layout.addRow(QLabel(Constants.TXT_EMPTY), self.build_push_btn(Constants.Settings.BTN_SIAM_WEIGHTS, self.choose_siam_weights))

        self.maskWeightsLabel = QLabel(self.config.mask_rcnn_weights)
        layout.addRow(QLabel(Constants.Settings.TXT_MASK_WEIGHTS), self.maskWeightsLabel)
        layout.addRow(QLabel(Constants.TXT_EMPTY), self.build_push_btn(Constants.Settings.BTN_MASK_WEIGHTS, self.choose_mask_weights))

        self.maskActive = QRadioButton(Constants.DETECTOR_SOLUTION_MASK)
        self.siamActive = QRadioButton(Constants.DETECTOR_SOLUTION_SIAM)
        if self.config.active_solution == Constants.DETECTOR_SOLUTION_MASK:
            self.maskActive.setChecked(True)
            self.siamActive.setChecked(False)
        else:
            self.maskActive.setChecked(False)
            self.siamActive.setChecked(True)

        layout.addRow(QLabel(Constants.Settings.TXT_SOLUTION), self.maskActive)
        layout.addRow(QLabel(Constants.TXT_EMPTY), self.siamActive)
        self.formGroupBox.setLayout(layout)

    def choose_siam_weights(self):
        print("Choosing new weights siam")
        weights = self.select_weights_file()
        self.siamWeightsLabel.setText(weights)

    def choose_mask_weights(self):
        print("Choosing new weights mask")
        weights = self.select_weights_file()
        self.maskWeightsLabel.setText(weights)

    def build_push_btn(self, label, func):
        btn = QPushButton(label)
        btn.clicked.connect(func)
        return btn

    def select_weights_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            options=options,
            filter="weights(*.h5)"
        )

        return fileName
