import sqlite3

conn = sqlite3.connect('concerts.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS venues (
    title TEXT NOT NULL,
    city TEXT NOT NULL)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bands (
    title TEXT NOT NULL,
    city TEXT NOT NULL)""")


cursor.execute("""
CREATE TABLE concerts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  band_id INTEGER,
  venue_id INTEGER,
  date TEXT,
  FOREIGN KEY (band_id) REFERENCES bands(id),
  FOREIGN KEY (venue_id) REFERENCES venues(id)
);
""")
conn.commit()



cursor.execute("INSERT INTO bands (name, hometown) VALUES (?, ?)", ("Radiohead", "Abingdon-on-Thames"))
cursor.execute("INSERT INTO bands (name, hometown) VALUES (?, ?)", ("The Beatles", "Liverpool"))
cursor.execute("INSERT INTO venues (title, city) VALUES (?, ?)", ("Madison Square Garden", "New York City"))
cursor.execute("INSERT INTO venues (title, city) VALUES (?, ?)", ("The O2 Arena", "London"))
cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)", (1, 1, "2024-10-26"))
cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)", (2, 2, "2024-11-12"))
conn.commit()

class Band:
    def __init__(self, name, hometown):
        self._name = name  
        self._hometown = hometown  
        self._concerts = []  

    @property
    def name(self):
        return self._name  

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 0:  
            self._name = value  
        else:
            ValueError("Name must be a non-empty string")  

    @property
    def hometown(self):
        return self._hometown  

    @hometown.setter
    def hometown(self, value):
        if isinstance(value, str) and len(value) > 0: 
            self._hometown = value  
        else:
            ValueError("Hometown must be a non-empty string")  

    def add_concert(self, concert):
        if concert not in self._concerts:
            self._concerts.append(concert)  

    def concerts(self):
        return self._concerts  

    def venues(self):
        return list({concert.venue for concert in self._concerts if isinstance(concert.venue, Venue)})  

    def play_in_venue(self, venue, date):
        concert = Concert(date=date, band=self, venue=venue)  
        self.add_concert(concert)  
        venue.add_concert(concert)  
        return concert  

    def all_introductions(self):
        return [concert.introduction() for concert in self._concerts]  
class Venue:
    def __init__(self, name, city):
        self._name = name  
        self._city = city  
        self._concerts = []  
        self._bands = set()  

    @property
    def name(self):
        return self._name  

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 0:  
            self._name = value  
        else:
            ValueError("Name must be a non-empty string")  
    @property
    def city(self):
        return self._city  

    @city.setter
    def city(self, value):
        if isinstance(value, str) and len(value) > 0:  
            self._city = value  
        else:
            ValueError("City must be a non-empty string") 

    def add_concert(self, concert):
        """Add a concert to the venue."""
        if concert not in self._concerts:
            self._concerts.append(concert)
            self.add_band(concert.band)  

    def remove_concert(self, concert):
        """Remove a concert from the venue."""
        if concert in self._concerts:
            self._concerts.remove(concert) 

    def add_band(self, band):
        """Add a band to the venue."""
        if band not in self._bands:
            self._bands.add(band)  

    def remove_band(self, band):
        """Remove a band from the venue."""
        if band in self._bands:
            self._bands.remove(band)  

    def concerts(self):
        """Return a list of concerts at the venue."""
        return self._concerts  

    def bands(self):
        """Return a list of unique bands that have played at the venue."""
        return list(self._bands)  

class Concert:
    all = []  

    def __init__(self, date, band, venue):
        self._date = date  
        self._band = band  
        self._venue = venue  
        self._band.add_concert(self) 
        self._venue.add_concert(self)  
        Concert.all.append(self)  

    @property
    def date(self):
        return self._date  

    @date.setter
    def date(self, value):
        if isinstance(value, str) and len(value) > 0:  
            self._date = value  
        else:
            ValueError("Date must be a non-empty string.")  

    @property
    def band(self):
        return self._band  

    @band.setter
    def band(self, value):
        if isinstance(value, Band):
            self._band = value  
        else:
            ValueError("Band must be an instance of Band class.")  

    @property
    def venue(self):
        return self._venue  

    @venue.setter
    def venue(self, value):
        if isinstance(value, Venue):
            self._venue = value  
        else:
            ValueError("Venue must be an instance of Venue class.")  

    def hometown_show(self):
        return self._venue.city == self._band.hometown  

    def introduction(self):
        return f"Hello {self._venue.city}!!!!! We are {self._band.name} and we're from {self._band.hometown}"  