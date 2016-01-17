
import sys
from PySide.QtCore import *
from PySide.QtGui import *
import numpy as np


from vision.camera import Camera


cam = Camera(320, 240, id=0)

app = QApplication(sys.argv)


class ImageView(QWidget):
    def __init__(self, shape, parent=None):
        super(ImageView, self).__init__(parent)

        self.image = np.zeros(shape, dtype=np.uint8)
        height, width, byteValue = self.image.shape
        byteValue = byteValue * width
        self.setFixedSize(width, height)

        self.mQImage = QImage(self.image.data, width, height, byteValue, QImage.Format_RGB888)

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        painter.drawImage(0, 0, self.mQImage)
        painter.end()

    def setImage(self, im):
        self.image[:] = im
        self.repaint()

wid = QWidget()
wid.setWindowTitle('Simple')

image_view = ImageView(shape=cam.shape + (3,))
refresh_button = QPushButton("test")

@refresh_button.clicked.connect
def on_click():
    image_view.setImage(cam.read())

image_view.setImage(cam.read())

layout = QVBoxLayout()
layout.addWidget(image_view)
layout.addWidget(refresh_button)
wid.setLayout(layout)

wid.show()


sys.exit(app.exec_())