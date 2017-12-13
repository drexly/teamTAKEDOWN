from PyQt4.QtCore import QCoreApplication, Qt
from PyQt4.QtGui import QListWidget, QListWidgetItem, QApplication

import sys

class MyList(QListWidget):
    def __init__(self):
        QListWidget.__init__(self)
        self.add_items()
        self.itemClicked.connect(self.item_click)

    def add_items(self):
        for item_text in ['item1', 'item2', 'item3']:
            item = QListWidgetItem(item_text)
            self.addItem(item)

    def item_click(self, item):
        print item, str(item.text())

if __name__ == '__main__':
    app = QApplication([])
    myList = MyList()
    myList.show()
    sys.exit(app.exec_())
