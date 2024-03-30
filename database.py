import sqlite3

db = sqlite3.connect('./sqlite.db')

cur = db.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS reportedLinks(chatId INTEGER NOT NULL, link TEXT NOT NULL PRIMARY KEY)''')

db.commit()
