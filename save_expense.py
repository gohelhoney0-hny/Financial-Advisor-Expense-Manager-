import sqlite3
def save_expense(text, category):
    
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       text TEXT,
                       category TEXT)''')
    cursor.execute('INSERT INTO expenses (text, category) VALUES (?, ?)', (text, category))
    conn.commit()
    conn.close()