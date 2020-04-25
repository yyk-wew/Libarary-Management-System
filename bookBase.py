# !_*_ coding:utf-8 _*_

import datetime, re
import sys, database, login
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class bookBaseWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        # self.db = database.SQLConn()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('书籍管理')

        # push button
        self.button_add = QPushButton()
        self.button_add.setText('书籍入库')
        self.button_add.clicked.connect(self.addBook)

        self.button_change = QPushButton()
        self.button_change.setText("在库增删")
        self.button_change.clicked.connect(self.changeBook)

        self.button_batch = QPushButton()
        self.button_batch.setText('批量入库')
        self.button_batch.clicked.connect(self.batchBook)

        # table
        self.table = QTableWidget()
        self.initTable()

        # layout
        layout = QGridLayout()
        layout.addWidget(self.button_add, 0, 0, 1, 1)
        layout.addWidget(self.button_change, 0, 1, 1, 1)
        layout.addWidget(self.button_batch, 0, 2, 1, 1)
        layout.addWidget(self.table, 1, 0, 3, 3)
        self.setLayout(layout)

    def batchBook(self):
        fileName = QFileDialog.getOpenFileName(self, '选择文件', '/', '文本文件(*.txt)')
        if fileName[0]:
            f = open(fileName[0], 'r')
        else:
            return
        attrList = ['BookNo', 'BookType', 'BookName', 'Publisher', 'Year', 'Author', 'Price', 'Total',
                    'Storage', 'UpdateTime']
        with f:
            data = f.readlines()
            for i in range(len(data)):
                insertList = (data[i].strip()).split(',')
                checked = self.check(i, insertList)
                if not checked:
                    return
                insertList.append(str(datetime.date.today()))
                for i in range(len(insertList)):
                    if i in [0, 1, 2, 3, 5, 9]:
                        insertList[i] = "'" + insertList[i] + "'"
                insert = database.insert_sql('Books', attrList, insertList)
                self.db.execute(insert)
        self.db.commit()
        QMessageBox.about(self, '批量入库', '入库成功！')
        self.initTable()

    def check(self, i, l):
        condition = "BookNo = '%s'" % l[0]
        select = database.select_sql('Books', ['BookNo'], condition)
        self.db.execute(select)
        res = self.db.fetch_result(['BookNo'])
        if len(res) > 0:
            QMessageBox.about(self, '批量入库', '第%d行图书书号已存在' % i)
            return False
        if len(l) != 9:
            QMessageBox.about(self, '批量入库', '第%d行图书属性不全' % i)
            return False
        if not l[4].isdecimal():
            QMessageBox.about(self, '批量入库', '第%d行年份必须为整数' % i)
            return False
        if not l[6].isdigit():
            QMessageBox.about(self, '批量入库', '第%d行价格必须为数字' % i)
            return False
        if not l[7].isdecimal():
            QMessageBox.about(self, '批量入库', '第%d行图书总量必须为整数' % i)
            return False
        if not l[8].isdecimal():
            QMessageBox.about(self, '批量入库', '第%d行图书库存必须为整数' % i)
            return False
        if int(l[7]) < int(l[8]):
            QMessageBox.about(self, '批量入库', '第%d行图书总量必须大于库存' % i)
            return False
        return True

    def changeBook(self):
        Dialog = changeBookDialog(self.db)
        if Dialog.exec_() == QDialog.Accepted:
            self.initTable()

    def addBook(self):
        Dialog = addBookDialog(self.db)
        if Dialog.exec_() == QDialog.Accepted:
            self.initTable()

    def initTable(self):
        self.table.clear()
        select = database.select_sql('Books', '*')
        self.db.execute(select)
        attrlist = ['书号', '类型', '书名', '出版社', '出版时间',
                    '作者', '价格', '总藏书量', '库存', '最近更新']
        reslist = self.db.fetch_result(attrlist)
        self.table.setColumnCount(len(attrlist))
        self.table.setRowCount(len(reslist))
        self.table.setHorizontalHeaderLabels(attrlist)

        for i in range(len(attrlist)):
            for j in range(len(reslist)):
                self.table.setItem(j, i, QTableWidgetItem(reslist[j][attrlist[i]]))

class addBookDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        # self.db = database.SQLConn()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('图书入库')
        # lineEdit
        self.lineEdit_BookNo = QLineEdit()
        self.lineEdit_BookNo.setPlaceholderText("请输入书号")
        self.lineEdit_name = QLineEdit()
        self.lineEdit_name.setPlaceholderText("请输入书名")
        self.lineEdit_type = QLineEdit()
        self.lineEdit_type.setPlaceholderText("请输入类别")
        self.lineEdit_publisher = QLineEdit()
        self.lineEdit_publisher.setPlaceholderText("请输入出版社")
        self.lineEdit_author = QLineEdit()
        self.lineEdit_author.setPlaceholderText("请输入作者")
        self.lineEdit_price = QLineEdit()
        self.lineEdit_price.setPlaceholderText("请输入价格")
        self.lineEdit_total = QLineEdit()
        self.lineEdit_total.setPlaceholderText("请输入藏书总量")
        self.lineEdit_storage = QLineEdit()
        self.lineEdit_storage.setPlaceholderText("请输入库存数")

        # comboBox
        self.box_year = QComboBox()
        yearlist = [str(i) for i in range(1900, 2020)]
        self.box_year.addItems(yearlist)
        self.box_year.setCurrentIndex(-1)

        # push button
        self.button_enter = QPushButton()
        self.button_enter.setText("确定")
        self.button_enter.clicked.connect(self.enter)
        self.button_quit = QPushButton()
        self.button_quit.setText("取消")
        self.button_quit.clicked.connect(self.quit)

        # layout
        Flayout = QFormLayout()
        Flayout.addRow("书号", self.lineEdit_BookNo)
        Flayout.addRow("书名", self.lineEdit_name)
        Flayout.addRow("类型", self.lineEdit_type)
        Flayout.addRow("出版社", self.lineEdit_publisher)
        Flayout.addRow("出版日期", self.box_year)
        Flayout.addRow("作者", self.lineEdit_author)
        Flayout.addRow("价格", self.lineEdit_price)
        Flayout.addRow("总量", self.lineEdit_total)
        Flayout.addRow("库存", self.lineEdit_storage)
        Hlayout = QHBoxLayout()
        Hlayout.addWidget(self.button_enter)
        Hlayout.addWidget(self.button_quit)
        Vlayout = QVBoxLayout()
        Vlayout.addLayout(Flayout)
        Vlayout.addLayout(Hlayout)
        self.setLayout(Vlayout)

    def enter(self):
        # check integrity
        id = self.lineEdit_BookNo.text()
        select = database.select_sql('Books', ['BookNo'])
        self.db.execute(select)
        resList = self.db.fetch_result_list()
        if id in resList:
            QMessageBox.about(self, '图书入库', '书籍已存在')
            return
        # check NULL
        name = self.lineEdit_name.text()
        type = self.lineEdit_type.text()
        publisher = self.lineEdit_publisher.text()
        year = self.box_year.currentText()
        author = self.lineEdit_author.text()
        price = self.lineEdit_price.text()
        total = self.lineEdit_total.text()
        storage = self.lineEdit_storage.text()
        if id == '':
            QMessageBox.about(self, '图书入库', '书号不能为空')
            return
        if name == '':
            QMessageBox.about(self, '图书入库', '书名不能为空')
            return
        if type == '':
            QMessageBox.about(self, '图书入库', '类别不能为空')
            return
        if publisher == '':
            QMessageBox.about(self, '图书入库', '出版社不能为空')
            return
        if year == '':
            QMessageBox.about(self, '图书入库', '出版日期不能为空')
            return
        if author == '':
            QMessageBox.about(self, '图书入库', '作者不能为空')
            return
        if price == '':
            QMessageBox.about(self, '图书入库', '价格不能为空')
            return
        if total == '':
            QMessageBox.about(self, '图书入库', '总量不能为空')
            return
        if storage == '':
            QMessageBox.about(self, '图书入库', '库存不能为空')
            return
        if int(storage) > int(total):
            QMessageBox.about(self, '图书入库', '库存不能大于总量')
            return

        # insert
        attrList = ['BookNo', 'BookType', 'BookName', 'Publisher', 'Year', 'Author', 'Price', 'Total', 'Storage',
                    'UpdateTime']
        insertList = [id, type, name, publisher, year, author, price, total, storage, str(datetime.date.today())]
        for i in range(len(insertList)):
            if i in [0, 1, 2, 3, 5, 9]:
                insertList[i] = "'" + insertList[i] + "'"
        insert = database.insert_sql('Books', attrList, insertList)
        self.db.execute(insert)
        self.db.commit()
        QMessageBox.about(self, '图书入库', '入库成功！')
        self.accept()

    def quit(self):
        self.reject()

class changeBookDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.initUI()

    def initUI(self):
        self.setWindowTitle('在库书籍调整')
        self.resize(300, 150)

        self.lineEdit_id = QLineEdit()
        self.lineEdit_id.setPlaceholderText("请输入书号")
        self.lineEdit_id.textChanged.connect(self.idChanged)

        self.label_name = QLabel()

        self.lineEdit_total = QLineEdit()

        self.lineEdit_storage = QLineEdit()

        self.pushButton_enter = QPushButton()
        self.pushButton_enter.setText("提交")
        self.pushButton_enter.setEnabled(False)

        self.pushButton_quit = QPushButton()
        self.pushButton_quit.setText("取消")

        self.bookList = self.initBookList()

        form = QFormLayout()
        form.addRow('书号', self.lineEdit_id)
        form.addRow('书名', self.label_name)
        form.addRow('总量', self.lineEdit_total)
        form.addRow('库存', self.lineEdit_storage)

        gridButton = QHBoxLayout()
        gridButton.addWidget(self.pushButton_enter)
        gridButton.addWidget(self.pushButton_quit)
        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addLayout(gridButton)
        self.setLayout(vbox)

        self.pushButton_enter.clicked.connect(self.button_enter)
        self.pushButton_quit.clicked.connect(self.button_quit)

    def idChanged(self):
        self.pushButton_enter.setEnabled(False)
        self.label_name.clear()
        self.lineEdit_total.clear()
        self.lineEdit_storage.clear()
        id = self.lineEdit_id.text()
        for item in self.bookList:
            if id == item['BookNo']:
                self.label_name.setText(item['BookName'])
                self.lineEdit_storage.setText(item['Storage'])
                self.lineEdit_total.setText(item['Total'])
                self.pushButton_enter.setEnabled(True)

    def initBookList(self):
        select = database.select_sql('Books', '*')
        self.db.execute(select)
        res = self.db.fetch_result(['BookNo', 'BookType', 'BookName', 'Publisher', 'Year', 'Author',
                                    'Price', 'Total', 'Storage', 'UpdateTime'])
        return res

    def button_enter(self):
        id = self.lineEdit_id.text()
        storage = self.lineEdit_storage.text()
        total = self.lineEdit_total.text()
        update = database.update_sql('Books', 'Storage = %s, Total = %s' % (storage, total),
                                     "BookNo = '%s'" % id)
        self.db.execute(update)
        self.db.commit()
        QMessageBox.about(self, '在库增删', '书籍信息修改成功！')
        self.accept()

    def button_quit(self):
        self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = database.SQLConn()
    window = bookBaseWindow(db)
    window.show()
    sys.exit(app.exec_())
