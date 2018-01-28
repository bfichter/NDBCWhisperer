from eve import Eve
from scraper import Scraper
from ndbcMongoClient import NDBCMongoClient

def scrapeIfNecessary(stationID):
    client = NDBCMongoClient().client
    db = client.ndbc
    # clean all this up
    # possibly hold onto a db connection outside of eve
    if db.buoys.find( { "station_id" : stationID } ).count() > 0:
        print("HIT THE CACHE")
        client.close()
        return
    
    scraper = Scraper(stationID, db)
    scraper.scrape()
    client.close()

# This isn't getting used for anything anymore, gonna leave it in case
# We want to use it for some reason
def pre_buoys_get_callback(request, lookup):
    stationID = lookup["station_id"]
    scrapeIfNecessary(stationID)
    
def pre_readings_get_callback(request, lookup):
    stationID = lookup["station_id"]
    scrapeIfNecessary(stationID) 

app = Eve()
app.on_pre_GET_buoys += pre_buoys_get_callback
app.on_pre_GET_readings += pre_readings_get_callback

if __name__ == '__main__':
    app.run(port=5002, debug=True) # was conflicting with something on 5000
    