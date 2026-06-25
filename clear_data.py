import sqlite3
conn = sqlite3.connect("expenses.db")

cursor = conn.cursor()
cursor.execute("DELETE FROM expenses")
conn.commit()
conn.close()

print("All records deleted successfully")