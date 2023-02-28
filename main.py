import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from UI.main_ui import Ui_MainWindow
from UI.addEditCoffeeForm_ui import Ui_Form


class DBSample(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.load_table()
        self.widget = MyWidget()
        self.pushButton.clicked.connect(self.widget.show)

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


class MyWidget(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("data/coffee.sqlite")
        self.pushButton.clicked.connect(self.update_result)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton_2.clicked.connect(self.save_results)
        self.modified = {}
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM coffee WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.label_2.setText('Ничего не нашлось')
            return
        else:
            self.label_2.setText(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
