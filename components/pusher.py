from gcm import GCM
from apns import APNs, Frame, Payload

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AndroidPusher:
    gcm = None

    # push
    def push(self, push_token, data):
        logger.info('Push to token: ' + str(push_token) + ' ' + str(data))
        try:
            # token is test?
            import re
            m = re.search('TEST_PUSH_TOKEN', push_token)
            if m:
                logger.info('That was a test push')
                return True

            # token is real

            # create GCM
            if not AndroidPusher.gcm:
                from H2O.settings import GCM_API_KEY
                AndroidPusher.gcm = GCM(GCM_API_KEY)

            # sending
            res = AndroidPusher.gcm.json_request(
                registration_ids=[push_token],
                data={
                    'notification': data,
                },
                delay_while_idle=True,
                time_to_live=3600,
            )
            logger.info(res)

            # old token
            old_token = None
            try:
                errors = res['errors']
                old_token = errors['NotRegistered'][0]
            except:
                pass

            # remove it
            if old_token:
                from models.user_device import UserDevice
                UserDevice.delete_push_token(None, old_token)

        except Exception, e:
            raise PusherException(e)

        return True


class ApplePusher:
    apns = None

    # push
    def push(self, push_token, data):
        logger.info('Push to token: ' + str(push_token) + ' ' + str(data))

        try:
            import re
            m = re.search('TEST_PUSH_TOKEN', push_token)
            if m:
                logger.info('That was a test push')
                return True

            if not ApplePusher.apns:
                from H2O.settings import BASE_DIR
                cert_file = BASE_DIR + '/resources/certs/push_H2O_Dev.pem'
                key_file = BASE_DIR + '/resources/certs/push_H2O_Dev.key'
                ApplePusher.apns = APNs(use_sandbox=True, cert_file=cert_file, key_file=key_file)

            payload = Payload(alert=data, sound="default", badge=1)
            ApplePusher.apns.gateway_server.send_notification(push_token, payload)

        except Exception, e:
            raise PusherException(e)

        return True


class Pusher:
    pushers = {
        'ios': None,
        'android': None,
    }

    @staticmethod
    def get_pusher(device_type):
        if device_type == 'ios':
            if not Pusher.pushers['ios']:
                Pusher.pushers['ios'] = ApplePusher()
            return Pusher.pushers['ios']

        elif device_type == 'android':
            if not Pusher.pushers['android']:
                Pusher.pushers['android'] = AndroidPusher()
            return Pusher.pushers['android']

class PusherException(Exception):
    pass
