import sqlite3
from config import DATABASE_URL

def init_db():
    conn = sqlite3.connect(DATABASE_URL)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS questions 
                 (id INTEGER PRIMARY KEY, subject TEXT, question TEXT, options TEXT, correct TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (user_id INTEGER PRIMARY KEY, full_name TEXT, score INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def get_questions(subject, limit=10):
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE subject = ? ORDER BY RANDOM() LIMIT ?", (subject, limit))
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows

def add_question(subject, q, opts, ans):
    conn = sqlite3.connect(DATABASE_URL)
    conn.cursor().execute("INSERT INTO questions (subject, question, options, correct) VALUES (?,?,?,?)",
                          (subject, q, opts, ans))
    conn.commit()
    conn.close()
