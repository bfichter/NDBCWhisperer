from eve import Eve
from buoyUpdater import BuoyUpdater
from ndbcMongoClient import NDBCMongoClient
from ndbcDaemon import NDBCDaemon
from notifier import Notifier
from potentialBuoysUpdater import PotentialBuoysUpdater

def updateBuoyIfNecessary(stationID):
    client = NDBCMongoClient().client
    db = client.ndbc
    #Testing
    PotentialBuoysUpdater(db).update()
    # clean all this up
    # possibly hold onto a db connection outside of eve
    if db.buoys.find( { "station_id" : stationID } ).count() > 0:
        print("HIT THE CACHE")
        client.close()
        return
    
    buoyUpdater = BuoyUpdater(db)
    buoyUpdater.update(stationID)
    client.close()

def notifyUser(userID):
    client = NDBCMongoClient().client
    db = client.ndbc
    for user in db.users.find():
        NDBCDaemon().notifyUser(db, user, Notifier())
    client.close()

# This isn't getting used for anything anymore, gonna leave it in case
# We want to use it for some reason
def pre_buoys_get_callback(request, lookup):
    stationID = lookup["station_id"]
    updateBuoyIfNecessary(stationID)
    
def pre_readings_get_callback(request, lookup):
    stationID = lookup["station_id"]
    updateBuoyIfNecessary(stationID)

def on_inserted_alerts_callback(items):
    print(items)
    for item in items:
        print('wtf')
        userID = item["user_id"]
        notifyUser(userID)

def on_deleted_alerts(item):
    userID = item["user_id"]
    notifyUser(userID)
        
app = Eve()
app.on_pre_GET_buoys += pre_buoys_get_callback
app.on_pre_GET_readings += pre_readings_get_callback

# client = NDBCMongoClient().client
# db = client.ndbc
# # Refresh the potential buoys db
# PotentialBuoysUpdater(db).update()
# These following two callbacks are to synchronize the badge count on the app
# These obviously come with a substantial performance hit per request (especially update which is currently delete/create)
# If it's not worth it, can remove these or try to make them async somehow
# app.on_inserted_alerts += on_inserted_alerts_callback
# app.on_deleted_item_alerts += on_deleted_alerts

if __name__ == '__main__':
    app.run(port=5002, debug=True) # was conflicting with something on 5000
    