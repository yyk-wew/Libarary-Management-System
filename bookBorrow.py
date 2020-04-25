# !_*_ coding:utf-8 _*_

import datetime
import sys, database, login
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class bookBorrowWindow(QWidget):

    readerID = ''
    adminName = ''

    def __init__(self, admin, db):
        super().__init__()
        self.db = db
        # self.db = database.SQLConn()
        self.adminName = admin
        self.initUI()

    def initUI(self):
        # label
        self.label_name  = QLabel()

        # line edit
        self.lineEdit_bookID = QLineEdit()
        self.lineEdit_bookID.setPlaceholderText('请输入书号')

        # push button
        self.button_change = QPushButton()
        self.button_change.setText('切换用户')
        self.button_change.clicked.connect(self.changeUser)

        self.button_borrow = QPushButton()
        self.button_borrow.setText('借书')
        self.button_borrow.clicked.connect(self.bookBorrow)

        # table
        self.table = QTableWidget()

        # layout
        layout = QGridLayout()
        layout.addWidget(self.label_name, 0, 0, 1, 2)
        layout.addWidget(self.button_change, 0, 2, 1, 1)
        layout.addWidget(self.lineEdit_bookID, 0, 3, 1, 2)
        layout.addWidget(self.button_borrow, 0, 5, 1, 1)
        layout.addWidget(self.table, 1, 0, 6, 6)
        self.setLayout(layout)

    def initAdmin(self, admin):
        self.adminName = admin

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
        self.initTable()

    def initTable(self):
        # update record
        conditions = 'CardNo = ' + self.readerID
        select = database.select_sql('LibraryRecords', '*', conditions)
        self.db.execute(select)
        attrlist = ['卡号', '书号', '借出日期', '归还日期', '操作人']
        reslist = self.db.fetch_result(attrlist)
        self.table.setColumnCount(len(attrlist))
        self.table.setRowCount(len(reslist))
        self.table.setHorizontalHeaderLabels(attrlist)
        for i in range(len(attrlist)):
            for j in range(len(reslist)):
                self.table.setItem(j, i, QTableWidgetItem(reslist[j][attrlist[i]]))

    def bookBorrow(self):
        bookID = self.lineEdit_bookID.text()
        select = database.select_sql('Books', ['BookNo', 'BookName', 'Storage'])
        self.db.execute(select)
        resList = self.db.fetch_result(['BookNo', 'BookName', 'Storage'])
        find = False
        for item in resList:
            if bookID == item['BookNo']:
                find = True
                contentStr = '是否要借 ' + item['BookName'] + ' ?'
                reply = QMessageBox.question(self, '借书', contentStr,
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    # already borrow this book
                    conditions = 'CardNo = ' + self.readerID
                    select = database.select_sql('LibraryRecords', ['BookNo'], conditions)
                    self.db.execute(select)
                    res = self.db.fetch_result_list()
                    if bookID in res:
                        QMessageBox.about(self, '借书', '已经借过这本书了')
                        break
                    if int(item['Storage']) > 0:
                        # storage - 1
                        conditions = "BookNo = '" + bookID + "'"
                        update = database.update_sql('Books', 'Storage = Storage - 1', conditions)
                        self.db.execute(update)
                        print('update succeed')
                        # insert record
                        insertList = [self.readerID, bookID, str(datetime.date.today()), self.adminName]
                        for i in range(len(insertList)):
                            insertList[i] = "'" + insertList[i] + "'"
                        insert = database.insert_sql('LibraryRecords', ['CardNo', 'BookNo', 'LentDate', 'Operator'],
                                                     insertList)
                        self.db.execute(insert)
                        self.db.commit()
                        self.initTable()
                        contentStr = '借书成功！'
                    else:
                        contentStr = '库存量不足'
                    QMessageBox.about(self, '借书', contentStr)
                break
        if not find:
            QMessageBox.about(self, '借书', '该书号不存在')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db1 = database.SQLConn()
    window = bookBorrowWindow('admin', db1)
    window.show()
    sys.exit(app.exec_())
