from lxml import html
import requests

class Scraper:
    def __init__(self, stationID):
        self.stationID = stationID
        self.xPathPrefix = '//*[@id="contenttable"]/tr/td[3]/table/tr[td = '
        self.xPathSuffix = ']/td[3]/text()'
    
    def scrape(self):
        page = requests.get('http://www.ndbc.noaa.gov/station_page.php?station=' + self.stationID)
        self.tree = html.fromstring(page.content)
        
        # Main box variables
        windDirection = self.grabFromTree('"Wind Direction (WDIR):"')
        windSpeed = self.grabFromTree('"Wind Speed (WSPD):"')
        windGust = self.grabFromTree('"Wind Gust (GST):"')
        waveHeight = self.grabFromTree('"Wave Height (WVHT):"')
        dominantPeriod = self.grabFromTree('"Dominant Wave Period (DPD):"')
        averagePeriod = self.grabFromTree('"Average Period (APD):"')
        meanWaveDirection = self.grabFromTree('"Mean Wave Direction (MWD):"')
        airTemperature = self.grabFromTree('"Air Temperature (ATMP):"')
        print windDirection
        print windSpeed
        print windGust
        print waveHeight
        print dominantPeriod
        print averagePeriod
        print meanWaveDirection
        print airTemperature
        
    # Grab the raw string from the parsed tree with xPath
    def grabFromTree(self, variableDescription):
        return self.tree.xpath(self.xPathPrefix +  variableDescription + self.xPathSuffix)
    