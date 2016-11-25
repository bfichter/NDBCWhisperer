from lxml import html
import requests

stationID = '44013'
page = requests.get('http://www.ndbc.noaa.gov/station_page.php?station=' + stationID)
tree = html.fromstring(page.content)

xPathPrefix = '//*[@id="contenttable"]/tr/td[3]/table/tr[td = '
xPathSuffix = ']/td[3]/text()'

# Main box variables
windDirection = tree.xpath(xPathPrefix +  '"Wind Direction (WDIR):"' + xPathSuffix)
windSpeed = tree.xpath(xPathPrefix + '"Wind Speed (WSPD):"' + xPathSuffix)
windGust = tree.xpath(xPathPrefix + '"Wind Gust (GST):"' + xPathSuffix)
waveHeight = tree.xpath(xPathPrefix + '"Wave Height (WVHT):"' + xPathSuffix)
dominantPeriod = tree.xpath(xPathPrefix + '"Dominant Wave Period (DPD):"' + xPathSuffix)
averagePeriod = tree.xpath(xPathPrefix + '"Average Period (APD):"' + xPathSuffix)
meanWaveDirection = tree.xpath(xPathPrefix + '"Mean Wave Direction (MWD):"' + xPathSuffix)
airTemperature = tree.xpath(xPathPrefix + '"Air Temperature (ATMP):"' + xPathSuffix)



print windDirection
print windSpeed
print windGust
print waveHeight
print dominantPeriod
print meanWaveDirection
print airTemperature
