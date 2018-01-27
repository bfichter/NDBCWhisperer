from scraper import Scraper
from ndbcMongoClient import NDBCMongoClient
from notifier import Notifier

class NDBCDaemon:
    def run(self):
        #push test
        #notifier = Notifier()
        #notifier.send('5886e435dadfbd10f15df6e8f2c73b7eecb7de9eaa9e5becb31f83894ed707a1', 'Test Message', 1, False)
        client = NDBCMongoClient().client
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
            print(userID)
            alerts = []
            for alert in db.alerts.find({'user_id': userID}):
                # Could optimize by maintaining a dict of Readings
                # Not sure how slow Mongo lookups will be
                reading = db.readings.find_one({'station_id': alert['station_id']})
                
                if reading is not None and self.isFulfilled(alert, reading):
                    print('----FULFILLED-----')
                    print('Alert Is:')
                    print(alert)
                    print('Reading Is:')
                    print(reading)
                    print('_End_Fulfilled_')
                    alerts.append(alert)
                else:
                    print('NOT FULFILLED')
                    print('Alert Is:')
                    print(alert)
                    print('Reading Is:')
                    print(reading)
                    print('END NOT FULFILLED')
            
            count = len(alerts)
            message = str(count) + " active alerts kook. This message sucks and needs to be better"
            for device in db.devices.find({'user_id': userID}):
                try:
                    notifier.send(device['token'], message, count, False)
                except:
                    print("APNS error, couldn't send to " + device['token']) 
            
    # we should actually get some tests on this, gonna be fucked otherwise        
    def isFulfilled(self, alert, reading):
        if 'wind_speed_max' in alert:
            if 'wind_speed' not in reading:
                return False
            
            if reading['wind_speed'] > alert['wind_speed_max']:
                return False
        
        if 'wave_height_min' in alert:
            if 'wave_height' not in reading:
                return False
            
            if reading['wave_height'] < alert['wave_height_min']:
                return False
            
        if 'wave_period_min' in alert:
            if 'wave_period' not in reading:
                return False
            
            if reading['wave_period'] < alert['wave_period_min']:
                return False
        
        if 'swell_height_min' in alert:
            if 'swell_height' not in reading:
                return False
            
            if reading['swell_height'] < alert['swell_height_min']:
                return False
            
        if 'swell_period_min' in alert:
            if 'swell_period' not in reading:
                return False
            
            if reading['swell_period'] < alert['swell_period_min']:
                return False
        
        if 'wind_direction_range' in alert:
            if 'wind_direction' not in reading:
                return False
            
            if not self.isRangeFulfilled(alert['wind_direction_range'], reading['wind_direction']):
                return False
        
        if 'wave_direction_range' in alert:
            if 'wave_direction' not in reading:
                return False
            
            if not self.isRangeFulfilled(alert['wave_direction_range'], reading['wave_direction']):
                return False
            
        if 'swell_direction_range' in alert:
            if 'swell_direction' not in reading:
                return False
            
            if not self.isRangeFulfilled(alert['swell_direction_range'], reading['swell_direction']):
                return False
            
        # Got through the gauntlet, this alert is valid
        return True
    
    # Parameters are rangeType and directionType defined in settings.py
    # Logic/naming mirrors client logic/naming
    def isRangeFulfilled(self, directionRange, direction):
        requiredClockwiseStart = directionRange['clockwise_start']
        requiredClockwiseEnd = directionRange['clockwise_end']
        readingAngle = direction['angle']
        
        if requiredClockwiseStart is None or requiredClockwiseEnd is None or readingAngle is None:
            return False
        
        if requiredClockwiseStart < requiredClockwiseEnd:
            return readingAngle >= requiredClockwiseStart and readingAngle <= requiredClockwiseEnd
        
        if requiredClockwiseStart > requiredClockwiseEnd:
            if readingAngle >= requiredClockwiseStart and readingAngle <= 360:
                return True
            
            if readingAngle <= requiredClockwiseEnd and readingAngle >= 0:
                return True
            
            return False
        
        return readingAngle == requiredClockwiseStart and readingAngle == requiredClockwiseEnd
    
    