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
        
        # Secondary box variables
        significantWaveHeight = self.grabNumberFromString(self.grabFromTree('"Significant Wave Height (WVHT):"'))
        swellHeight = self.grabNumberFromString(self.grabFromTree('"Swell Height (SwH):"'))
        swellPeriod = self.grabNumberFromString(self.grabFromTree('"Swell Period (SwP):"'))
        swellDirection = self.grabCompassFromString(self.grabFromTree('"Swell Direction (SwD):"'))
        windWaveHeight = self.grabNumberFromString(self.grabFromTree('"Wind Wave Height (WWH):"'))
        windWavePeriod = self.grabNumberFromString(self.grabFromTree('"Wind Wave Period (WWP):"'))
        windWaveDirection = self.grabCompassFromString(self.grabFromTree('"Wind Wave Direction (WWD):"'))
        averageWavePeriod = self.grabNumberFromString(self.grabFromTree('"Average Wave Period (APD):"'))
        
        # Grab the time
        print significantWaveHeight
        print swellHeight
        print swellPeriod
        print swellDirection
        print windWaveHeight
        print windWavePeriod
        print windWaveDirection
        print averageWavePeriod
        
        localTime = self.grabLocalTime()
        
        print localTime
        
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
        
    def grabLocalTime(self):
        timeList = self.tree.xpath('//*[@id="contenttable"]/tr/td[3]/table[2]/caption/text()[2]')
        
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
    