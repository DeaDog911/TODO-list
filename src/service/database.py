import sqlite3
import logging


class TwiceCompletedTask(Exception):
    pass


class ToDoListDB:
    TABLE_NAME = 'todo'

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        logging.info(f'Table is exist')
        print(f'Table is exist')
        try:
            self.cursor.execute(f'CREATE TABLE {self.TABLE_NAME} '
                                '(task text, is_completed numeric, complete_date text)')
            self.conn.commit()
            print(f'Table {self.TABLE_NAME} is created')
        except sqlite3.OperationalError:
            pass

    def select_tasks(self):
        try:
            self.cursor.execute(f'SELECT * FROM {self.TABLE_NAME} ORDER BY complete_date DESC')
            tasks = self.cursor.fetchall()
            return tasks
        except sqlite3.OperationalError:
            logging.error('Failed to fetch values from the table')

    def add_new_task(self, task):
        try:
            self.cursor.execute(f""" 
                                INSERT INTO {self.TABLE_NAME} VALUES ('{task}', 0, '' ) 
                                """)
            self.conn.commit()
        except sqlite3.OperationalError as e:
            logging.error(e)

    def edit_task(self, old_text, new_text):
        try:
            self.cursor.execute(f"""
                                UPDATE {self.TABLE_NAME}
                                SET task = '{new_text}'
                                WHERE task = '{old_text}'
                                """)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error("Failed to update the table")

    def delete_task(self, task):
        try:
            self.cursor.execute(f"""
                                DELETE FROM {self.TABLE_NAME} WHERE task = '{task}'
                                """)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error('Failed to delete values from table')

    def mark_task_as_complete(self, task_text, date):
        try:
            self.cursor.execute(f"""
                                UPDATE {self.TABLE_NAME}
                                SET is_completed = 1,
                                complete_date = '{date}'
                                WHERE task = '{task_text}' AND is_completed = 0
                                """)

            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error("Failed to update the table")

    def mark_task_as_uncompleted(self, task_text):
        try:
            self.cursor.execute(f"""
                                UPDATE {self.TABLE_NAME}
                                SET is_completed = 0,
                                complete_date = ''
                                WHERE task = '{task_text}'
                                """)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error("Failed to update the table")

    def delete_all_tasks(self):
        try:
            self.cursor.execute(f"DELETE FROM {self.TABLE_NAME}")
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error("Failed to delete all values from table")