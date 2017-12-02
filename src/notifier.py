from apns2.client import APNsClient
from apns2.payload import Payload

class Notifier:
    def __init__(self):
        self.client = APNsClient('kmDevPush.pem', use_sandbox=True, use_alternative_port=False)
        
    def send(self, token, message, count, isSilent):
        # TODO utilize isSilent
        payload = Payload(alert=message, sound="default", badge=count)
        topic = 'com.bfichter.KookMachine'
        self.client.send_notification(token, payload, topic)
         