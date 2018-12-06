import sqlite3
from typing import List


class SqliteWrapper:
    def __init__(self,
                 dbname: str = "forecast.db",
                 commit_immediately: bool = True):
        # Create Connection and Cursor
        self.connection = sqlite3.connect(dbname)
        self.cursor = self.connection.cursor()
        self.commit_immediately = commit_immediately

        # Check if schema exists, if not create
        self._check_or_create_schema_()

    def commit(self):
        self.connection.commit()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

    def insert_rows(self, query: str):
        self.cursor.execute(query)
        if self.commit_immediately:
            self.commit()

    def fetch_one(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_all(self, query: str):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def _check_or_create_schema_(self):
        with open("schema.sql", "r") as sql_file:
            sql_query = sql_file.read()
            sqlite3.complete_statement(sql_query)
            self.cursor.executescript(sql_query)
