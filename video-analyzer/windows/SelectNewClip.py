import random, sys
import cv2
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def convert_to_qt(img):
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(convert_to_qt_format)


class SelectNewClip(QMainWindow):

    def __init__(self, parent=None, reference_img=None, callback=None):

        QMainWindow.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.callback = callback

        wid = QWidget()

        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        image_frame = QLabel()
        image_frame.setPixmap(convert_to_qt(reference_img))
        hbox.addWidget(image_frame)
        wid.setLayout(hbox)
        self.setCentralWidget(wid)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.callback(self.rubberBand.geometry())
        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()
        self.close()
