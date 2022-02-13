from multiprocessing import connection
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()



CREATE_TABLE = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(CREATE_TABLE)

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
cursor.execute(CREATE_TABLE)

# cursor.execute("INSERT INTO items VALUES ('test', 10.99)")
conn.commit()

conn.close()
