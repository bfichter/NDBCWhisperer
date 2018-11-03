from buoy import Buoy
from reading import Reading
import requests

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
        
        print('updating for ' + stationID)
        wavesReading = self.ndbcDictionaryForRequest('waves', stationID)
        windsReading = self.ndbcDictionaryForRequest('winds', stationID)
        waveHeight = self.feetFromReading(wavesReading, '"sea_surface_wave_significant_height (m)"')
        wavePeriod = self.floatFromReading(wavesReading, '"sea_surface_wave_peak_period (s)"')
        waveDirection = self.fromDirectionFromReading(wavesReading, '"sea_surface_wave_to_direction (degree)"')
        
        swellHeight = self.feetFromReading(wavesReading, '"sea_surface_swell_wave_significant_height (m)"')
        swellPeriod = self.floatFromReading(wavesReading, '"sea_surface_swell_wave_period (s)"')
        swellDirection = self.fromDirectionFromReading(wavesReading, '"sea_surface_swell_wave_to_direction (degree)"')
        
        wavesDatetime = wavesReading['date_time']
        
        windSpeed = self.knotsFromReading(windsReading, '"wind_speed (m/s)"')
        windDirection = self.floatFromReading(windsReading, '"wind_from_direction (degree)"') 
        
        print(waveHeight)
        print(wavePeriod)
        print(waveDirection)
        print(swellHeight)
        print(swellPeriod)
        print(swellDirection)
        print(wavesDatetime)
        print(windDirection)
        print(windSpeed)
        
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
