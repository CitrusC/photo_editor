"""
*** File Name           : Filter_list.py
*** Designer            : 入力
*** Date                : 2018.06.05
*** Function            : 入力
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QAbstractItemView, QMenu

from History import History
import Filter

"""
*** Class Name          : FilterList
*** Designer            : 稲垣 大輔
*** Date                : 2018.06.19
*** Function            : FilterItemを管理する
"""


class FilterList(QListWidget):
    def __init__(self, parent_):
        super().__init__()
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setAlternatingRowColors(True)
        self.parent_ = parent_
        self.history = None
        self.id_count = 0

    """
    *** Function Name       : set_array()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : arrayの値をセットする
    *** Return              : なし
    """

    def set_array(self, array):
        self.history = History(array)
        self.clear()

    """
    *** Function Name       : dropEvent()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : フィルタ入れ替えの処理
    *** Return              : なし
    """

    def dropEvent(self, drop_event):
        super().dropEvent(drop_event)
        filters = self.history.swap(self.all_filters())
        self.clear()
        for f in filters:
            self.create_item(f)

    """
    *** Function Name       : add_event()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : フィルタを追加する
    *** Return              : なし
    """

    def add_event(self, f):
        self.add_item(getattr(Filter, f)())

    """
    *** Function Name       : add_item()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : FilterItemを追加する
    *** Return              : なし
    """
    def add_item(self, f):
        f.set_id(self.id_count)
        self.id_count += 1
        self.history.add_filter(f)
        self.create_item(f)

    """
    *** Function Name       : create_item()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : FilterItemを生成する
    *** Return              : なし
    """
    def create_item(self, f):
        item = QListWidgetItem(self)
        item_widget = FilterItem(parent=self, filter_=f)
        f.set_parent(item_widget)
        item_widget.setLayout(f.get_layout())
        item.setSizeHint(item_widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, item_widget)
        self.parent_.btnUndo.setEnabled(True)
        self.parent_.btnRedo.setEnabled(False)

    """
    *** Function Name       : remove_item()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : FilterItemを削除する
    *** Return              : なし
    """
    def remove_item(self, item):
        for n, i in enumerate(self.all_items()):
            if i is item:
                t_item = self.takeItem(n)
                t_item = None
                break
        filters = self.history.remove_filter(item.filter_)
        self.clear()
        for f in filters:
            self.create_item(f)
        self.parent_.btnUndo.setEnabled(True)
        self.parent_.btnRedo.setEnabled(False)

    """
    *** Function Name       : update_item()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : FilterItemを更新する
    *** Return              : なし
    """
    def update_filter(self, fil):
        filters = self.history.update_filter(fil)
        self.clear()
        for f in filters:
            self.create_item(f)

    """
    *** Function Name       : undo()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : FilterListを前の状態に戻す
    *** Return              : なし
    """
    def undo(self):
        array, filters, can_undo = self.history.undo()
        self.parent_.update_image(array)
        self.clear()
        for f in filters:
            print(f.before_image_id, f.after_image_id)
            self.create_item(f)
        self.parent_.btnUndo.setEnabled(can_undo)
        self.parent_.btnRedo.setEnabled(True)

    """
    *** Function Name       : redo()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : FilterListを次の状態に進める
    *** Return              : なし
    """
    def redo(self):
        array, filters, can_redo = self.history.redo()
        self.parent_.update_image(array)
        self.clear()
        for f in filters:
            self.create_item(f)
        self.parent_.btnUndo.setEnabled(True)
        self.parent_.btnRedo.setEnabled(can_redo)

    """
    *** Function Name       : apply_filters()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : FilterListのFilterを適用する
    *** Return              : なし
    """
    def apply_filters(self):
        if self.history is None:
            return
        array, filters = self.history.apply()
        self.parent_.update_image(array)
        self.clear()
        for f in filters:
            self.create_item(f)
        self.parent_.btnUndo.setEnabled(True)

    """
    *** Function Name       : all_filters()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : すべてのフィルタを返す
    *** Return              : フィルタリスト
    """
    def all_filters(self):
        filters = []
        for i in self.all_items():
            filters.append(i.filter_)
        return filters

    """
    *** Function Name       : create_item()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : すべてのFilterItemを返す
    *** Return              : FilterItemリスト
    """
    def all_items(self):
        items = []
        for i in range(self.count()):
            item = self.item(i)
            items.append(self.itemWidget(item))
        return items


"""
*** Class Name          : FilterItem
*** Designer            : 稲垣 大輔
*** Date                : 2018.06.19
*** Function            : フィルタとそのレイアウトを管理する
"""
class FilterItem(QWidget, QListWidgetItem):
    def __init__(self, parent=None, filter_=None):
        super(FilterItem, self).__init__(parent)
        self.filter_ = filter_
        self.parent_list = parent
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.build_context_menu)

    """
    *** Function Name       : set_layout()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : レイアウトをセットする
    *** Return              : なし
    """
    def setLayout(self, layout):
        super().setLayout(layout)

    """
    *** Function Name       : build_context_menu()
    *** Designer            : 稲垣 大輔
    *** Date                : 2018.06.19
    *** Function            : 右クリック時のメニューを表示する
    *** Return              : なし
    """
    def build_context_menu(self, q_point):
        menu = QMenu(self)
        menulabels = ['remove']
        actionlist = []
        for label in menulabels:
            actionlist.append(menu.addAction(label))

        action = menu.exec_(self.mapToGlobal(q_point))
        for act in actionlist:
            if act == action:
                ac = act.text()
                if (ac == menulabels[0]):
                    self.parent_list.remove_item(self)
