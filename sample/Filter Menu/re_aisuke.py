import sys
from PyQt5.QtWidgets \
import QApplication, QWidget, QListWidget, QVBoxLayout, QLabel,\
       QPushButton, QListWidgetItem, QHBoxLayout, QAbstractItemView


class CustomQWidget(QWidget):

    def __init__(self, parent = None, id = 0):
        super(CustomQWidget, self).__init__(parent)
        label = QLabel('Filter ' + str(id))
        button = QPushButton("×")
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        title = QLabel("Sort the Filters. If You Want to Add Filter, Right Click is Required.")

        list = QListWidget()
        list.setDragDropMode(QAbstractItemView.InternalMove)

        for i in range(10):
            item = QListWidgetItem(list)
            item_widget = CustomQWidget(id=i)
            item.setSizeHint(item_widget.sizeHint())
            list.addItem(item)
            list.setItemWidget(item, item_widget)

        window_layout = QVBoxLayout(self)
        window_layout.addWidget(title)
        window_layout.addWidget(list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())