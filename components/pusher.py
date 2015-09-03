from gcm import GCM

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AndroidPusher:
    gcm = None

    # push
    def push(self, push_token, data):
        import re
        m = re.search('TEST_PUSH_TOKEN', push_token)
        if m:
            logger.info('Test push: ' + str(data))
            return True

        if not AndroidPusher.gcm:
            from H2O.settings import GCM_API_KEY
            AndroidPusher.gcm = GCM(GCM_API_KEY)

        res = AndroidPusher.gcm.json_request(
            registration_ids=[push_token],
            data=data,
            delay_while_idle=True,
            time_to_live=3600,
        )
        print res

        return True


class ApplePusher:
    apns = None

    # push
    def push(self, push_token, data):
        import re
        m = re.search('TEST_PUSH_TOKEN', push_token)
        if m:
            logger.info('Test push: ' + str(data))
            return True

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
