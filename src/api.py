from eve import Eve
from scraper import Scraper
from pymongo import MongoClient

def pre_buoys_get_callback(request, lookup):
    client = MongoClient('localhost', 27017)
    stationID = lookup["station_id"]
    db = client.ndbc
    # clean all this up
    # possibly hold onto a db connection outside of eve
    if db.buoys.find( { "station_id" : stationID } ).count() > 0:
        print("HIT THE CACHE")
        client.close()
        return
    
    scraper = Scraper(lookup["station_id"], db)
    scraper.scrape()
    client.close()

app = Eve()
app.on_pre_GET_buoys += pre_buoys_get_callback

if __name__ == '__main__':
    app.run(port=5002, debug=True) # was conflicting with something on 5000
    