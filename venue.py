from db_setup import create_connection

class Venue:
    def __init__(self, venue_id):
        self.venue_id = venue_id

    def concerts(self):
        """Returns a collection of all concerts for the venue."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT concerts.id, concerts.date 
            FROM concerts 
            WHERE concerts.venue_id = ?
        """, (self.venue_id,))
        concerts = cur.fetchall()
        cur.close()
        conn.close()
        return concerts

    def bands(self):
        """Returns a collection of all bands who performed at the venue."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT bands.id, bands.name 
            FROM concerts 
            JOIN bands ON concerts.band_id = bands.id 
            WHERE concerts.venue_id = ?
        """, (self.venue_id,))
        bands = cur.fetchall()
        cur.close()
        conn.close()
        return bands

    def concert_on(self, date):
        """Finds the first concert on the given date at the venue."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT concerts.id, concerts.date 
            FROM concerts 
            WHERE concerts.venue_id = ? AND concerts.date = ? 
            LIMIT 1
        """, (self.venue_id, date))
        concert = cur.fetchone()
        cur.close()
        conn.close()
        return concert

    def most_frequent_band(self):
        """Returns the band that has performed the most at the venue."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT bands.name, COUNT(concerts.band_id) as performance_count
            FROM concerts 
            JOIN bands ON concerts.band_id = bands.id
            WHERE concerts.venue_id = ?
            GROUP BY concerts.band_id
            ORDER BY performance_count DESC
            LIMIT 1
        """, (self.venue_id,))
        band = cur.fetchone()
        cur.close()
        conn.close()
        return band
