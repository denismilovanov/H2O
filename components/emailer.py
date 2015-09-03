import mandrill

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailerException(Exception):
    pass

class MandrillEmailer:
    def send(self, email, content):
        import re
        m = re.search('TEST_EMAIL', email)
        if m:
            logger.info('Test send: ' + str(content))
            return True

        try:
            from H2O.settings import MANDRILL_API_KEY
            mandrill_client = mandrill.Mandrill(MANDRILL_API_KEY)
            message = {
                'auto_html': None,
                'auto_text': None,
                'from_email': 'team@h2o-project.com',
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
        return MandrillEmailer()
