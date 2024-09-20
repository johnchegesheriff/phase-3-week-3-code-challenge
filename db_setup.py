import sqlite3  

conn = sqlite3.connect('concerts.db')  
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS concerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    band_id INTEGER,
    venue_id INTEGER,
    date TEXT NOT NULL,
    FOREIGN KEY (band_id) REFERENCES bands(id),
    FOREIGN KEY (venue_id) REFERENCES venues(id)
)
""")

conn.commit()
conn.close()
print("Concerts table created.")
