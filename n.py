import sqlite3

conn = sqlite3.connect('Raffle.db', check_same_thread=False)
conn.execute("UPDATE Members SET CHAT_ID=0 WHERE Number=1")
conn.commit()
conn.close()
