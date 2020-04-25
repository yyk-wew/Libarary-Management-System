# !_*_ coding:utf-8 _*_

import sys, login, database, bookQuery, bookBorrow, bookReturn, manageID, bookBase
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class myMainWindow(QWidget):

    admin = ''
    admin2borrow = pyqtSignal(str)
    admin2return = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.db = database.SQLConn()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 50, 600, 600)
        self.setWindowTitle("图书管理系统")

        # navigation
        self.navigation = QStackedWidget()
        self.init_navigation()
        self.navigation.setCurrentIndex(0)

        # stack widget
        self.stack_NULL_0 = QWidget()
        self.stack_query_1 = bookQuery.bookQueryWindow(self.db)
        self.stack_borrow_2 = bookBorrow.bookBorrowWindow(self.admin, self.db)
        self.admin2borrow.connect(self.stack_borrow_2.initAdmin)
        self.stack_return_3 = bookReturn.bookReturnWindow(self.admin, self.db)
        self.admin2return.connect(self.stack_return_3.initAdmin)
        self.stack_card_4 = manageID.manageIDWindow(self.db)
        self.stack_base_5 = bookBase.bookBaseWindow(self.db)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.stack_NULL_0)
        self.stack.addWidget(self.stack_query_1)
        self.stack.addWidget(self.stack_borrow_2)
        self.stack.addWidget(self.stack_return_3)
        self.stack.addWidget(self.stack_card_4)
        self.stack.addWidget(self.stack_base_5)
        self.stack.setCurrentIndex(0)

        # status bar
        self.label_status = QLabel()
        self.label_status.setAlignment(Qt.AlignCenter)
        self.label_status.setText('欢迎！')

        # layout
        Box = QGridLayout()
        Box.addWidget(self.navigation, 0, 0, 12, 2)
        Box.addWidget(self.stack, 0, 2, 12, 10)
        Box.addWidget(self.label_status, 12, 0, 1, 12)
        self.setLayout(Box)

    def init_navigation(self):
        # before login
        self.navigation_visitor_0 = QWidget()
        self.init_nav_visitor()
        self.navigation.addWidget(self.navigation_visitor_0)

        # after login
        self.navigation_admin_1 = QWidget()
        self.init_nav_admin()
        self.navigation.addWidget(self.navigation_admin_1)

    def init_nav_visitor(self):
        # button init
        self.navigation_visitor_0.pushButton_query = QPushButton()
        self.navigation_visitor_0.pushButton_query.setText("图书查询")
        self.navigation_visitor_0.pushButton_query.clicked.connect(self.book_query)

        self.navigation_visitor_0.pushButton_login = QPushButton()
        self.navigation_visitor_0.pushButton_login.setText("管理员登录")
        self.navigation_visitor_0.pushButton_login.clicked.connect(self.login)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.navigation_visitor_0.pushButton_query)
        layout.addWidget(self.navigation_visitor_0.pushButton_login)
        layout.setSpacing(40)
        layout.addStretch()
        self.navigation_visitor_0.setLayout(layout)

    def init_nav_admin(self):
        # button init
        self.navigation_admin_1.pushButton_query = QPushButton()
        self.navigation_admin_1.pushButton_query.setText("图书查询")
        self.navigation_admin_1.pushButton_query.clicked.connect(self.book_query)

        self.navigation_admin_1.pushButton_logout = QPushButton()
        self.navigation_admin_1.pushButton_logout.setText("退出登录")
        self.navigation_admin_1.pushButton_logout.clicked.connect(self.logout)

        self.navigation_admin_1.pushButton_borrow = QPushButton()
        self.navigation_admin_1.pushButton_borrow.setText("借书管理")
        self.navigation_admin_1.pushButton_borrow.clicked.connect(self.borrow)

        self.navigation_admin_1.pushButton_return = QPushButton()
        self.navigation_admin_1.pushButton_return.setText("还书管理")
        self.navigation_admin_1.pushButton_return.clicked.connect(self.bookReturn)

        self.navigation_admin_1.pushButton_newbook = QPushButton()
        self.navigation_admin_1.pushButton_newbook.setText("书籍管理")
        self.navigation_admin_1.pushButton_newbook.clicked.connect(self.newbook)

        self.navigation_admin_1.pushButton_manageID = QPushButton()
        self.navigation_admin_1.pushButton_manageID.setText("借书证管理")
        self.navigation_admin_1.pushButton_manageID.clicked.connect(self.manageID)

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.navigation_admin_1.pushButton_query)
        layout.addWidget(self.navigation_admin_1.pushButton_logout)
        layout.addWidget(self.navigation_admin_1.pushButton_borrow)
        layout.addWidget(self.navigation_admin_1.pushButton_return)
        layout.addWidget(self.navigation_admin_1.pushButton_newbook)
        layout.addWidget(self.navigation_admin_1.pushButton_manageID)
        layout.setSpacing(40)
        layout.addStretch()
        self.navigation_admin_1.setLayout(layout)

    def book_query(self):
        # query page of stack
        self.stack.setCurrentIndex(1)
        self.stack_query_1.initBox()

    def login(self):
        loginWindow = login.loginDialog(self.db)
        loginWindow.adminSignal.connect(self.getAdminID)
        if loginWindow.exec_() == QDialog.Accepted:
            self.navigation.setCurrentIndex(1)

    def getAdminID(self, name):
        self.label_status.setText('欢迎，尊敬的' + name)
        self.admin = name

    def logout(self):
        if QMessageBox.question(self, '用户', '是否要注销当前用户？', QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes) \
         == QMessageBox.Yes:
            self.stack.setCurrentIndex(0)
            self.navigation.setCurrentIndex(0)
            self.admin = ''
            self.label_status.setText('欢迎！')

    def borrow(self):
        readerLoginWindow = login.readerLoginDialog(self.db)
        readerLoginWindow.idSignal.connect(self.getReaderID)
        if readerLoginWindow.exec_() == QDialog.Accepted:
            self.admin2borrow.emit(self.admin)
            self.stack.setCurrentIndex(2)

    def getReaderID(self, id):
        self.stack_borrow_2.getReaderID(id)
        self.stack_return_3.getReaderID(id)

    def newbook(self):
        self.stack.setCurrentIndex(5)

    def bookReturn(self):
        readerLoginWindow = login.readerLoginDialog(self.db)
        readerLoginWindow.idSignal.connect(self.getReaderID)
        if readerLoginWindow.exec_() == QDialog.Accepted:
            self.admin2return.emit(self.admin)
            self.stack.setCurrentIndex(3)

    def manageID(self):
        self.stack.setCurrentIndex(4)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myMainWindow()
    window.show()
    sys.exit(app.exec_())

