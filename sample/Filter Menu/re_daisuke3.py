from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, qRgb
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, \
    QHBoxLayout, QAbstractItemView, QMenu
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
import numpy as np
from PIL import Image
import os


class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtCore.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0


class CustomQWidget(QWidget, QListWidgetItem):
    def __init__(self, parent=None, item=None, id=0):
        super(CustomQWidget, self).__init__(parent)
        self.item = item
        self.parent_list = parent
        label = QLabel('item' + str(id))
        self.name = 'item' + str(id)
        button = QPushButton('button')
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)


        #############　ここから　#########################################################

        # Brightness
        def get_layout(self, parent):
            super(CustomQWidget, self).__init__(parent)
            label = QLabel(self.get_name())
            self.name = 'Filter' + str(id)
            self.slider = QSlider(Qt.Horizontal, parent)
            self.slider.setRange(-255, 255)
            self.slider.sliderReleased.connect(self.release_mouse)
            layout = QHBoxLayout()
            layout.addWidget(label)
            layout.addWidget(self.slider)
            return layout

        # Liner Filter
        def get_layout(self, parent):
            super(CustomQWidget, self).__init__(parent)
            label = QLabel(self.get_name())
            self.name = 'Filter' + str(id)

            self.mask()

            layout = QHBoxLayout()
            layout.addWidget(label)
            return layout

        # Median Filter
        def get_layout(self, parent):
            super(CustomQWidget, self).__init__(parent)
            label = QLabel(self.get_name())
            self.name = 'Filter' + str(id)

            layout = QHBoxLayout()
            layout.addWidget(label)
            return layout

        # Bilateral Filter
        def get_layout(self, parent):
            super(CustomQWidget, self).__init__(parent)
            label = QLabel(self.get_name())
            self.name = 'Filter' + str(id)

            layout = QHBoxLayout()
            layout.addWidget(label)
            return layout

        # Half Tone Filter
        def get_layout(self, parent):
            super(CustomQWidget, self).__init__(parent)
            label = QLabel(self.get_name())
            self.name = 'Filter' + str(id)

            layout = QHBoxLayout()
            layout.addWidget(label)
            return layout

        # Frequency Filter
        def get_layout(self, parent):
            super(CustomQWidget, self).__init__(parent)
            label = QLabel(self.get_name())
            self.name = 'Filter' + str(id)

            layout = QHBoxLayout()
            layout.addWidget(label)
            return layout


        ################################################################

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.buildContextMenu)
        self.setLayout(layout)

    def buildContextMenu(self, qPoint):
        menu = QMenu(self)
        menulabels = ['Brightness', 'Liner Filter', 'Median Filter', 'Bilateral Filter', 'Half Tone Filter', 'remove']
        actionlist = []
        for label in menulabels:
            actionlist.append(menu.addAction(label))

        action = menu.exec_(self.mapToGlobal(qPoint))
        for act in actionlist:
            if act == action:
                print('  - Menu Label is "%s"' % act.text())
                ac = act.text()
                if (ac == menulabels[0]):
                    self.parent_list.add_item(self)
                if (ac == menulabels[1]):
                    self.parent_list.add_item(self)
                if (ac == menulabels[2]):
                    self.parent_list.add_item(self)
                if (ac == menulabels[3]):
                    self.parent_list.add_item(self)
                if (ac == menulabels[4]):
                    self.parent_list.add_item(self)
                if (ac == menulabels[5]):
                    self.parent_list.remove_item(self)


