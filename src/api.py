from eve import Eve
from eve.auth import BasicAuth
from werkzeug.security import check_password_hash, generate_password_hash
from buoyUpdater import BuoyUpdater
from ndbcMongoClient import NDBCMongoClient
from ndbcDaemon import NDBCDaemon
from notifier import Notifier
from potentialBuoysUpdater import PotentialBuoysUpdater
from werkzeug import generate_password_hash

def updateBuoyIfNecessary(stationID):
    # use eve's native db connection
    db = app.data.driver.db
    if db.buoys.find( { "station_id" : stationID } ).count() > 0:
        print("HIT THE CACHE")
        return
    
    buoyUpdater = BuoyUpdater(db)
    buoyUpdater.update(stationID)

def notifyUser(userID):
    client = NDBCMongoClient().client
    db = client.ndbc
    for user in db.users.find():
        NDBCDaemon().notifyUser(db, user, Notifier())
    client.close()

# This isn't getting used for anything anymore, gonna leave it in case
# We want to use it for some reason
def pre_buoys_get_callback(request, lookup):
    stationID = lookup['station_id']
    updateBuoyIfNecessary(stationID)
    
def pre_readings_get_callback(request, lookup):
    stationID = lookup['station_id']
    updateBuoyIfNecessary(stationID)

def insert_users_callback(users):
    for user in users:
        user['password'] = generate_password_hash(user['password'])
    
class EveAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        # Only time auth isn't required is user creation
        if resource == 'users' and method == 'POST':
            return True
        
        user = app.data.driver.db.users.find_one({'user_id': username})
        return user and check_password_hash(user['password'], password)

app = Eve(auth=EveAuth)
#app = Eve()
app.on_pre_GET_buoys += pre_buoys_get_callback
app.on_pre_GET_readings += pre_readings_get_callback
app.on_insert_users += insert_users_callback

if __name__ == '__main__':
    app.run(port=5002, debug=True) # was conflicting with something on 5000
    