"""Messages for flash."""
from flask_babel import lazy_gettext as _l  # noqa: WPS347, WPS111

LOGIN_EROOR = _l('Invalid username or password')
LOGIN = _l('Logged in successfully')
LOGOUT = _l('Logged out successfully')

REGISTER = _l('Congratulations, you are now a registered user')

EDIT_PROFILE = _l('Your changes have been saved')

USERNAME_ERROR = _l('Please use a different username')
EMAIL_ERROR = _l('Please use a different email address')

USERNAME_NOT_FOUND = lambda username: _l('User %(username)s not found', username=username)
FOLLOW = lambda username: _l('You are following %(username)s', username=username)
FOLLOW_YOURSELF = _l('You cannot follow yourself')
UNFOLLOW = lambda username: _l('You are not following %(username)s', username=username)
UNFOLLOW_YOURSELF = _l('You cannot unfollow yourself')

RESET_PASSWORD_REQUEST = _l('Check your email for the instructions to reset your password')
RESET_PASSWORD = _l('Your password has been reset')

__all__ = [
    'LOGIN',
    'LOGIN_EROOR',
    'LOGOUT',
    'USERNAME_ERROR',
    'EMAIL_ERROR',
]
