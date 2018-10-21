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
        windsReading = self.ndbcDictionaryForRequest('winds', stationID)
        print(windsReading)
        waveHeightMeters = float(wavesReading['"sea_surface_wave_significant_height (m)"']) # this float call might crash if param doesn't exist?
        waveHeightFeet = self.feetFromMeters(waveHeightMeters)
        print(waveHeightFeet)
        
    
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
            reading[key] = value
            
        return reading
    
    def feetFromMeters(self, meters):
        # In order to map to the ft readings on ndbc,
        # we need to round before converting, then round again.
        # Obviously this loses information, but I've decided that
        # being consistent with ndbc is more important than retaining
        # reading precision.
        roundedMeters = round(meters, 1)
        feet = roundedMeters * 3.28084
        return round(feet, 1)
        


updater = BuoyUpdater("dummy db, python is weird")
updater.update('44013')
# print(reading)
# print('------')
# 
# stringReading = reading['"sea_surface_wave_significant_height (m)"']
# floatReading = float(stringReading)
# significantWaveHeight = round(floatReading, 1)
# significantWaveHeight *= 3.28084
# significantWaveHeight = round(significantWaveHeight, 1)
# 
# #significantWaveHeight = reading['"sea_surface_wave_significant_height (m)"']
# print(significantWaveHeight)

# "check out wind"
# "check out invalid stations" need to have
# "split on comma"
# "split resulting array in half (make sure even number of elements)"
# "make a dictionary of results"
# "look for the relevant keys"
# transform to american units 
# "make sure this works for different stations"
