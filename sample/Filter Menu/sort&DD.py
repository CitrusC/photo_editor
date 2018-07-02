import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QListWidget, QAbstractItemView

class Widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.widget_layout = QVBoxLayout()

        # Create ListWidget and add 10 items to move around.
        self.list_widget = QListWidget()
        for x in range(1, 11):
            self.list_widget.addItem('Item {:02d}'.format(x))
            # self.list_widget.setSizeHint(Qsize(50,50))
            self.list_widget.setItemWidget(self, list_widget, '×')
            # self.list_widget.addI

        # # add delete button.
        # for x in range(1, 11):
        #     self.list_widget.addButon()
        #     self.clicked.connect(self.deleteButtonClicked)

        # Enable drag & drop ordering of items.
        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)

        self.widget_layout.addWidget(self.list_widget)
        self.setLayout(self.widget_layout)

    # def deleteButtonClicked
    #     delete item



if __name__ == '__main__':
  app = QApplication(sys.argv)
  widget = Widget()
  widget.show()

  sys.exit(app.exec_())