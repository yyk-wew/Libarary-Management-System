# !_*_ coding:utf-8 _*_

import sys, database
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class loginDialog(QDialog):

    adminSignal = pyqtSignal(str)

    def __init__(self, database):
        super().__init__()
        self.initUI()
        self.db = database

    def initUI(self):
        self.setWindowTitle('管理员登陆')
        self.resize(300, 150)

        self.label_account = QLabel()
        self.label_account.setText('账号')

        self.lineEdit_account = QLineEdit()
        self.lineEdit_account.setPlaceholderText("请输入账号")

        self.label_pass = QLabel()
        self.label_pass.setText('密码')

        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText("请输入密码")
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("确定")

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("取消")

        self.reslabel = QLabel()

        grid = QVBoxLayout()
        widgetlist = [self.label_account, self.lineEdit_account, self.label_pass, self.lineEdit_password, self.reslabel]
        for i in range(0, 5):
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

    def button_enter(self):
        id = self.lineEdit_account.text()
        password = self.lineEdit_password.text()
        select = database.select_sql('Users', ['UserID', 'Password', 'Name'])
        self.db.execute(select)
        res = self.db.fetch_result(['UserID', 'Password', 'Name'])
        userexist = False
        login = False
        for item in res:
            if item['UserID'] == str(id):
                userexist = True
                if item['Password'] == password:
                    login = True
                    name = item['Name']
                else:
                    login = False
        if userexist:
            if login:
                self.adminSignal.emit(name)
                self.accept()
            else:
                self.reslabel.setText('密码错误')
                self.lineEdit_password.clear()
        else:
            self.reslabel.setText('用户不存在')
            self.lineEdit_password.clear()
            self.lineEdit_account.clear()

    def button_quit(self):
        self.reject()


class readerLoginDialog(QDialog):

    idSignal = pyqtSignal(str)

    def __init__(self, database):
        super().__init__()
        # self.db = database.SQLConn()
        self.db = database
        self.initUI()

    def initUI(self):
        self.setWindowTitle('借书证登入')
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
        self.idSignal.emit(id)
        self.accept()

    def button_quit(self):
        self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = readerLoginDialog()
    if dialog.exec_() == QDialog.Accepted:
        print('yes')
    else:
        print('no')
