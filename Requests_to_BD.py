import sqlite3
from secret import BD


class requests:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect(BD)
        self.cursor = self.sqlite_connection.cursor()

    def proverka_na_prava_stuff(self, ID):
        self.cursor.execute("SELECT Status_rank FROM Stuff WHERE ?", (str(ID)))
        return str(self.cursor.fetchone())
