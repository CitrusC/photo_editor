"""
*** File Name           : Filter_list.py
*** Designer            : 入力
*** Date                : 2018.07.入力
*** Function            : 入力
"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QAbstractItemView, QMenu

from History import History
import Filter


class FilterList(QListWidget):
    def __init__(self, parent_):
        super().__init__()
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setAlternatingRowColors(True)
        self.parent_ = parent_
        self.history = None
        self.id_count = 0

    def init(self, array):
        self.history = History(array)
        self.clear()

    def dropEvent(self, drop_event):
        super().dropEvent(drop_event)
        filters = self.history.swap(self.all_filters())
        self.clear()
        for f in filters:
            self.add_filter(f)

    def add_event(self, f):
        self.add_item(getattr(Filter, f)())

    def add_item(self, f):
        f.set_id(self.id_count)
        self.id_count += 1
        self.history.add_filter(f)
        self.add_filter(f)

    def add_filter(self, f):
        item = QListWidgetItem(self)
        item_widget = CustomQWidget(parent=self, filter_=f)
        f.set_parent(item_widget)
        item_widget.setLayout(f.get_layout())
        item.setSizeHint(item_widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, item_widget)
        self.parent_.btnUndo.setEnabled(True)
        self.parent_.btnRedo.setEnabled(False)

    def remove_item(self, item):
        for n, i in enumerate(self.all_items()):
            if i is item:
                t_item = self.takeItem(n)
                t_item = None
                break
        filters = self.history.remove_filter(item.filter_)
        self.clear()
        for f in filters:
            self.add_filter(f)
        self.parent_.btnUndo.setEnabled(True)
        self.parent_.btnRedo.setEnabled(False)

    def update_filter(self, fil):
        filters = self.history.update_filter(fil)
        self.clear()
        for f in filters:
            self.add_filter(f)

    def undo(self):
        array, filters, can_undo = self.history.undo()
        self.parent_.update_image(array)
        self.clear()
        for f in filters:
            print(f.before_image_id, f.after_image_id)
            self.add_filter(f)
        self.parent_.btnUndo.setEnabled(can_undo)
        self.parent_.btnRedo.setEnabled(True)

    def redo(self):
        array, filters, can_redo = self.history.redo()
        self.parent_.update_image(array)
        self.clear()
        for f in filters:
            self.add_filter(f)
        self.parent_.btnUndo.setEnabled(True)
        self.parent_.btnRedo.setEnabled(can_redo)

    def apply_filters(self):
        if self.history is None:
            return
        array, filters = self.history.apply()
        self.parent_.update_image(array)
        self.clear()
        for f in filters:
            self.add_filter(f)
        self.parent_.btnUndo.setEnabled(True)

    def all_filters(self):
        filters = []
        for i in self.all_items():
            filters.append(i.filter_)
        return filters

    def all_items(self):
        items = []
        for i in range(self.count()):
            item = self.item(i)
            items.append(self.itemWidget(item))
        return items


class CustomQWidget(QWidget, QListWidgetItem):
    def __init__(self, parent=None, filter_=None):
        super(CustomQWidget, self).__init__(parent)
        self.filter_ = filter_
        self.parent_list = parent
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.build_context_menu)

    def setLayout(self, layout):
        super().setLayout(layout)

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
