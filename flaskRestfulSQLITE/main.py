import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

CREATE_TABLE = "CREATE TABLE IF NOT EXISTS users (id int, username text, password text)"

cursor.execute(CREATE_TABLE)

user = (1, "kairi", "password")
users = [
    (2, "kairi2", "password"),
    (3, "kairi3", "password")
]
INSERT_QUERY = "INSERT INTO users VALUES (?,?,?)"

cursor.execute(INSERT_QUERY, user)
cursor.executemany(INSERT_QUERY, users)
SELECT_QUERY = "SELECT * FROM users"

for row in cursor.execute(SELECT_QUERY):
    print(row)

connection.commit()
connection.close()