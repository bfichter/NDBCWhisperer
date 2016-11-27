from scraper import Scraper

def main():
    stationID = '46002'
    scraper = Scraper(stationID)
    scraper.scrape()

if __name__ == "__main__":
    main()