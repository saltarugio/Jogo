import mysql.connector

db = None
cursor = None

def open():
    global db, cursor
    try:
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="mundo_interativo"
        )
        cursor = db.cursor(dictionary=True)

        return True
    except mysql.connector.Error as e:
        return False

def close():
    global db, cursor
    if db and db.is_connected():
        cursor.close()
        db.close()
