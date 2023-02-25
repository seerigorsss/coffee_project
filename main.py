import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class DBSample(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.load_table()

    def load_table(self):
        res = self.connection.cursor().execute(
            """SELECT coffee.id, sorts.name, degrees.name,  types.name, taste_description, price, size
    FROM coffee
    JOIN sorts  ON coffee.sort = sorts.sort_id
    JOIN degrees  ON coffee.degree_of_roasting = degrees.degree_id
    JOIN types ON coffee.type = types.type_id""").fetchall()

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Сорт кофе", "Степень обжарки", 'Тип кофе',
                                                    'Описание вкуса', 'Цена в рублях', 'Объем в мл'])

    def closeEvent(self, event):
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
