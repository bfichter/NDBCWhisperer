from scraper import Scraper

def main():
    stationID = '46042'
    scraper = Scraper(stationID)
    scraper.scrape()

if __name__ == "__main__":
    main()