import sys
import os
from apns2.client import APNsClient
from apns2.payload import Payload
from config import config
from ndbcMongoClient import NDBCMongoClient

SENT_LOG = '/root/broadcast_sent.log'

def main():
    if len(sys.argv) < 2:
        print('usage: python broadcast.py "message"')
        sys.exit(1)
    message = sys.argv[1]

    alreadySent = set()
    if os.path.exists(SENT_LOG):
        with open(SENT_LOG) as f:
            alreadySent = set(line.strip() for line in f)

    apnsConfig = config['apns']
    client = APNsClient(apnsConfig['cert'], use_sandbox=apnsConfig['sandbox'])
    # No badge so we don't clobber anyone's alert count
    payload = Payload(alert=message, sound="default")
    topic = 'com.bfichter.KookMachine'

    db = NDBCMongoClient().client.ndbc
    ok = 0
    skipped = 0
    failed = 0
    with open(SENT_LOG, 'a') as log:
        for device in db.devices.find():
            token = device['token']
            if token in alreadySent:
                skipped += 1
                continue
            try:
                client.send_notification(token, payload, topic)
                log.write(token + '\n')
                log.flush()
                ok += 1
            except Exception as e:
                failed += 1
                print('FAILED %s: %r' % (token, e))
    print('sent %d, skipped %d already-sent, %d failed' % (ok, skipped, failed))

if __name__ == '__main__':
    main()
