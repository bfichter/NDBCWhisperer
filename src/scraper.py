from lxml import html
from buoy import Buoy
from reading import Reading
import requests
import re

class Scraper:
    def __init__(self, stationID, db):
        self.stationID = stationID
        self.xPathPrefix = '//*[@id="contenttable"]/tr/td[3]/table/tr[td = '
        self.xPathSuffix = ']/td[3]/text()'
        self.db = db
    
    def scrape(self):
        page = requests.get('http://www.ndbc.noaa.gov/station_page.php?station=' + self.stationID)
        
        self.tree = html.fromstring(page.content)
        
        if not self.isValidStation():
            return
        
        
        # setup the dictionaries
        buoy = {}
        reading = {}
        
        buoy['station_id'] = self.stationID
        reading['station_id'] = self.stationID
        
        # Main box variables
        windDirection = self.grabDirectionTupleFromString(self.grabFromTree('"Wind Direction (WDIR):"'))
        reading['wind_direction_compass'] = windDirection[0]
        reading['wind_direction_angle'] = windDirection[1]
        reading['wind_speed'] = self.grabNumberFromString(self.grabFromTree('"Wind Speed (WSPD):"'))
        reading['wind_gust'] = self.grabNumberFromString(self.grabFromTree('"Wind Gust (GST):"'))
        reading['wave_height'] = self.grabNumberFromString(self.grabFromTree('"Wave Height (WVHT):"')) # this also seems to track 'Significant Wave Height'
        reading['dominant_period'] = self.grabNumberFromString(self.grabFromTree('"Dominant Wave Period (DPD):"'))
        reading['average_period'] = self.grabNumberFromString(self.grabFromTree('"Average Period (APD):"'))
        reading['wave_direction'] = self.grabDirectionTupleFromString(self.grabFromTree('"Mean Wave Direction (MWD):"'))
        reading['air_temperature'] = self.grabNumberFromString(self.grabFromTree('"Air Temperature (ATMP):"'))
        
        # Secondary box variables
        reading['significant_wave_height'] = self.grabNumberFromString(self.grabFromTree('"Significant Wave Height (WVHT):"'))
        reading['swell_height'] = self.grabNumberFromString(self.grabFromTree('"Swell Height (SwH):"'))
        reading['swell_period'] = self.grabNumberFromString(self.grabFromTree('"Swell Period (SwP):"'))
        reading['swell_direction'] = self.grabCompassFromString(self.grabFromTree('"Swell Direction (SwD):"'))
        reading['wind_wave_height'] = self.grabNumberFromString(self.grabFromTree('"Wind Wave Height (WWH):"'))
        reading['wind_wave_period'] = self.grabNumberFromString(self.grabFromTree('"Wind Wave Period (WWP):"'))
        reading['wind_wave_direction'] = self.grabCompassFromString(self.grabFromTree('"Wind Wave Direction (WWD):"'))
        reading['average_wave_period'] = self.grabNumberFromString(self.grabFromTree('"Average Wave Period (APD):"'))
        
        # Grab the time
        reading['first_time'] = self.grabLocalTime(True)
        reading['second_time'] = self.grabLocalTime(False)
        
        # Grab the buoy name 
        buoy['name'] = self.grabBuoyName()
        
        # Instantiate model objects
        buoyObject = Buoy(**buoy)
        readingObject = Reading(**reading)
        
        readingObject.id = self.db.readings.insert_one(readingObject.mongoDB()).inserted_id
        self.db.buoys.update({'station_id': self.stationID}, buoyObject.mongoDB(), upsert = True)
        
        cursor = self.db.buoys.find({})
        for document in cursor: 
            print(document)
            
        cursor = self.db.readings.find({})
        for document in cursor: 
            print(document)
        
    def grabFromTree(self, variableDescription):
        valueList = self.tree.xpath(self.xPathPrefix +  variableDescription + self.xPathSuffix)
        
        if len(valueList) > 0:
            return valueList[0]
        else:
            return ''
        
    # these strings only have one number in them
    def grabNumberFromString(self, rawString):
        numberList = re.findall(r"[-+]?\d*\.\d+|\d+", rawString)
        
        if len(numberList) > 0:
            return float(numberList[0])
        else:
            return None
        
    # the string is like ' SE (direction 320 degrees true) '
    def grabCompassFromString(self, rawString):
        strippedString = rawString.replace(" ", "")
        splitList = strippedString.split('(')
        
        if len(splitList) > 0:
            return splitList[0]
        else:
            return None
    
    def grabDirectionTupleFromString(self, rawString):
        compass = self.grabCompassFromString(rawString)
        angle = self.grabNumberFromString(rawString)
        
        if compass is None or angle is None:
            return (None, None)
        else:
            return (compass, angle)
        
    def grabLocalTime(self, isFirstBox):
        if isFirstBox:
            timeList = self.tree.xpath('//*[@id="contenttable"]/tr/td[3]/table[2]/caption/text()[2]')
        else:
            timeList = self.tree.xpath('//*[@id="contenttable"]/tr/td[3]/table[5]/caption/text()[2]') 
        
        if len(timeList) == 0:
            return None
        
        rawTime = timeList[0]
        
        # rawTime should be "<stuff>(5:30 pm est)<stuff>
        splitList = rawTime.split('(')
        
        if len(splitList) < 2:
            return None
        
        firstSplit = splitList[1]
        splitList = firstSplit.split(')')
        
        if len(splitList) < 2:
            return None
        
        return splitList[0]
    
    def grabBuoyName(self):
        nameList = self.tree.xpath('//*[@id="contenttable"]/tr/td[3]/h1/text()')
        
        if len(nameList) == 0:
            return None
        
        # there are some differences b/w stations here, this seems to catch all of them
        rawName = nameList[len(nameList) - 1]
        
        splitList = rawName.split('-')
        
        if len(splitList) < 2:
            return None
        
        name = splitList[1].strip()
        
        return name
    
    def isValidStation(self):
        titleList = self.tree.xpath('/html/head/title/text()')
        
        if len(titleList) == 0:
            return True
        
        title = titleList[0]
        
        return title != 'NDBC - Station not found'
    