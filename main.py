import sys
import datetime
import sqlite3

from src.gui import window
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor

from src.service.database import ToDoListDB


class Todo_App(QtWidgets.QMainWindow, window.Ui_MainWindow):
    COMPLETE_COLOR = '#778791'
    BASE_COLOR = '#FFFFFF'

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.new_task_btn.clicked.connect(self.add_task)
        self.delete_btn.clicked.connect(self.delete_task)

        self.save_btn.clicked.connect(self.save_task)
        self.edit_btn.clicked.connect(self.edit_task)

        self.complete_btn.clicked.connect(self.complete_task)
        self.uncomplete_btn.clicked.connect(self.uncomplete_task)

        self.delete_all_btn.clicked.connect(self.delete_all_tasks)

        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        self.database = ToDoListDB()

        self.show_tasks()

    def show_tasks(self):
        tasks = self.database.select_tasks()
        for task in tasks:
            if task[1] == 1:
                self.append_completed_task(task[0], task[2])
            else:
                self.append_uncompleted_task(task[0])
        self.sort_items()

    def append_completed_task(self, task, date):
        text = f'{task} | {date}'
        self.task_list_widget.addItem(text)
        last_item = self.task_list_widget.item(self.task_list_widget.count() - 1)
        last_item.setBackground(QColor(self.COMPLETE_COLOR))

    def append_uncompleted_task(self, task):
        self.task_list_widget.addItem(task)
        last_item = self.task_list_widget.item(self.task_list_widget.count() - 1)
        last_item.setBackground(QColor(self.BASE_COLOR))

    def get_input_task(self):
        return self.lineEdit.text()

    def append_completed_tasks(self, tasks):
        for i in range(len(tasks)):
            self.task_list_widget.addItem(tasks[i])
            last_item = self.task_list_widget.item(self.task_list_widget.count() - 1)
            last_item.setBackground(QColor(self.COMPLETE_COLOR))

    def append_uncompleted_tasks(self, tasks):
        for i in range(len(tasks)):
            self.task_list_widget.addItem(tasks[i])
            last_item = self.task_list_widget.item(self.task_list_widget.count() - 1)
            last_item.setBackground(QColor(self.BASE_COLOR))

    def add_task(self):
        new_task = self.lineEdit.text()
        if new_task:
            self.task_list_widget.addItem(new_task)
            self.lineEdit.setText('')

        self.database.add_new_task(new_task)

    def edit_task(self):
        current_item = self.task_list_widget.currentItem()
        if current_item:
            self.lineEdit.setText(current_item.text())

    def save_task(self):
        current_item = self.task_list_widget.currentItem()
        old_text = current_item.text()
        new_text = self.lineEdit.text()
        if current_item:
            current_item.setText(new_text)
            self.lineEdit.setText('')

        self.database.edit_task(old_text, new_text)

    def delete_task(self):
        current_row = self.task_list_widget.currentRow()
        current_item = self.task_list_widget.currentItem()
        current_item_text = current_item.text()

        if current_item:
            if current_row:
                self.task_list_widget.takeItem(current_row)

            if self.task_list_widget.count() == 1:
                self.task_list_widget.clear()

            self.database.delete_task(current_item_text)

    def complete_task(self):
        current_item = self.task_list_widget.currentItem()
        if current_item and current_item.text().split('|') == []:
            date = str(datetime.datetime.now().date())
            task_text = current_item.text()
            self.database.mark_task_as_complete(task_text, date)
            new_text = f'{task_text} | {date}'
            current_item.setText(new_text)
            current_item.setBackground(QColor(self.COMPLETE_COLOR))
            self.sort_items()


    def uncomplete_task(self):
        current_item = self.task_list_widget.currentItem()
        if current_item:
            task_text_date = current_item.text().split('|')
            task_text = task_text_date[0].strip()
            current_item.setText(task_text)
            current_item.setBackground(QColor(self.BASE_COLOR))
            self.sort_items()

            self.database.mark_task_as_uncompleted(task_text)

    def get_completed_tasks(self):
        completed_tasks = []
        for i in range(self.task_list_widget.count()):
            task = self.task_list_widget.item(i)
            if task.background().color() == QColor(self.COMPLETE_COLOR):
                completed_tasks.append(task.text())
        return completed_tasks

    def get_uncompleted_tasks(self):
        uncompleted_tasks = []
        for i in range(self.task_list_widget.count()):
            task = self.task_list_widget.item(i)
            if task.background().color() != QColor(self.COMPLETE_COLOR):
                uncompleted_tasks.append(task.text())
        return uncompleted_tasks

    def sort_items(self):
        completed_tasks = self.get_completed_tasks()
        uncompleted_tasks = self.get_uncompleted_tasks()

        self.task_list_widget.clear()

        self.append_completed_tasks(completed_tasks)
        self.append_uncompleted_tasks(uncompleted_tasks)

    def delete_all_tasks(self):
        self.task_list_widget.clear()

        self.database.delete_all_tasks()


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = Todo_App()
    win.setWindowTitle('TODO')
    win.show()
    app.exec_()


if __name__ == '__main__':
    main()
