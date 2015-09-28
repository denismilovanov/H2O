from gcm import GCM
from apns import APNs, Frame, Payload

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AndroidPusher:
    gcm = None

    # push
    def push(self, user_id, push_token, data):
        logger.info('Push to token: ' + str(push_token) + ' ' + str(user_id) + ' ' + str(data))
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

            # only for apple
            del data['push_header']

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
                UserDevice.delete_push_token(user_id, old_token)

        except Exception, e:
            raise PusherException(e)

        return True


class ApplePusher:
    @staticmethod
    def get_apns():
        from H2O.settings import APNS_USE_SANDBOX, APNS_CERT_FILE, APNS_KEY_FILE
        apns = APNs(use_sandbox=APNS_USE_SANDBOX, cert_file=APNS_CERT_FILE, key_file=APNS_KEY_FILE)
        return apns

    # push
    def push(self, user_id, push_token, data):
        logger.info('Push to token: ' + str(push_token) + ' ' + str(user_id) + ' ' + str(data))

        try:
            import re
            m = re.search('TEST_PUSH_TOKEN', push_token)
            if m:
                logger.info('That was a test push')
                return True

            apns = ApplePusher.get_apns()

            # dummy alert, all real information in 'data'
            alert = {
                "title": "H2O",
                "body": data['push_header'],
            }
            del data['push_header']

            # payload
            from models.notification import Notification
            badge = Notification.get_unread_notifications_count(user_id)
            logger.info('badge = ' + str(badge))
            payload = Payload(alert=alert, sound="default", badge=badge, custom=data)

            # send
            apns.gateway_server.send_notification(push_token, payload)

            # close connection
            del apns

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
