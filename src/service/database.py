import sqlite3
import logging


class Todo_list_DB:
    TABLE_NAME = 'todo'

    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute(f'CREATE TABLE {self.TABLE_NAME} '
                                '(task text, is_completed numeric, complete_date text)')
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

    def select_tasks(self):
        try:
            self.cursor.execute('SELECT * FROM todo ORDER BY complete_date DESC')
            tasks = self.cursor.fetchall()
            return tasks
        except sqlite3.OperationalError:
            logging.error('Failed to fetch values from the table')

    def add_new_task(self, task):
        try:
            self.cursor.execute(f""" 
                                INSERT INTO todo
                                VALUES ('{task}', {False}, '' ) 
                                """)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error('Failed to insert values into the table')

    def edit_task(self, old_text, new_text):
        try:
            self.cursor.execute(f"""
                                UPDATE todo
                                SET task = '{new_text}'
                                WHERE task = '{old_text}'
                                """)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error("Failed to update the table")

    def delete_task(self, task):
        try:
            self.cursor.execute(f"""
                                DELETE FROM todo WHERE task = '{task}'
                                """)
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error('Failed to delete values from table')

    def mark_task_as_complete(self, task_text, date):
        try:
            self.cursor.execute(f"""
                                UPDATE todo
                                SET is_completed = {True}
                                WHERE task = '{task_text}'
                                """)

            self.cursor.execute(f"""
                                UPDATE todo
                                SET complete_date = '{date}'
                                WHERE task = '{task_text}'
                                """)

            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error("Failed to update the table")

    def mark_task_as_uncomplete(self, task_text):
        try:
            self.cursor.execute(f"""
                                UPDATE todo
                                SET is_completed = {False}
                                WHERE task = '{task_text}'
                                """)

            self.cursor.execute(f"""
                                UPDATE todo
                                SET complete_date = ''
                                WHERE task = '{task_text}'
                                """)

            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error("Failed to update the table")

    def delete_all_tasks(self):
        try:
            self.cursor.execute("DELETE FROM todo")
            self.conn.commit()
        except sqlite3.OperationalError:
            logging.error("Failed to delete all values from table")