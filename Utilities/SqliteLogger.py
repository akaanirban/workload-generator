import sqlite3
import json


class SqliteLogger:
    def __init__(self, db_file_name):
        self.db_file = db_file_name
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def execute_statement(self, statement, commit_flag=False):
        self.cursor.execute(statement)
        if commit_flag :
            self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close_logger(self):
        self.conn.close()



