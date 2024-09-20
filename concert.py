from db_setup import create_connection

class Concert:
    def __init__(self, concert_id):
        self.concert_id = concert_id

    def band(self):
        """Returns the Band instance for this concert."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT bands.id, bands.name, bands.hometown 
            FROM concerts 
            JOIN bands ON concerts.band_id = bands.id 
            WHERE concerts.id = ?
        """, (self.concert_id,))
        band = cur.fetchone()
        cur.close()
        conn.close()
        return band

    def venue(self):
        """Returns the Venue instance for this concert."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT venues.id, venues.title, venues.city 
            FROM concerts 
            JOIN venues ON concerts.venue_id = venues.id 
            WHERE concerts.id = ?
        """, (self.concert_id,))
        venue = cur.fetchone()
        cur.close()
        conn.close()
        return venue

    def hometown_show(self):
        """Returns True if the concert is in the band's hometown, otherwise False."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT venues.city, bands.hometown 
            FROM concerts
            JOIN bands ON concerts.band_id = bands.id
            JOIN venues ON concerts.venue_id = venues.id
            WHERE concerts.id = ?
        """, (self.concert_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] == result[1]

    def introduction(self):
        """Returns the introduction string for this concert."""
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT venues.city, bands.name, bands.hometown 
            FROM concerts
            JOIN bands ON concerts.band_id = bands.id
            JOIN venues ON concerts.venue_id = venues.id
            WHERE concerts.id = ?
        """, (self.concert_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return f"Hello {result[0]}!!!!! We are {result[1]} and we're from {result[2]}"
