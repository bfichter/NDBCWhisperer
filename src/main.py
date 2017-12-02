from scraper import Scraper
from pymongo import MongoClient
from notifier import Notifier

def main():
    #push test
    notifier = Notifier()
    notifier.send('5886e435dadfbd10f15df6e8f2c73b7eecb7de9eaa9e5becb31f83894ed707a1', 'Test Message', 1, False)
    #
    stationID = '44008'
    client = MongoClient('localhost', 27017)
    db = client.ndbc
    scraper = Scraper(stationID, db)
    scraper.scrape()
    client.close()

if __name__ == "__main__":
    main()