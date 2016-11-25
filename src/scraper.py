from lxml import html
import requests
import re

class Scraper:
    def __init__(self, stationID):
        self.stationID = stationID
        self.xPathPrefix = '//*[@id="contenttable"]/tr/td[3]/table/tr[td = '
        self.xPathSuffix = ']/td[3]/text()'
    
    def scrape(self):
        page = requests.get('http://www.ndbc.noaa.gov/station_page.php?station=' + self.stationID)
        self.tree = html.fromstring(page.content)
        
        # Main box variables
        windDirection = self.grabDirectionTupleFromString(self.grabFromTree('"Wind Direction (WDIR):"'))
        windSpeed = self.grabNumberFromString(self.grabFromTree('"Wind Speed (WSPD):"'))
        windGust = self.grabNumberFromString(self.grabFromTree('"Wind Gust (GST):"'))
        waveHeight = self.grabNumberFromString(self.grabFromTree('"Wave Height (WVHT):"'))
        dominantPeriod = self.grabNumberFromString(self.grabFromTree('"Dominant Wave Period (DPD):"'))
        averagePeriod = self.grabNumberFromString(self.grabFromTree('"Average Period (APD):"'))
        meanWaveDirection = self.grabDirectionTupleFromString(self.grabFromTree('"Mean Wave Direction (MWD):"'))
        airTemperature = self.grabNumberFromString(self.grabFromTree('"Air Temperature (ATMP):"'))
        
        print windDirection
        print windSpeed
        print windGust
        print waveHeight
        print dominantPeriod
        print averagePeriod
        print meanWaveDirection
        print airTemperature
        
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
        velocity = self.grabNumberFromString(rawString)
        
        if compass is None or velocity is None:
            return None
        else:
            return (compass, velocity)
    