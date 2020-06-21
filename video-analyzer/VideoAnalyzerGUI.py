import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThreadPool
from windows.Settings import Settings
from windows.ResultWindow import ResultWindow
from Configuration import Configuration
from util.Constants import Constants
from util.Worker import Worker
from analyzer.AnalyzerBuilder import build_analyzer


def show_error():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)

    msg.setText("Weights not valid.")
    msg.setInformativeText("Please go to preferences and set a valid weights file.")
    msg.setWindowTitle("Error")
    msg.setStandardButtons(QMessageBox.Ok)

    msg.exec_()


class VideoAnalyzerMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = Constants.Main.TITLE
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.left = qtRectangle.left()
        self.top = qtRectangle.top()
        self.width = 840
        self.height = 480
        self.config = Configuration()
        self.analyzer = build_analyzer(config=self.config)
        self.threadpool = QThreadPool()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left - 100, self.top, self.width, self.height)

        self.toolbar = self.addToolBar(Constants.Main.TXT_EXIT)
        self.toolbar.addAction(self.build_toolbar_action(Constants.Main.TXT_EXIT, Constants.Main.SHORTCUT_EXIT, qApp.quit))
        self.toolbar.addAction(self.build_toolbar_action(Constants.Main.TXT_LOAD, Constants.Main.SHORTCUT_LOAD, self.open_file))
        self.analyzeAct = self.build_toolbar_action(Constants.Main.TXT_ANALYZE, Constants.Main.SHORTCUT_ANALYZE, self.analyze, True)
        self.toolbar.addAction(self.analyzeAct)
        self.toolbar.addAction(
            self.build_toolbar_action(Constants.Main.TXT_PREFERENCES, Constants.Main.SHORTCUT_PREFERENCES, self.open_settings)
        )

        self.txt_log = QPlainTextEdit(self)
        self.txt_log.move(0, 20)
        self.txt_log.resize(self.width, self.height)
        self.txt_log.horizontalScrollBar()
        self.txt_log.setDisabled(False)

        self.show()

    def build_toolbar_action(self, name, shortcut, action, disabled=False):
        qaction = QAction(name, self)
        qaction.setShortcut(shortcut)
        qaction.triggered.connect(action)
        qaction.setDisabled(disabled)
        return qaction

    def resizeEvent(self, event):
        self.txt_log.resize(event.size())
        QMainWindow.resizeEvent(self, event)

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "QFileDialog.getOpenFileName()",
            "",
            options=options,
            filter="video(*.mp4 *.avi)"
        )
        if fileName:
            self.analyzeAct.setDisabled(False)
            self.txt_log.appendPlainText(f"Loaded video file {fileName}")
            self.file_path = fileName

    def open_settings(self):
        dialog = Settings(self.config)
        dialog.exec_()
        dialog.show()

    def analyze(self):
        if not self.config.valid:
            show_error()
            return
        elif self.config.dirty:
            self._initialize_analyzer_()

        self.analyzeAct.setDisabled(True)
        worker = Worker(self.analyze_video)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)

    def _initialize_analyzer_(self):
        print(f"initialize new analyzer with config {self.config.as_string()}")
        self.txt_log.appendPlainText(f"Current config: {self.config.as_string()}")
        self.analyzer = build_analyzer(self.config)
        self.config.dirty = False

    def analyze_video(self, progress_callback):
        print(f"Analyze video")
        self.workflow_builder, self.workflow, self.workflow_full_frames, self.reference_img = self.analyzer.process(self.file_path, progress_callback)
        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        self.statusBar().showMessage("Progress: COMPLETE")
        self.txt_log.appendPlainText("------------------------------------------")
        self.result = ResultWindow(self.workflow_builder, self.workflow, self.workflow_full_frames, self.reference_img)
        self.result.show()

    def progress_fn(self, n, step):
        if n is not -1:
            self.statusBar().showMessage(f"Progress: {n}%")

        if step:
            self.txt_log.appendPlainText(step)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoAnalyzerMain()
    sys.exit(app.exec_())
