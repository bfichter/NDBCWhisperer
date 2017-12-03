from scraper import Scraper
from pymongo import MongoClient
from notifier import Notifier

class NDBCDaemon:
    def run(self):
        #push test
        #notifier = Notifier()
        #notifier.send('5886e435dadfbd10f15df6e8f2c73b7eecb7de9eaa9e5becb31f83894ed707a1', 'Test Message', 1, False)
        
        client = MongoClient('localhost', 27017)
        db = client.ndbc
        self.refreshReadings(db)
        self.notifyUsers(db)
        client.close()
    
    def refreshReadings(self, db):
        # Get all readings from Mongo
        # and run scrape() on each
        for buoy in db.buoys.find():
            Scraper(buoy['station_id'], db).scrape()
            print(buoy['station_id'])
        
    def notifyUsers(self, db):
        notifier = Notifier()
        for user in db.users.find():
            userID = user['user_id']
            alerts = []
            for alert in db.alerts.find({'user_id': userID}):
                print(alert)
                # I think this should work, but gotta clear out old users
        # Get all users
            # Get all alerts
            # Figure out which alerts are valid
            # Compile into a message
            # Get all devices for that user
            # and blast off a note to each device