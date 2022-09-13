import sqlite3
import datetime
from datetime import datetime, timedelta

def db():
        connection = sqlite3.connect("base.db")
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS user(user_id INTEGER, user_balance INTEGER)')

async def db_add_user(user_id):
	connection = sqlite3.connect("base.db")
	cursor = connection.cursor()
	if cursor.execute("SELECT * FROM user WHERE user_id = ?", (user_id, )).fetchone() == None:
		cursor.execute("INSERT INTO user VALUES(?, ?)", (user_id, 0, ))
	connection.commit()
	cursor.close()
