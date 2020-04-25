# !_*_ coding:utf-8 _*_

import datetime, re
import sys, database, login
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class manageIDWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        # self.db = database.SQLConn()
        self.initUI()

    def initUI(self):
        # push button
        self.button_add = QPushButton()
        self.button_add.setText('添加借书证')
        self.button_add.clicked.connect(self.addID)

        self.button_delete = QPushButton()
        self.button_delete.setText("删除借书证")
        self.button_delete.clicked.connect(self.deleteID)

        self.button_view = QPushButton()
        self.button_view.setText('查看借书证')
        self.button_view.clicked.connect(self.viewID)

        # table
        self.table = QTableWidget()

        # layout
        layout = QGridLayout()
        layout.addWidget(self.button_add, 0, 0, 1, 1)
        layout.addWidget(self.button_delete, 0, 1, 1, 1)
        layout.addWidget(self.button_view, 0, 2, 1, 1)
        layout.addWidget(self.table, 1, 0, 3, 3)
        self.setLayout(layout)

    def initTable(self):
        self.table.clear()
        select = database.select_sql('LibraryCard', '*')
        self.db.execute(select)
        attrlist = ['卡号', '姓名', '单位', '类别', '更新时间']
        reslist = self.db.fetch_result(attrlist)
        print(reslist)
        self.table.setColumnCount(len(attrlist))
        self.table.setRowCount(len(reslist))
        self.table.setHorizontalHeaderLabels(attrlist)
        for i in range(len(reslist)):
            for j in range(len(attrlist)):
                self.table.setItem(i, j, QTableWidgetItem(reslist[i][attrlist[j]]))

    def addID(self):
        Dialog = addIDDialog(self.db)
        Dialog.exec_()

    def deleteID(self):
        Dialog = deleteIDDialog(self.db)
        Dialog.exec_()

    def viewID(self):
        self.initTable()


class addIDDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        # self.db = database.SQLConn()
        self.initUI()

    def initUI(self):
        # lineEdit
        self.lineEdit_ID = QLineEdit()
        self.lineEdit_ID.setPlaceholderText("请输入卡号")
        self.lineEdit_name = QLineEdit()
        self.lineEdit_name.setPlaceholderText("请输入姓名")
        self.lineEdit_department = QLineEdit()
        self.lineEdit_department.setPlaceholderText("请输入单位")
        self.lineEdit_type = QLineEdit()
        self.lineEdit_type.setPlaceholderText("请输入类别")

        # push button
        self.button_enter = QPushButton()
        self.button_enter.setText("确定")
        self.button_enter.clicked.connect(self.enter)
        self.button_quit = QPushButton()
        self.button_quit.setText("取消")
        self.button_quit.clicked.connect(self.quit)

        # layout
        Flayout = QFormLayout()
        Flayout.addRow("CardID", self.lineEdit_ID)
        Flayout.addRow("Name", self.lineEdit_name)
        Flayout.addRow("Department", self.lineEdit_department)
        Flayout.addRow("Type", self.lineEdit_type)
        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.button_enter)
        Hlayout.addWidget(self.button_quit)
        Vlayout = QVBoxLayout()
        Vlayout.addLayout(Flayout)
        Vlayout.addLayout(Hlayout)
        self.setLayout(Vlayout)

    def enter(self):
        # check integrity
        id = self.lineEdit_ID.text()
        select = database.select_sql('LibraryCard', ['CardNo'])
        self.db.execute(select)
        resList = self.db.fetch_result_list()
        if id in resList:
            QMessageBox.about(self, '借书证管理', '用户名已存在')
            return

        # check NULL
        name = self.lineEdit_name.text()
        type = self.lineEdit_type.text()
        department = self.lineEdit_department.text()
        if name == '':
            QMessageBox.about(self, '借书证管理', '姓名不能为空')
            return
        if type == '':
            QMessageBox.about(self, '借书证管理', '类别不能为空')
            return
        if department == '':
            QMessageBox.about(self, '借书证管理', '单位不能为空')
            return

        # insert
        attrList = ['CardNo', 'Name', 'Department', 'CardType', 'UpdateTime']
        insertList = [id, name, department, type, str(datetime.date.today())]
        for i in range(len(insertList)):
            insertList[i] = "'" + insertList[i] + "'"
        insert = database.insert_sql('LibraryCard', attrList, insertList)
        self.db.execute(insert)
        self.db.commit()
        QMessageBox.about(self, '借书证管理', '借书证增加成功！')
        self.accept()

    def quit(self):
        self.reject()


class deleteIDDialog(QDialog):
    def __init__(self, database):
        super().__init__()
        # self.db = database.SQLConn()
        self.db = database
        self.initUI()

    def initUI(self):
        self.setWindowTitle('借书证删除')
        self.resize(300, 150)

        self.label_account = QLabel()
        self.label_account.setText('借书证号')

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入借书证号")
        self.lineEdit_account.textChanged.connect(self.accountChanged)

        self.label_name = QLabel()
        self.label_name.setText("姓名:")

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("确定")
        self.pushButton_enter.setEnabled(False)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("取消")

        self.cardList = self.initLibraryCard()

        grid = QVBoxLayout()
        widgetlist = [self.label_account, self.lineEdit_account, self.label_name]
        for i in range(len(widgetlist)):
            grid.addWidget(widgetlist[i])
        gridButton = QHBoxLayout()
        gridButton.addWidget(self.pushButton_enter)
        gridButton.addWidget(self.pushButton_quit)
        grid.addLayout(gridButton)
        grid.setSpacing(20)
        grid.setContentsMargins(50, 30, 50, 30)
        self.setLayout(grid)

        self.pushButton_enter.clicked.connect(self.button_enter)
        self.pushButton_quit.clicked.connect(self.button_quit)

    def accountChanged(self):
        self.pushButton_enter.setEnabled(False)
        self.label_name.setText("姓名：  ")
        id = self.lineEdit_account.text()
        for item in self.cardList:
            if id == item['CardNo']:
                self.label_name.setText('姓名：   ' + item['Name'])
                self.pushButton_enter.setEnabled(True)

    def initLibraryCard(self):
        select = database.select_sql('LibraryCard', '*')
        self.db.execute(select)
        res = self.db.fetch_result(['CardNo', 'Name', 'Department', 'CardType', 'UpdateTime'])
        return res

    def button_enter(self):
        id = self.lineEdit_account.text()
        # delete
        conditions = "CardNo = '%s'" % id
        delete = database.delete_sql('LibraryCard', conditions)
        self.db.execute(delete)
        self.db.commit()
        QMessageBox.about(self, '借书证删除', '借书证删除成功！')
        self.accept()

    def button_quit(self):
        self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = manageIDWindow()
    window.show()
    sys.exit(app.exec_())
