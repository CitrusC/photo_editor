import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QListWidget, QAbstractItemView

class Widget(QWidget):
    def __init__(self, parent=None):

        QWidget.__init__(self, parent)

        self.widget_layout = QVBoxLayout()

        # Create ListWidget and add 10 items to move around.
        self.list_widget = QListWidget()
        for x in range(1, 11):

            # リストを追加
            self.list_widget.addItem('Item {:02d}'.format(x))

            # リサイズ
            # self.list_widget.setSizeHint(Qsize(50,50))

        # # 右クリックでメニュー表示
        self.list_widget.itemDoubleClicked(self.list_widget)

            # リストの右側に×ボタン表示（クリックしたら削除→deleteButtonClickedへ）
            # self.list_widget.setItemWidget(self, format(x), '×')


        # # add delete button.
        # for x in range(1, 11):
        #     self.list_widget.addButton()
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