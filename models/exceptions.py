class InviteCodeAlreadyTakenException(Exception):
    def __str__(self):
        return 'INVITE_CODE_IS_ALREADY_TAKEN'
    pass

class InviteCodeDoesNotExistException(Exception):
    def __str__(self):
        return 'INVITE_CODE_DOES_NOT_EXIST'
    pass

class FacebookException(Exception):
    def __str__(self):
        return 'FACEBOOK_EXCEPTION'
    pass

class NotImplementedException(Exception):
    def __str__(self):
        return 'NOT_IMPLEMENTED'
    pass
