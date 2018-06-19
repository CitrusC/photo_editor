from PyQt5 import QtCore, QtGui, QtWidgets


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


# def toggleDragMode(self):
    #     if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
    #         self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
    #     elif not self._photo.pixmap().isNull():
    #         self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    # def mousePressEvent(self, event):
    #     if self._photo.isUnderMouse():
    #         self.photoClicked.emit(QtCore.QPoint(event.pos()))
    #     super(PhotoViewer, self).mousePressEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)
        bw = 32                     # buttonWidth
        iw = 24                     # iconWidth
        # 'Load image' button
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setIcon(QtGui.QIcon("../icons/add_files.png"))
        self.btnLoad.setFixedSize(bw, bw)
        self.btnLoad.setIconSize(QtCore.QSize(iw, iw))
        self.btnLoad.clicked.connect(self.loadImage)
        # 'Export image' button
        self.btnExport = QtWidgets.QToolButton(self)
        self.btnExport.setIcon(QtGui.QIcon("../icons/export.png"))
        self.btnExport.setFixedSize(bw, bw)
        self.btnExport.setIconSize(QtCore.QSize(iw, iw))
        # self.btnExport.clicked.connect(   )
        # 'Zoom in' button
        self.btnZoomIn = QtWidgets.QToolButton(self)
        self.btnZoomIn.setIcon(QtGui.QIcon("../icons/zoom_in.png"))
        self.btnZoomIn.setFixedSize(bw, bw)
        self.btnZoomIn.setIconSize(QtCore.QSize(iw, iw))
        # self.btnZoomIn.clicked.connect(self.zoomIn)
        # 'Zoom out' button
        self.btnZoomOut = QtWidgets.QToolButton(self)
        self.btnZoomOut.setIcon(QtGui.QIcon("../icons/zoom_out.png"))
        self.btnZoomOut.setFixedSize(bw, bw)
        self.btnZoomOut.setIconSize(QtCore.QSize(iw, iw))
        # self.btnExport.clicked.connect(self.zoomOut)
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
        EditBar = QtWidgets.QHBoxLayout()
        EditBar.setAlignment(QtCore.Qt.AlignLeft)
        EditBar.addWidget(self.btnZoomIn)
        EditBar.addWidget(self.btnZoomOut)
        EditBar.addWidget(self.btnUndo)
        EditBar.addWidget(self.btnRedo)
        VBlayout.addWidget(self.viewer)
        VBlayout.addLayout(EditBar)
        MainView.addLayout(LeftView)
        # MainView.addWidget(SideBar)
        VBlayout.addLayout(MainView)

    def loadImage(self):
        self.viewer.setPhoto(QtGui.QPixmap('IMG_7843.jpg'))


    def zoomIn(self):
        if PhotoViewer.hasPhoto(self):
            factor = 1.25
            PhotoViewer._zoom += 1
            if PhotoViewer._zoom > 0:
                PhotoViewer.scale(factor, factor)
            elif PhotoViewer._zoom == 0:
                PhotoViewer.fitInView()
            else:
                PhotoViewer._zoom = 0

    def zoomOut(self):
        if PhotoViewer.hasPhoto(self):
            factor = 0.8
            PhotoViewer._zoom -= 1
            if PhotoViewer._zoom > 0:
                PhotoViewer.scale(factor, factor)
            elif PhotoViewer._zoom == 0:
                PhotoViewer.fitInView()
            else:
                PhotoViewer._zoom = 0

    # def pixInfo(self):
    #     self.viewer.toggleDragMode()

    # def photoClicked(self, pos):
    #     if self.viewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
    #         self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())