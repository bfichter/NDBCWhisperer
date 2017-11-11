from scraper import Scraper
from pymongo import MongoClient

def main():
    stationID = '44018'
    client = MongoClient('localhost', 27017)
    db = client.ndbc
    scraper = Scraper(stationID, db)
    scraper.scrape()
    client.close()

if __name__ == "__main__":
    main()