
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
import sqlite3

class CoffeeManager(QMainWindow):
    def __init__(self):
        super(CoffeeManager, self).__init__()
        loadUi('main.ui', self)
        self.setWindowTitle('Coffee Manager')
        self.load_data()
        self.addButton.clicked.connect(self.open_add_edit_form)
        self.editButton.clicked.connect(self.open_add_edit_form)

    def load_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM coffee')
        data = cursor.fetchall()
        connection.close()
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))

    def open_add_edit_form(self):
        form = AddEditCoffeeForm()
        if form.exec_() == QDialog.Accepted:
            self.load_data()

class AddEditCoffeeForm(QDialog):
    def __init__(self):
        super(AddEditCoffeeForm, self).__init__()
        loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('Add/Edit Coffee')
        self.saveButton.clicked.connect(self.save_coffee)

    def save_coffee(self):
        name = self.nameLineEdit.text()
        roast = self.roastComboBox.currentText()
        ground = self.groundRadioButton.isChecked()
        taste = self.tasteTextEdit.toPlainText()
        price = self.priceSpinBox.value()
        volume = self.volumeSpinBox.value()

        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()
        if self.windowTitle() == 'Add/Edit Coffee':
            cursor.execute('INSERT INTO coffee (name, roast, ground, taste, price, volume) VALUES (?, ?, ?, ?, ?, ?)',
                           (name, roast, ground, taste, price, volume))
        else:
            pass 
        connection.commit()
        connection.close()
        self.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeManager()
    window.show()
    sys.exit(app.exec_())
