import sqlite3 as sql


class Database:

    def __init__(self, database_file):
        self.conn = sql.connect(database_file)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.conn.close()

    def create_new_cursor(self):
        self.cursor = self.conn.cursor()

    def commit_changes(self):
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def count_rows(self, table):
        self.cursor.execute(f'SELECT COUNT(*) FROM {table}')
        return self.cursor.fetchone()[0]