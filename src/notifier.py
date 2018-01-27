from apns2.client import APNsClient
from apns2.payload import Payload
from config import config

apnsConfig = config['apns']
cert = apnsConfig['cert']
sandbox = apnsConfig['sandbox']

class Notifier:
    def __init__(self):
        self.client = APNsClient(cert, use_sandbox=sandbox, use_alternative_port=False)
        
    def send(self, token, message, count, isSilent):
        if isSilent:
            payload = Payload(contentAvailable=True, badge=count)
        else:
            # TODO create custom sound (more so on client)
            payload = Payload(alert=message, sound="default", badge=count)
        topic = 'com.bfichter.KookMachine'
        self.client.send_notification(token, payload, topic)
        