# !_*_ coding:utf-8 _*_

import datetime, re
import sys, database, login
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class bookReturnWindow(QWidget):

    readerID = ''
    admin = ''

    def __init__(self, admin, db):
        super().__init__()
        self.admin = admin
        # self.db = database.SQLConn()
        self.db = db
        self.initUI()

    def initUI(self):
        # label
        self.label_name = QLabel()

        # push button
        self.button_change = QPushButton()
        self.button_change.setText('切换用户')
        self.button_change.clicked.connect(self.changeUser)

        # list
        self.borrowList = QListWidget()
        self.borrowList.itemClicked.connect(self.bookReturn)
        self.initList()

        # layout
        layout = QGridLayout()
        layout.addWidget(self.label_name, 0, 0, 1, 2)
        layout.addWidget(self.button_change, 0, 2, 1, 1)
        layout.addWidget(self.borrowList, 1, 0, 6, 3)
        self.setLayout(layout)

    def initList(self):
        self.borrowList.clear()
        conditions = "LibraryRecords.BookNo = Books.BookNo and LibraryRecords.CardNo = '%s'" % self.readerID
        conditions += " and isNULL(LibraryRecords.ReturnDate)"
        select = database.select_sql('LibraryRecords, Books', ['Books.BookNo', 'BookName'], conditions)
        self.db.execute(select)
        reslist = self.db.fetch_result(['BookNo', 'BookName'])
        mlist = []
        for tup in reslist:
            temp = "%s(%s)" % (tup['BookName'], tup['BookNo'])
            mlist.append(temp)
        self.borrowList.addItems(mlist)

    def initAdmin(self, admin):
        self.admin = admin

    def changeUser(self):
        readerLoginWindow = login.readerLoginDialog(self.db)
        readerLoginWindow.idSignal.connect(self.getReaderID)
        readerLoginWindow.exec_()

    def getReaderID(self, id):
        # update label
        self.readerID = id
        select = database.select_sql('LibraryCard', ['CardNo', 'Name'])
        self.db.execute(select)
        res = self.db.fetch_result(['id', 'Name'])
        for item in res:
            if id == item['id']:
                self.label_name.setText("当前图书证用户： " + item['Name'])
        self.initList()

    def bookReturn(self, item):
        book = item.text()
        b = re.findall(r'[(](.*?)[)]', book)
        bookNo = b[0]
        contentStr = "是否要还 %s ?" % book
        reply = QMessageBox.question(self, '还书', contentStr,
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            # update ReturnDate
            date = str(datetime.date.today())
            conditions = "CardNo = '%s' and BookNo = '%s'" % (self.readerID, bookNo)
            set = "ReturnDate = '%s', Operator = '%s'" % (date, self.admin)
            update = database.update_sql('LibraryRecords', set, conditions)
            self.db.execute(update)
            # update storage
            conditions = "BookNo = '%s'" % bookNo
            update = database.update_sql('Books', "Storage = Storage + 1", conditions)
            self.db.execute(update)
            self.db.commit()
            QMessageBox.about(self, '还书', '还书成功！')
            self.initList()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = database.SQLConn()
    window = bookReturnWindow('admin', db)
    window.show()
    sys.exit(app.exec_())
