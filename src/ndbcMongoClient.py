from pymongo import MongoClient
import yaml

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

mongoConfig = config['mongo']
debug = config['general']['debug']
mongoHost = mongoConfig['host']
mongoPort = mongoConfig['port']
if not debug:
    mongoUsername = mongoConfig['username']
    mongoPassword = mongoConfig['password']

class NDBCMongoClient:
    def __init__(self):
        print(mongoHost)
        print(mongoPort)
        self.client = MongoClient(mongoHost, mongoPort) if debug else MongoClient(host=mongoHost, port=mongoPort, username=mongoUsername, password=mongoPassword, authSource='ndbc')
