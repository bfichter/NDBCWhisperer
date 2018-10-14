import requests

payload = {
    'request': 'GetObservation',
    'service': 'SOS',
    'version': '1.0.0',
    'offering': 'urn:ioos:station:wmo:44013',
    'observedproperty': 'waves',
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

print(reading)
# "check out wind"
# "check out invalid stations" need to have
# "split on comma"
# "split resulting array in half (make sure even number of elements)"
# "make a dictionary of results"
# "look for the relevant keys"
# transform to american units 
# "make sure this works for different stations"
