from buoy import Buoy
from reading import Reading
import requests

class BuoyUpdater:
    def __init__(self, db):
        self.db = db

    def update(self, stationID):
        # TODO have some exists/buoy name gathering function here
        print('updating for ' + stationID)
        wavesReading = self.ndbcDictionaryForRequest('waves', stationID)
        print(wavesReading)
        windsReading = self.ndbcDictionaryForRequest('winds', stationID)
        print(windsReading)
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
        except ValueError:
            return None
    
    def feetFromReading(self, reading, key):
        # In order to map to the ft readings on ndbc,
        # we need to round before converting, then round again.
        # Obviously this loses information, but I've decided that
        # being consistent with ndbc is more important than retaining
        # reading precision.
        try:
            roundedMeters = round(float(reading[key]), 1)
        except ValueError:
            return None
        
        feet = roundedMeters * 3.28084
        return round(feet, 1)
    
    def knotsFromReading(self, reading, key):
        try:
            roundedMetersPerSecond = round(float(reading[key]), 1)
        except ValueError:
            return None
        
        knots = roundedMetersPerSecond * 1.94384
        return round(knots, 1)
    
    def fromDirectionFromReading(self, reading, key):
        # For some reason wave direction is being reported as 'to direction'. So we need
        # to flip 180 degrees to make it the 'from direction'
        try:
            toDirection = round(float(reading[key]), 1)
        except ValueError:
            return None
        
        fromDirection = (toDirection + 180) % 360
        return fromDirection


updater = BuoyUpdater("dummy db, python is weird")
updater.update('44013')
#updater.update('44008')
