# !_*_ coding:utf-8 _*_

import sys, database
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class bookQueryWindow(QWidget):
    def __init__(self, database):
        super().__init__()
        self.db = database
        # self.db = database.SQLConn()
        self.initUI()

    def initUI(self):
        # label
        self.label_name = QLabel('书名')
        self.label_type = QLabel('类别')
        self.label_author = QLabel('作者')
        self.label_publisher = QLabel('出版社')
        self.label_year = QLabel('出版时间')
        self.label_price = QLabel('价格范围')

        # lineEdit
        self.lineEdit_name = QLineEdit()
        self.lineEdit_author = QLineEdit()
        self.lineEdit_publisher = QLineEdit()
        self.lineEdit_pricelow = QLineEdit()
        self.lineEdit_pricehigh = QLineEdit()

        # comboBox
        self.box_type = QComboBox()
        self.box_type.activated.connect(self.boxclear)

        self.box_publisher = QComboBox()
        self.box_publisher.activated.connect(self.boxclear)

        self.initBox()

        self.box_yearlow = QComboBox()
        yearlist = [str(i) for i in range(1900, 2020)]
        yearlist.append('空')
        self.box_yearlow.addItems(yearlist)
        self.box_yearlow.activated.connect(self.boxclear)
        self.box_yearlow.setCurrentIndex(-1)

        self.box_yearhigh = QComboBox()
        self.box_yearhigh.addItems(yearlist)
        self.box_yearhigh.activated.connect(self.boxclear)
        self.box_yearhigh.setCurrentIndex(-1)

        # pushbutton
        self.pushbutton_query = QPushButton("查询")
        self.pushbutton_query.clicked.connect(self.query)
        self.pushbutton_clear = QPushButton("清空")
        self.pushbutton_clear.clicked.connect(self.clear)

        # table
        self.table = QTableWidget()

        # layout
        layout = QGridLayout()
        layout.addWidget(self.label_name, 0, 0, 1, 1)
        layout.addWidget(self.label_type, 0, 3, 1, 1)
        layout.addWidget(self.label_author, 0, 6, 1, 1)
        layout.addWidget(self.label_publisher, 1, 0, 1, 1)
        layout.addWidget(self.label_year, 1, 3, 1, 1)
        layout.addWidget(self.label_price, 1, 6, 1, 1)
        layout.addWidget(self.lineEdit_name, 0, 1, 1, 2)
        layout.addWidget(self.lineEdit_author, 0, 7, 1, 2)
        layout.addWidget(self.lineEdit_pricelow, 1, 7, 1, 1)
        layout.addWidget(self.lineEdit_pricehigh, 1, 8, 1, 1)
        layout.addWidget(self.box_type, 0, 4, 1, 2)
        layout.addWidget(self.box_publisher, 1, 1, 1, 2)
        layout.addWidget(self.box_yearlow, 1, 4, 1, 1)
        layout.addWidget(self.box_yearhigh, 1, 5, 1, 1)
        layout.addWidget(self.pushbutton_query, 0, 9, 1, 1)
        layout.addWidget(self.pushbutton_clear, 1, 9, 1, 1)
        layout.addWidget(self.table, 2, 0, 10, 10)

        self.setLayout(layout)

    def initBox(self):
        self.box_type.clear()
        select = database.select_sql('Books', ['distinct BookType'])
        self.db.execute(select)
        oblist = self.db.fetch_result_list()
        oblist.append('空')
        self.box_type.addItems(oblist)

        self.box_publisher.clear()
        select = database.select_sql('Books', ['distinct Publisher'])
        self.db.execute(select)
        oblist = self.db.fetch_result_list()
        oblist.append('空')
        self.box_publisher.addItems(oblist)

        self.box_type.setCurrentIndex(-1)
        self.box_publisher.setCurrentIndex(-1)

    def boxclear(self):
        if self.box_yearhigh.currentText() == '空':
            self.box_yearhigh.setCurrentIndex(-1)
        if self.box_yearlow.currentText() == '空':
            self.box_yearlow.setCurrentIndex(-1)
        if self.box_publisher.currentText() == '空':
            self.box_publisher.setCurrentIndex(-1)
        if self.box_type.currentText() == '空':
            self.box_type.setCurrentIndex(-1)

    def query(self):
        # conditions
        conditions = ''
        if self.lineEdit_name.text() != '':
            conditions += "BookName = '" + self.lineEdit_name.text() + "' and "
        if self.lineEdit_author.text() != '':
            conditions += "Author = '" + self.lineEdit_author.text() + "' and "
        if self.lineEdit_pricelow.text() != '':
            conditions += 'Price >= ' + self.lineEdit_pricelow.text() + ' and '
        if self.lineEdit_pricehigh.text() != '':
            conditions += 'Price <= ' + self.lineEdit_pricehigh.text() + ' and '
        if self.box_type.currentText() != '':
            conditions += "BookType = '" + self.box_type.currentText() + "' and "
        if self.box_publisher.currentText() != '':
            conditions += "Publisher = '" + self.box_publisher.currentText() + "' and "
        if self.box_yearlow.currentText() != '':
            conditions += "Year >= " + self.box_yearlow.currentText() + " and "
        if self.box_yearhigh.currentText() != '':
            conditions += "Year <= " + self.box_yearhigh.currentText() + " and "
        conditions = conditions[:-5]
        select = database.select_sql('Books', '*', conditions)
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

    def clear(self):
        self.table.clearContents()
        self.lineEdit_name.clear()
        self.lineEdit_author.clear()
        self.lineEdit_pricelow.clear()
        self.lineEdit_pricehigh.clear()
        self.box_type.setCurrentIndex(-1)
        self.box_publisher.setCurrentIndex(-1)
        self.box_yearlow.setCurrentIndex(-1)
        self.box_yearhigh.setCurrentIndex(-1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db1 = database.SQLConn()
    window = bookQueryWindow(db1)
    window.show()
    sys.exit(app.exec_())
