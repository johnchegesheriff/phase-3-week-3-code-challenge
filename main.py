import sqlite3

def create_database():
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bands (
        name TEXT NOT NULL,
        hometown TEXT NOT NULL
    )
    ''')


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS venues (
        title TEXT NOT NULL,
        city TEXT NOT NULL
    )
    ''')

    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS concerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        band_name TEXT,
        venue_title TEXT,
        date TEXT,
        FOREIGN KEY(band_name) REFERENCES bands(name),
        FOREIGN KEY(venue_title) REFERENCES venues(title)
    )
    ''')

    #closing the connection
    conn.commit()
    conn.close()


def insert_sample_data():
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO bands (name, hometown) VALUES ('The Swindlers', 'Switzerland')")
    cursor.execute("INSERT INTO venues (title, city) VALUES ('Gig Hall', 'New York')")
    cursor.execute("INSERT INTO concerts (band_name, venue_title, date) VALUES ('The Swindlers', 'Gig Hall', '2024-09-01')")

    conn.commit()
    conn.close()


def get_band_for_concert(concert_id):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM bands
        JOIN concerts ON bands.name = concerts.band_name
        WHERE concerts.id = ?
    ''', (concert_id,))
    band = cursor.fetchone()
    conn.close()
    return band


def get_venue_for_concert(concert_id):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM venues
        JOIN concerts ON venues.title = concerts.venue_title
        WHERE concerts.id = ?
    ''', (concert_id,))
    venue = cursor.fetchone()
    conn.close()
    return venue


def get_concerts_for_venue(venue_title):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM concerts
        WHERE venue_title = ?
    ''', (venue_title,))
    concerts = cursor.fetchall()
    conn.close()
    return concerts


def get_bands_for_venue(venue_title):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT band_name FROM concerts
        WHERE venue_title = ?
    ''', (venue_title,))
    bands = cursor.fetchall()
    conn.close()
    return bands


def get_concerts_for_band(band_name):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM concerts
        WHERE band_name = ?
    ''', (band_name,))
    concerts = cursor.fetchall()
    conn.close()
    return concerts


def get_venues_for_band(band_name):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT venue_title FROM concerts
        WHERE band_name = ?
    ''', (band_name,))
    venues = cursor.fetchall()
    conn.close()
    return venues


def hometown_show(concert_id):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bands.hometown, venues.city FROM concerts
        JOIN bands ON bands.name = concerts.band_name
        JOIN venues ON venues.title = concerts.venue_title
        WHERE concerts.id = ?
    ''', (concert_id,))
    hometown, city = cursor.fetchone()
    conn.close()
    return hometown == city


def introduction(concert_id):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT venues.city, bands.name, bands.hometown FROM concerts
        JOIN bands ON bands.name = concerts.band_name
        JOIN venues ON venues.title = concerts.venue_title
        WHERE concerts.id = ?
    ''', (concert_id,))
    city, name, hometown = cursor.fetchone()
    conn.close()
    return f"Hello {city}!!!!! We are {name} and we're from {hometown}"


def play_in_venue(band_name, venue_title, date):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO concerts (band_name, venue_title, date) VALUES (?, ?, ?)
    ''', (band_name, venue_title, date))
    conn.commit()
    conn.close()

def all_introductions(band_name):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT venues.city, bands.name, bands.hometown FROM concerts
        JOIN bands ON bands.name = concerts.band_name
        JOIN venues ON venues.title = concerts.venue_title
        WHERE bands.name = ?
    ''', (band_name,))
    introductions = cursor.fetchall()
    conn.close()
    return [f"Hello {city}!!!!! We are {name} and we're from {hometown}" for city, name, hometown in introductions]

def most_performances():
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT band_name, COUNT(*) as performance_count FROM concerts
        GROUP BY band_name
        ORDER BY performance_count DESC
        LIMIT 1
    ''')
    most_performed_band = cursor.fetchone()
    conn.close()
    return most_performed_band

def concert_on(venue_title, date):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM concerts
        WHERE venue_title = ? AND date = ?
        LIMIT 1
    ''', (venue_title, date))
    concert = cursor.fetchone()
    conn.close()
    return concert

def most_frequent_band(venue_title):
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT band_name, COUNT(*) as performance_count FROM concerts
        WHERE venue_title = ?
        GROUP BY band_name
        ORDER BY performance_count DESC
        LIMIT 1
    ''', (venue_title,))
    frequent_band = cursor.fetchone()
    conn.close()
    return frequent_band

if __name__ == "__main__":
    create_database()
    insert_sample_data()