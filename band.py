from db_setup import create_connection

class Band:
    def __init__(self, band_id):
        self.band_id = band_id

    def concerts(self):
        """Returns a collection of all concerts the band has played."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT concerts.id, concerts.date 
            FROM concerts 
            WHERE concerts.band_id = ?
        """, (self.band_id,))
        concerts = cur.fetchall()
        cur.close()
        conn.close()
        return concerts

    def venues(self):
        """Returns a collection of all venues the band has performed at."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT venues.id, venues.title 
            FROM concerts 
            JOIN venues ON concerts.venue_id = venues.id 
            WHERE concerts.band_id = ?
        """, (self.band_id,))
        venues = cur.fetchall()
        cur.close()
        conn.close()
        return venues

    def play_in_venue(self, venue_id, date):
        """Creates a new concert for the band at the venue on the given date."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO concerts (band_id, venue_id, date)
            VALUES (?, ?, ?)
        """, (self.band_id, venue_id, date))
        conn.commit()
        cur.close()
        conn.close()

    def all_introductions(self):
        """Returns all introductions for this band."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT venues.city, bands.name, bands.hometown
            FROM concerts
            JOIN venues ON concerts.venue_id = venues.id
            JOIN bands ON concerts.band_id = bands.id
            WHERE concerts.band_id = ?
        """, (self.band_id,))
        introductions = cur.fetchall()
        cur.close()
        conn.close()
        return [f"Hello {intro[0]}!!!!! We are {intro[1]} and we're from {intro[2]}" for intro in introductions]

    @staticmethod
    def most_performances():
        """Returns the band with the most concerts."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT bands.name, COUNT(concerts.id) as performance_count
            FROM concerts
            JOIN bands ON concerts.band_id = bands.id
            GROUP BY bands.id
            ORDER BY performance_count DESC
            LIMIT 1
        """)
        band = cur.fetchone()
        cur.close()
        conn.close()
        return band
