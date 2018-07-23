"""
*** File Name           : PhotoEditor.py
*** Designer            : 入力
*** Date                : 2018.07.入力
*** Function            : 入力
"""

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QMenu, QMessageBox, QPushButton, QToolButton, QFileDialog, QAction, QSplitter, QWidget
import numpy as np
import os
from PIL import Image
from FilterList import FilterList
from PhotoViewer import PhotoViewer

"""
*** Class Name          : PhotoViewer
*** Designer            : 邱 雨澄
*** Date                : 2018.07.入力
*** Function            : 入力
"""


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)
        bw = 32  # buttonWidth
        iw = 24  # iconWidth

        self.list = FilterList(self)
        # self.list.setFixedWidth(350)

        # 'Load image' button
        self.btnLoad = QToolButton(self)
        self.btnLoad.setIcon(QtGui.QIcon("icons/load.png"))
        self.btnLoad.setFixedSize(bw, bw)
        self.btnLoad.setIconSize(QtCore.QSize(iw, iw))
        self.btnLoad.clicked.connect(self.file_open)
        # 'Export image' button
        self.btnExport = QToolButton(self)
        self.btnExport.setIcon(QtGui.QIcon("icons/export.png"))
        self.btnExport.setFixedSize(bw, bw)
        self.btnExport.setIconSize(QtCore.QSize(iw, iw))
        self.btnExport.clicked.connect(self.save_image)
        # 'Zoom in' button
        self.btnZoomIn = QToolButton(self)
        self.btnZoomIn.setIcon(QtGui.QIcon("icons/zoom_in.png"))
        self.btnZoomIn.setFixedSize(bw, bw)
        self.btnZoomIn.setIconSize(QtCore.QSize(iw, iw))
        self.btnZoomIn.clicked.connect(self.zoom_in)
        # 'Zoom out' button
        self.btnZoomOut = QToolButton(self)
        self.btnZoomOut.setIcon(QtGui.QIcon("icons/zoom_out.png"))
        self.btnZoomOut.setFixedSize(bw, bw)
        self.btnZoomOut.setIconSize(QtCore.QSize(iw, iw))
        self.btnZoomOut.clicked.connect(self.zoom_out)
        # 'Undo' button
        self.btnUndo = QToolButton(self)
        self.btnUndo.setIcon(QtGui.QIcon("icons/undo.png"))
        self.btnUndo.setFixedSize(bw, bw)
        self.btnUndo.setIconSize(QtCore.QSize(iw, iw))
        self.btnUndo.clicked.connect(self.list.undo)
        self.btnUndo.setEnabled(False)
        # 'Redo' button
        self.btnRedo = QToolButton(self)
        self.btnRedo.setIcon(QtGui.QIcon("icons/redo.png"))
        self.btnRedo.setFixedSize(bw, bw)
        self.btnRedo.setIconSize(QtCore.QSize(iw, iw))
        self.btnRedo.clicked.connect(self.list.redo)
        self.btnRedo.setEnabled(False)
        # 'Add' button
        self.btnAdd = QPushButton(self)
        self.btnAdd.setText("Add")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnAdd.setFont(font)
        self.btnAdd.setFixedSize(bw * 2, bw)
        mapper = QtCore.QSignalMapper(self)
        menulabels = ['Brightness', 'Nega', 'Median', 'Linear', 'FFT2D', 'Grayscale', 'Thiza']
        actions = []
        for f in menulabels:
            action = QAction(self)
            mapper.setMapping(action, f)
            action.setText(f)
            action.triggered.connect(mapper.map)
            actions.append(action)
        mapper.mapped['QString'].connect(self.list.add_event)

        menu = QMenu(self)
        menu.addActions(actions)
        self.btnAdd.setMenu(menu)

        # 'Apply' button
        self.btnApply = QPushButton(self)
        self.btnApply.setText("Apply")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnApply.setFont(font)
        self.btnApply.setFixedSize(bw * 2, bw)
        self.btnApply.clicked.connect(self.list.apply_filters)

        # Arrange layout
        vb_layout = QtWidgets.QVBoxLayout(self)

        top_bar = QtWidgets.QHBoxLayout()
        top_bar.addWidget(self.btnLoad)
        top_bar.addStretch(1)
        top_bar.addWidget(self.btnExport)
        vb_layout.addLayout(top_bar)

        splitter = QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.viewer)
        splitter.addWidget(self.list)
        vb_layout.addWidget(splitter)

        edit_bar = QtWidgets.QHBoxLayout()
        edit_bar.addWidget(self.btnZoomIn)
        edit_bar.addWidget(self.btnZoomOut)
        edit_bar.addWidget(self.btnUndo)
        edit_bar.addWidget(self.btnRedo)
        edit_bar.addStretch(1)
        edit_bar.addWidget(self.btnAdd)
        edit_bar.addWidget(self.btnApply)
        vb_layout.addLayout(edit_bar)


    def file_open(self):
        if os.name == 'nt':
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop",
                                                filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        else:
            fname = QFileDialog.getOpenFileName(self, 'Open file', "./", filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        if fname[0]:
            try:
                self.array = np.array(Image.open(fname[0]).convert("RGBA"), np.float32)
                self.update_image(self.array)
                self.list.init(self.array)
            except AttributeError:
                QMessageBox.critical(self, 'Error', "The image file is broken.", QMessageBox.Ok)

    def save_image(self):
        if os.name == 'nt':
            fname = QFileDialog.getSaveFileName(self, 'Save file',
                                                os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop",
                                                filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        else:
            fname = QFileDialog.getSaveFileName(self, 'Save file', "./", filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        if fname[0]:
            try:
                pil_img = Image.fromarray(self.array.astype(np.uint8)).convert("RGB")
                pil_img.save(fname[0])
            except AttributeError:
                QMessageBox.critical(self, 'Error', "The image file is not selcted.", QMessageBox.Ok)

    def update_image(self, array):
        self.array = array
        self.viewer.set_photo(self.ndarray_to_qpixmap(array.astype(np.uint8)))

    def ndarray_to_qpixmap(self, image):
        qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.shape[1] * 4,
                              QtGui.QImage.Format_RGBA8888)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        return pixmap

    def zoom_in(self):
        if self.viewer.hasPhoto():
            factor = 1.25
            self.viewer._zoom += 1
            if self.viewer._zoom > 0:
                self.viewer.scale(factor, factor)
            elif self.viewer._zoom == 0:
                self.viewer.fitInView()
            else:
                self.viewer._zoom = 0

    def zoom_out(self):
        if self.viewer.hasPhoto():
            factor = 0.8
            self.viewer._zoom -= 1
            if self.viewer._zoom > 0:
                self.viewer.scale(factor, factor)
            elif self.viewer._zoom == 0:
                self.viewer.fitInView()
            else:
                self.viewer._zoom = 0


if __name__ == '__main__':
    import sys

    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())
