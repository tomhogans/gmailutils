import requests
import lxml.etree
import logging


class InvalidAccountException(Exception): pass
class VerificationException(Exception): pass
class UnknownResponseException(Exception): pass


class GmailSession:
    GOOGLE_LOGIN_URL = 'https://accounts.google.com/ServiceLogin'
    GOOGLE_RECOVERY_URL = 'https://accounts.google.com/AccountRecoveryOptionsPrompt'
    GOOGLE_VERIFICATION_URL = 'https://accounts.google.com/LoginVerification'

    def __init__(self):
        self.req = requests.Session()
        # TODO: Set browser string

    def login(self, email, password, recovery_email=None):
        """ Logs in to a Google Account.  Email and password are normally
        sufficient, but if VerificationException is raised, the account
        requires the recovery_email parameter in order to be unlocked. """
        resp = self.req.get(self.GOOGLE_LOGIN_URL)
        html = lxml.etree.HTML(resp.content)
        fields = {i.get('name'): i.get('value') for i in html.xpath('//input')}
        fields['bgresponse'] = ''
        fields['Email'] = email
        fields['Passwd'] = password
        resp = self.req.post(self.GOOGLE_LOGIN_URL, fields)
        if 'username or password you entered is incorrect' in resp.content:
            raise InvalidAccountException(email)

        if 'signing in from an unusual location' in resp.content:
            html = lxml.etree.HTML(resp.content)
            fields = {i.get('name'): i.get('value') 
                    for i in html.xpath('//input')}
            fields['bgresponse'] = ''
            fields['challengetype'] = 'RecoveryEmailChallenge'
            if not recovery_email:
                raise VerificationException(email)
            logging.debug("Answering account verification with recovery email")
            fields['emailAnswer'] = recovery_email
            resp = self.req.post(self.GOOGLE_VERIFICATION_URL, fields)

        if 'email address below is no longer safe' in resp.content:
            html = lxml.etree.HTML(resp.content)
            fields = {i.get('name'): i.get('value') 
                    for i in html.xpath('//input')}
            del fields['change']
            logging.debug('Google asking for recovery email update, declining')
            resp = self.req.post(self.GOOGLE_LOGIN_URL, fields)

        if 'AccountRecoveryOptionsPrompt' in resp.content:
            html = lxml.etree.HTML(resp.content)
            fields = {i.get('name'): i.get('value') 
                    for i in html.xpath('//input')}
            logging.debug('Google prompting for account recovery options')
            resp = self.req.post(self.GOOGLE_RECOVERY_URL, fields)

        if not 'Account Overview' in resp.content:
            #open('resp.html', 'w').write(resp.content)
            raise UnknownResponseException(email)

        return True

