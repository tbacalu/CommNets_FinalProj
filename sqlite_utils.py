import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    finally:
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
            if cur.fetchall():
                pass
            else:
                cur.execute("CREATE TABLE messages (sender, receiver, message)")
                conn.commit()
            conn.close()

db = 'test-sqlite.db'
create_connection(db)

#create a table for messages to be used later

# def insert(db_name, sender, receiver, message):
#     con = sqlite3.connect(db_name)
#     cur = con.cursor()
#     cur.execute("INSERT INTO messages VALUES ('{}', '{}', '{}')".format(sender, receiver, message))
#     con.commit()
#     con.close()

# def retrieve(db_name):
#     con = sqlite3.connect(db_name)
#     cur = con.cursor()
#     cur.execute('SELECT * FROM messages')
#     return cur.fetchall()
#     con.close()

# insert()
# retrieve()