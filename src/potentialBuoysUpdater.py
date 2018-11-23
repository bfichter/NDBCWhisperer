from xml.etree import ElementTree
from ndbcMongoClient import NDBCMongoClient
from potentialBuoy import PotentialBuoy
import requests

class PotentialBuoysUpdater:
    def __init__(self, db):
        self.db = db

    def update(self):
        request = requests.get('https://www.ndbc.noaa.gov/activestations.xml')
        parsed = ElementTree.XMLID(request.content)
        elements = parsed[1]
        for stationID, element in elements.items():
            attributes = element.attrib
            name = attributes['name']
            potentialBuoy = {
                'station_id': stationID,
                'name': name
            }
            print potentialBuoy
            potentialBuoyObject = PotentialBuoy(**potentialBuoy)
            self.db.potentialBuoys.update({'station_id': stationID}, potentialBuoyObject.mongoDB(), upsert = True)
            
if __name__ == "__main__":
    client = NDBCMongoClient().client
    db = client.ndbc
    PotentialBuoysUpdater().update()
    
            