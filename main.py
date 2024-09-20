from concert import Concert
from venue import Venue
from band import Band

def main():
    
    concert = Concert(1)
    print("Band for concert 1:", concert.band())
    print("Venue for concert 1:", concert.venue())
    print("Is hometown show for concert 1?", concert.hometown_show())
    print("Introduction for concert 1:", concert.introduction())
    
    venue = Venue(1)
    print("Concerts at venue 1:", venue.concerts())
    print("Bands at venue 1:", venue.bands())
    print("First concert on 2024-01-20:", venue.concert_on("2024-01-20"))
    print("Most frequent band at venue 1:", venue.most_frequent_band())
    
    band = Band(1)
    print("Concerts played by band 1:", band.concerts())
    print("Venues played by band 1:", band.venues())
    band.play_in_venue(2, "2024-03-15")  
    print("All introductions for band 1:", band.all_introductions())
    print("Band with most performances:", Band.most_performances())

if __name__ == "__main__":
    main()
