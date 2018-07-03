import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QLabel, QPushButton, QListWidgetItem, \
    QHBoxLayout, QAbstractItemView, QMenu
from PyQt5 import QtCore


class CustomQWidget(QWidget, QListWidgetItem):

    def __init__(self, parent=None, item=None, id=0):
        super(CustomQWidget, self).__init__(parent)
        self.item = item
        self.parent_list = parent
        label = QLabel('Add a New Filter')
        self.name = 'item' + str(id)
        button = QPushButton('Add')
        button2 = QPushButton('Apply')
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        layout.addWidget(button2)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.buildContextMenu)
        self.setLayout(layout)

    # def __init__(self, parent=None, item=None, id=0):
    #     super(CustomQWidget, self).__init__(parent)
    #     self.item = item
    #     self.parent_list = parent
    #     label = QLabel('item ' + str(id))
    #     self.name = 'item' + str(id)
    #     button = QPushButton('×')
    #     layout = QHBoxLayout()
    #     layout.addWidget(label)
    #     layout.addWidget(button)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.buildContextMenu)
        self.setLayout(layout)

    def buildContextMenu(self, qPoint):
        menu = QMenu(self)
        menulabels = ['add', 'remove']
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
                    self.parent_list.remove_item(self)


class Filter_list(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragDropMode(QAbstractItemView.InternalMove)

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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        title = QLabel("Demo for widgets in a QListWidget")

        list = Filter_list()

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(title)
        window_layout.addWidget(list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())