class Filter_list(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setAlternatingRowColors(True)

        for i in range(10):
            item = QListWidgetItem(self)
            item_widget = CustomQWidget(parent=self, id=i)
            item.setSizeHint(item_widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, item_widget)

    def dropEvent(self, QDropEvent):
        super().dropEvent(QDropEvent)
        for i in self.all_items():
            print(i.name)
        print()

    def add_item(self, item):
        item = QListWidgetItem(self)
        item_widget = CustomQWidget(parent=self, id=0)
        item.setSizeHint(item_widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, item_widget)

    def remove_item(self, item):
        for n, i in enumerate(self.all_items()):
            if i is item:
                t_item = self.takeItem(n)
                t_item = None


    def all_items(self):
        items = []
        for i in range(self.count()):
            item = self.item(i)
            items.append(self.itemWidget(item))
        return items

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)
        bw = 32  # buttonWidth
        iw = 24  # iconWidth
        # 'Load image' button
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setIcon(QtGui.QIcon("../icons/add_files.png"))
        self.btnLoad.setFixedSize(bw, bw)
        self.btnLoad.setIconSize(QtCore.QSize(iw, iw))
        self.btnLoad.clicked.connect(self.fileOpen)
        # 'Export image' button
        self.btnExport = QtWidgets.QToolButton(self)
        self.btnExport.setIcon(QtGui.QIcon("../icons/export.png"))
        self.btnExport.setFixedSize(bw, bw)
        self.btnExport.setIconSize(QtCore.QSize(iw, iw))
        self.btnExport.clicked.connect(self.saveImage)
        # 'Zoom in' button
        self.btnZoomIn = QtWidgets.QToolButton(self)
        self.btnZoomIn.setIcon(QtGui.QIcon("../icons/zoom_in.png"))
        self.btnZoomIn.setFixedSize(bw, bw)
        self.btnZoomIn.setIconSize(QtCore.QSize(iw, iw))
        self.btnZoomIn.clicked.connect(self.zoomIn)
        # 'Zoom out' button
        self.btnZoomOut = QtWidgets.QToolButton(self)
        self.btnZoomOut.setIcon(QtGui.QIcon("../icons/zoom_out.png"))
        self.btnZoomOut.setFixedSize(bw, bw)
        self.btnZoomOut.setIconSize(QtCore.QSize(iw, iw))
        self.btnZoomOut.clicked.connect(self.zoomOut)
        # 'Undo' button
        self.btnUndo = QtWidgets.QToolButton(self)
        self.btnUndo.setIcon(QtGui.QIcon("../icons/undo.png"))
        self.btnUndo.setFixedSize(bw, bw)
        self.btnUndo.setIconSize(QtCore.QSize(iw, iw))
        # self.btnUndo.clicked.connect(   )
        # 'Redo' button
        self.btnRedo = QtWidgets.QToolButton(self)
        self.btnRedo.setIcon(QtGui.QIcon("../icons/redo.png"))
        self.btnRedo.setFixedSize(bw, bw)
        self.btnRedo.setIconSize(QtCore.QSize(iw, iw))
        # self.btnRedo.clicked.connect(   )

        # SideBar
        # self.sideBar = QtWidgets.QScrollArea(self)
        # self.sideBar.setFixedWidth(250)
        # self.sideBar.setWidgetResizable(True)

        self.list=Filter_list()
        self.list.setFixedWidth(250)

        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        TopBar = QtWidgets.QHBoxLayout()
        TopBar.setAlignment(QtCore.Qt.AlignLeft)
        TopBar.addWidget(self.btnLoad)
        TopBar.addStretch(1)
        TopBar.addWidget(self.btnExport)
        VBlayout.addLayout(TopBar)
        MainView = QtWidgets.QHBoxLayout()
        LeftView = QtWidgets.QVBoxLayout()
        LeftView.addWidget(self.viewer)
        EditBar = QtWidgets.QHBoxLayout()
        EditBar.setAlignment(QtCore.Qt.AlignLeft)
        EditBar.addWidget(self.btnZoomIn)
        EditBar.addWidget(self.btnZoomOut)
        EditBar.addWidget(self.btnUndo)
        EditBar.addWidget(self.btnRedo)
        LeftView.addLayout(EditBar)
        MainView.addLayout(LeftView)
        MainView.addWidget(self.list)
        VBlayout.addLayout(MainView)

    def fileOpen(self):
        if os.name == 'nt':
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop",
                                                filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        else:
            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                "./",
                                                filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")

        if fname[0]:
            self.array = np.array(Image.open(fname[0]).convert("RGBA"), np.float32)
            self.update_image(self.array)

    def saveImage(self):
        if os.name == 'nt':
            fname = QFileDialog.getSaveFileName(self, 'Save file',
                                                os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop",
                                                filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        else:
            fname = QFileDialog.getSaveFileName(self, 'Save file',
                                                "./",
                                                filter="JPG(*.jpg);;PNG(*.png);;BMP(*.bmp)")
        if fname[0]:
            pil_img = Image.fromarray(self.array.astype(np.uint8)).convert("RGB")
            pil_img.save(fname[0])

    def update_image(self, array):
        self.viewer.setPhoto(self.ndarray_to_qpixmap(array.astype(np.uint8)))

    def ndarray_to_qpixmap(self, image):
        qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], image.shape[1] * 4,
                              QtGui.QImage.Format_RGBA8888)
        pixmap = QtGui.QPixmap.fromImage(qimage)
        return pixmap

    def zoomIn(self):
        if self.viewer.hasPhoto():
            factor = 1.25
            self.viewer._zoom += 1
            if self.viewer._zoom > 0:
                self.viewer.scale(factor, factor)
            elif self.viewer._zoom == 0:
                self.viewer.fitInView()
            else:
                self.viewer._zoom = 0

    def zoomOut(self):
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

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())