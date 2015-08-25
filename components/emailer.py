import mandrill

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailerException(Exception):
    pass

class DevNullEmailer:
    def send(self, email, content):
        logger.info('Sending to ' + email + ' content: ' + content)
        return True

class MandrillEmailer:
    def send(self, email, content):
        try:
            mandrill_client = mandrill.Mandrill('fDlj32_-RH461igdYhjZQg')
            message = {
                'auto_html': None,
                'auto_text': None,
                'from_email': 'milovanov@octabrain.com',
                'from_name': 'H2O team',
                'html': content,
                'important': False,
                'preserve_recipients': None,
                'return_path_domain': None,
                'signing_domain': None,
                'subject': 'Registration at H2O project',
                'to': [{'email': email}],
            }

            result = mandrill_client.messages.send(message=message, async=False)[0]
            logger.info(result)

            if result['status'] != 'sent':
                raise EmailerException('Email was not sent')

            return True

        except mandrill.Error, e:
            logger.info(e)
            raise EmailerException(e)
        except Exception, e:
            logger.info(e)
            raise EmailerException(e)

class Emailer:
    @staticmethod
    def get():
        return DevNullEmailer()
        return MandrillEmailer()
