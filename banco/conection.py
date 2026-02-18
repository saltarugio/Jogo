import mysql.connector


class Banco:
    def __init__(self):
        self.db = None
        self.cursor = None
    
    def __enter__(self):
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="mundo_interativo"
        )
        self.cursor = self.db.cursor(dictionary=True)

        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db and self.db.is_connected():
            self.cursor.close()
            self.db.close()
        if self.cursor:
            self.cursor.close()