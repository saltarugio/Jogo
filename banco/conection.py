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
        print("✅ Database connection established")
        return True
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return False

def close():
    global db, cursor
    if db and db.is_connected():
        cursor.close()
        db.close()
        print("🔒 Database connection closed")
