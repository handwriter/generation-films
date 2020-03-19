import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem
from ui_3 import Ui_Form


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("films.db")
        self.pushButton.clicked.connect(self.update_result)
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("Select * from films WHERE id=?",
                             (self.spinBox.text(),)).fetchall()
        result2 = cur.execute("""UPDATE films
                                 SET title=?, year=?, duration=?
                                 WHERE id=?""",
                             (result[0][1][::-1], int(result[0][2]) + 1000, int(result[0][-1]) // 2, result[0][0])).fetchall()
        self.con.commit()
        result = cur.execute("Select * from films WHERE id=?",
                             (self.spinBox.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())