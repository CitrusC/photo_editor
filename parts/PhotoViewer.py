"""
*** File Name           : PhotoViewer.py
*** Designer            : 邱 雨澄
*** Date                : 2018.06.05
*** Function            : 画像表示部分の管理する
"""

from PyQt5 import QtGui, QtWidgets, QtCore

"""
*** Class Name          : PhotoViewer
*** Designer            : 邱 雨澄
*** Date                : 2018.06.05
*** Function            : 画像表示部分の管理
"""


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

    """
    *** Function Name       : has_photo()
    *** Designer            : 邱 雨澄
    *** Date                : 2018.06.05
    *** Function            : 画像がセットされているかを返す
    *** Return              : 画像がセットされているかの真偽値
    """
    def has_photo(self):
        return not self._empty

    """
    *** Function Name       : fitInView()
    *** Designer            : 邱 雨澄
    *** Date                : 2018.06.05
    *** Function            : 画像をウィンドウの幅に合わせる
    *** Return              : なし
    """
    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.has_photo():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                view_rect = self.viewport().rect()
                scene_rect = self.transform().mapRect(rect)
                factor = min(view_rect.width() / scene_rect.width(),
                             view_rect.height() / scene_rect.height())
                self.scale(factor, factor)
            self._zoom = 0

    """
    *** Function Name       : set_photo()
    *** Designer            : 邱 雨澄
    *** Date                : 2018.06.05
    *** Function            : 画像をセットする
    *** Return              : なし
    """
    def set_photo(self, pixmap=None):
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

    """
    *** Function Name       : wheelEvent()
    *** Designer            : 邱 雨澄
    *** Date                : 2018.06.05
    *** Function            : マウスホイールに合わせて、画像を拡大縮小する
    *** Return              : なし
    """
    def wheelEvent(self, event):
        if self.has_photo():
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
