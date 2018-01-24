from apns2.client import APNsClient
from apns2.payload import Payload
import yaml

with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

apnsConfig = config['apns']
cert = apnsConfig['cert']
sandbox = apnsConfig['sandbox']

class Notifier:
    def __init__(self):
        self.client = APNsClient(cert, use_sandbox=sandbox, use_alternative_port=False)
        
    def send(self, token, message, count, isSilent):
        # TODO utilize isSilent
        payload = Payload(alert=message, sound="default", badge=count)
        topic = 'com.bfichter.KookMachine'
        self.client.send_notification(token, payload, topic)
        