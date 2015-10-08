class BadRequestException(Exception):
    def __init__(self, e):
        self.e = e
    def __str__(self):
        return 'BAD_REQUEST'

class AccessTokenDoesNotExistException(Exception):
    def __str__(self):
        return 'ACCESS_TOKEN_DOES_NOT_EXIST'

class RefreshTokenDoesNotExistException(Exception):
    def __str__(self):
        return 'REFRESH_TOKEN_DOES_NOT_EXIST'

class UserIsNotFoundException(Exception):
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

class InvalidEmailException(Exception):
    def __str__(self):
        return 'INVALID_EMAIL'

class EmailIsAlreadyUsedException(Exception):
    def __str__(self):
        return 'EMAIL_IS_ALREADY_USED'

class YouHaveInvitedThisEmailException(Exception):
    def __str__(self):
        return 'YOU_HAVE_INVITED_THIS_EMAIL'

class UserIsAlreadyFollowedException(Exception):
    def __str__(self):
        return 'USER_IS_ALREADY_FOLLOWED'

class UserIsNotFoundException(Exception):
    def __str__(self):
        return 'USER_IS_NOT_FOUND'

class ResourceIsNotFoundException(Exception):
    def __str__(self):
        return 'RESOURCE_IS_NOT_FOUND'

class ForbiddenException(Exception):
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

class GoneException(Exception):
    def __str__(self):
        return 'GONE'

class LockedException(Exception):
    def __str__(self):
        return 'LOCKED'

class UnavailableException(Exception):
    def __str__(self):
        return 'UNAVAILABLE'
