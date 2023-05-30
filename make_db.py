import sqlite3

with sqlite3.connect('bugurts.db') as conn:
    c = conn.cursor()
    c.execute('ALTER TABLE users ADD COLUMN time REAL')
    conn.commit()
