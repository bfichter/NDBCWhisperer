from buoy import Buoy
from compass import compassDict
from reading import Reading
import requests
import urllib2

# Grabs new report for whatever station specified
# Updates the Reading in Mongo
# Typically this will be used on the hourly update
# And whenever someone requests a new buoy
class BuoyUpdater:
    def __init__(self, db):
        self.db = db

    def update(self, stationID):
        potentialBuoy = self.db.potentialBuoys.find_one({'station_id': stationID})
         
        if potentialBuoy is None:
            # This is not a valid stationID
            return
        buoyName = potentialBuoy['name']
        buoy = {
            'station_id': potentialBuoy['station_id'],
            'name': buoyName
        }

        # gets you the first box:
        # https://www.ndbc.noaa.gov/data/realtime2/41013.txt
        # then this for second box:
        # https://www.ndbc.noaa.gov/data/realtime2/44013.spec
        
        try:
            firstBoxData = urllib2.urlopen("https://www.ndbc.noaa.gov/data/realtime2/" + stationID + ".txt").read(2000)
            secondBoxData = urllib2.urlopen("https://www.ndbc.noaa.gov/data/realtime2/" + stationID + ".spec").read(2000)
        except urllib2.HTTPError:
            print('error caught trying to fetch ' + stationID)
            # TODO make this still update the reading as empty or something
            return
        
        # For some stations (e.g. 44008) the first box data is taken every 10 min,
        # but only 1 per hour (usually on the 50 min) has all the data.
        
        # First box columns and units:
        # YY  MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS PTDY  TIDE
        # yr  mo dy hr mn degT m/s  m/s     m   sec   sec degT   hPa  degC  degC  degC  nmi  hPa    ft
        
        
        # Second box columns and units:
        # YY  MM DD hh mm WVHT  SwH  SwP  WWH  WWP SwD WWD  STEEPNESS  APD MWD
        # yr  mo dy hr mn    m    m  sec    m  sec  -  degT     -      sec degT
        
        lines = firstBoxData.split('\n')
        firstLine = lines[0]
        firstLineValues = firstLine.split()
        
        minuteIndex = firstLineValues.index('mm')
        
        readingLines = lines[2:]
        
        # default to the latest if no 50 min readings are found
        latestFullReadingValues = readingLines[0].split()
        
        for readingLine in readingLines:
            readingValues = readingLine.split()
            minutes = readingValues[minuteIndex]
            if minutes == '50':
                latestFullReadingValues = readingValues
                break
        
        firstBoxDictionary = {}
        
        for index, label in enumerate(firstLineValues):
            readingValue = latestFullReadingValues[index]
            firstBoxDictionary[label] = readingValue
            
        lines = secondBoxData.split('\n')
        firstLine = lines[0]
        firstLineValues = firstLine.split()
        
        readingLine = lines[2]
        
        latestFullReadingValues = readingLine.split()
                
        secondBoxDictionary = {}
        
        for index, label in enumerate(firstLineValues):
            readingValue = latestFullReadingValues[index]
            secondBoxDictionary[label] = readingValue
        
        waveHeight = self.feetFromReading(firstBoxDictionary, 'WVHT')
        wavePeriod = self.floatFromReading(firstBoxDictionary, 'DPD')
        waveDirection = self.floatFromReading(firstBoxDictionary, 'MWD')
        swellHeight = self.feetFromReading(secondBoxDictionary, 'SwH')
        swellPeriod = self.floatFromReading(secondBoxDictionary, 'SwP')
        swellDirection = self.compassToDegreesFromReading(secondBoxDictionary, 'SwD') # Are all of these Strings?
        #2019-10-20T17:50:00Z
        try:
            wavesDatetime = (firstBoxDictionary['#YY'] + 
            '-' + firstBoxDictionary['MM'] +
            '-' + firstBoxDictionary['DD'] +
            'T' + firstBoxDictionary['hh'] +
            ':' + firstBoxDictionary['mm'] + ':00Z')
        except KeyError:
            wavesDatetime = None 
        windDirection = self.floatFromReading(firstBoxDictionary, 'WDIR')
        windSpeed = self.knotsFromReading(firstBoxDictionary, 'WSPD') 
                
        
        reading = {
            'station_id': stationID,
            'buoy_name': buoyName,
            'wind_direction': windDirection,
            'wind_speed': windSpeed,
            'wave_height': waveHeight,
            'dominant_period': wavePeriod,
            'wave_direction': waveDirection,
            'swell_height': swellHeight,
            'swell_period': swellPeriod,
            'swell_direction': swellDirection,
            'datetime': wavesDatetime
        }
         
        # Remove nulls
        reading = {k: v for k, v in reading.items() if v != None}
         
        # Instantiate model objects
        buoyObject = Buoy(**buoy)
        readingObject = Reading(**reading)
         
        #readingObject.id = self.db.readings.insert_one(readingObject.mongoDB()).inserted_id
        self.db.readings.update({'station_id': stationID}, readingObject.mongoDB(), upsert = True)
        self.db.buoys.update({'station_id': stationID}, buoyObject.mongoDB(), upsert = True)
    
    def ndbcDictionaryForRequest(self, requestType, stationID):
        payload = {
            'request': 'GetObservation',
            'service': 'SOS',
            'version': '1.0.0',
            'offering': 'urn:ioos:station:wmo:' + stationID,
            'observedproperty': requestType,
            'responseformat': 'text/csv',
            'eventtime': 'latest'
        }
        request = requests.get('https://sdf.ndbc.noaa.gov/sos/server.php', params = payload)
        list = request.text.split(',')
        
        if len(list) % 2 != 0:
            # There's a trailing comma which produces a dummy element making this an odd number list
            list.pop()
        
        keys = list[:len(list)//2]
        values = list[len(list)//2:]
        
        reading = {}
        for key, value in zip(keys, values):
            print(key)
            reading[key] = value
            
        return reading
    
    def floatFromReading(self, reading, key):
        try:
            return round(float(reading[key]), 1)
        except (ValueError, KeyError):
            return None
    
    def feetFromReading(self, reading, key):
        # In order to map to the ft readings on ndbc,
        # we need to round before converting, then round again.
        # Obviously this loses information, but I've decided that
        # being consistent with ndbc is more important than retaining
        # reading precision.
        try:
            roundedMeters = round(float(reading[key]), 1)
        except (ValueError, KeyError):
            return None
        
        feet = roundedMeters * 3.28084
        return round(feet, 1)
    
    def knotsFromReading(self, reading, key):
        try:
            roundedMetersPerSecond = round(float(reading[key]), 1)
        except (ValueError, KeyError):
            return None
        
        knots = roundedMetersPerSecond * 1.94384
        return round(knots, 1)
    
    def fromDirectionFromReading(self, reading, key):
        # For some reason wave direction is being reported as 'to direction'. So we need
        # to flip 180 degrees to make it the 'from direction'
        try:
            toDirection = round(float(reading[key]), 1)
        except (ValueError, KeyError):
            return None
        
        fromDirection = (toDirection + 180) % 360
        return fromDirection
    
    def compassToDegreesFromReading(self, reading, key):
        try:
            compass = compassDict[reading[key]]
        except (KeyError):
            return None
        
        return compass
