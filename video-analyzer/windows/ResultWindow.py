import os
import cv2
import webbrowser

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget, QLabel, QPushButton, QAction, QFileDialog
from analyzer.VideoAnalyzerResultWriter import write_full_frames, write_html, write_replay_file
from windows.SelectNewClip import SelectNewClip
from util.Constants import Constants


def convert_cv_qt(cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(convert_to_qt_format)


class ResultWindow(QMainWindow):

    def __init__(self, workfow_builder, workflow, workflow_full_frames, reference_img):
        super().__init__()

        self.workflow = workflow
        self.workflow_full_frames = workflow_full_frames
        self.workflow_builder = workfow_builder
        self.reference_img = reference_img

        self.setWindowTitle(Constants.Result.TITLE)
        self.setGeometry(10, 30, 600, 400)

        self.build_toolbar()
        self.build_content()
        self.as_html = workfow_builder.as_html()

    def build_content(self):
        grid = QGridLayout()
        wid = QWidget()
        wid.setLayout(grid)
        self.setCentralWidget(wid)

        row = 0
        for img_name, img in self.workflow:
            image_frame = QLabel()
            image_frame.setPixmap(convert_cv_qt(img))
            grid.addWidget(image_frame, row, 1)
            remove_frame_btn = QPushButton(Constants.Result.BTN_REMOVE)
            remove_frame_btn.clicked.connect(lambda state, x=img_name: self.remove_frame(x))
            grid.addWidget(remove_frame_btn, row, 2)
            select_new_clip_btn = QPushButton(Constants.Result.BTN_SELECT)

            select_new_clip_btn.clicked.connect(lambda state, x=row: self.select_new_for(x))
            grid.addWidget(select_new_clip_btn, row, 3)
            row += 1

    def remove_frame(self, img_name):
        self.workflow = [i for i in self.workflow if i[0] is not img_name]
        self.build_content()

    def select_new_for(self, row):
        self.row = row
        self.new_clip = SelectNewClip(self, self.reference_img, self.selected)
        self.new_clip.show()

    def selected(self, rect: QRect):
        x = rect.getRect()[0]
        y = rect.getRect()[1]
        width = rect.getRect()[2]
        height = rect.getRect()[3]
        img = self.reference_img[y:y + height, x:x + width, :]

        self.workflow[self.row] = (self.workflow[self.row][0], img)
        self.build_content()

    def build_toolbar(self):
        save_action = QAction(Constants.Result.TOOLBAR_SAVE, self)
        save_action.setShortcut(Constants.Result.SHORTCUT_SAVE)
        save_action.triggered.connect(self.save)

        open_browser_action = QAction(Constants.Result.TOOLBAR_OPEN_BROWSER, self)
        open_browser_action.setShortcut(Constants.Result.SHORTCUT_OPEN_BROWSER)
        open_browser_action.triggered.connect(self.open_in_browser)

        self.save_html = False
        toggleHTML = QAction(Constants.Result.TOOLBAR_OPEN_BROWSER, self)
        toggleHTML.setCheckable(True)
        toggleHTML.triggered.connect(self.toggle_html)

        self.save_full_frames = False
        toggleFullFrames = QAction(Constants.Result.TOOLBAR_EXPORT_FRAMES, self)
        toggleFullFrames.setCheckable(True)
        toggleFullFrames.triggered.connect(self.toggle_full_frames)

        self.toolbar = self.addToolBar(Constants.TXT_EMPTY)
        self.toolbar.addAction(save_action)
        self.toolbar.addAction(open_browser_action)
        self.toolbar.addAction(toggleHTML)
        self.toolbar.addAction(toggleFullFrames)

    def closeEvent(self, QCloseEvent):
        for img_name, _ in self.workflow:
            if os.path.exists(img_name):
                os.remove(img_name)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)

    def toggle_html(self):
        self.save_html = not self.save_html

    def toggle_full_frames(self):
        self.save_full_frames = not self.save_full_frames

    def save(self):
        target_dir = str(QFileDialog.getExistingDirectory(self, Constants.Result.TXT_SELECT_DIR))
        if target_dir:
            if self.save_html:
                write_html(target_dir, self.workflow_builder.as_html(), self.workflow)

            if self.save_full_frames:
                write_full_frames(target_dir, self.workflow_full_frames)

            write_replay_file(target_dir, self.workflow_builder.as_xml(), self.workflow)
            self.statusBar().showMessage(f"SAVED to {target_dir}")

    def open_in_browser(self):
        for img_name, img in self.workflow:
            cv2.imwrite(img_name, img)

        f = open('workflow.html', 'w')
        f.write(self.as_html)
        f.close()
        filename = 'file:///' + os.getcwd() + '/' + 'workflow.html'
        webbrowser.open_new_tab(filename)
