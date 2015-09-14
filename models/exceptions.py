class BadRequest(Exception):
    def __init__(self, e):
        self.e = e
    def __str__(self):
        return 'BAD_REQUEST'

class AccessTokenDoesNotExist(Exception):
    def __str__(self):
        return 'ACCESS_TOKEN_DOES_NOT_EXIST'

class ResfreshTokenDoesNotExist(Exception):
    def __str__(self):
        return 'REFRESH_TOKEN_DOES_NOT_EXIST'

class UserIsNotFound(Exception):
    def __str__(self):
        return 'USER_IS_NOT_FOUND'

class InviteCodeAlreadyTakenException(Exception):
    def __str__(self):
        return 'INVITE_CODE_IS_ALREADY_TAKEN'

class InviteCodeDoesNotExistException(Exception):
    def __str__(self):
        return 'INVITE_CODE_DOES_NOT_EXIST'

class FacebookException(Exception):
    def __str__(self):
        return 'FACEBOOK_EXCEPTION'

class NotImplementedException(Exception):
    def __str__(self):
        return 'NOT_IMPLEMENTED'

class InvalidEmail(Exception):
    def __str__(self):
        return 'INVALID_EMAIL'

class EmailIsAlreadyUsed(Exception):
    def __str__(self):
        return 'EMAIL_IS_ALREADY_USED'

class UserIsAlreadyFollowed(Exception):
    def __str__(self):
        return 'USER_IS_ALREADY_FOLLOWED'

class UserIsNotFound(Exception):
    def __str__(self):
        return 'USER_IS_NOT_FOUND'

class ResourceIsNotFound(Exception):
    def __str__(self):
        return 'RESOURCE_IS_NOT_FOUND'

class Forbidden(Exception):
    def __str__(self):
        return 'FORBIDDEN'

class ConflictException(Exception):
    def __str__(self):
        return 'CONFLICT'

class NotAcceptableException(Exception):
    def __str__(self):
        return 'NOT_ACCEPTABLE'

class NotEnoughMoneyException(Exception):
    def __str__(self):
        return 'NOT_ENOUGH_MONEY'
