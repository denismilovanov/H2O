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

class InvalidEmail(Exception):
    def __str__(self):
        return 'INVALID_EMAIL'
    pass

class EmailIsAlreadyUsed(Exception):
    def __str__(self):
        return 'EMAIL_IS_ALREADY_USED'
    pass

class UserIsAlreadyFollowed(Exception):
    def __str__(self):
        return 'USER_IS_ALREADY_FOLLOWED'
    pass

class UserIsNotFound(Exception):
    def __str__(self):
        return 'USER_IS_NOT_FOUND'
    pass
