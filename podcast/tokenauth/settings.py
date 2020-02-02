from django.conf import settings

# The rate at which people will be able to request logins.
RATELIMIT_RATE = getattr(settings, "TOKENAUTH_RATELIMIT_RATE", "3/h")

# A function that gets passed a user's email address and returns a normalized/cleaned
# up version.
NORMALIZE_EMAIL = getattr(settings, "TOKENAUTH_NORMALIZE_EMAIL", lambda e: e)

# A function that gets passed a user object and returns True if that user should
# be allowed to log in.
CAN_LOG_IN = getattr(settings, "TOKENAUTH_CAN_LOG_IN", lambda request, user: True)

# A function that gets passed a user object and returns True if that user should
# be allowed to log in.
CAN_LOG_IN = getattr(settings, "TOKENAUTH_CAN_LOG_IN", lambda request, user: True)

# How long a token should be valid for, in seconds.
TOKEN_DURATION = getattr(settings, "TOKENAUTH_TOKEN_DURATION", 30 * 60)

# How long the token should be, in characters.
TOKEN_LENGTH = getattr(settings, "TOKENAUTH_TOKEN_LENGTH", 8)

DEFAULT_FROM_EMAIL = getattr(
    settings, "TOKENAUTH_DEFAULT_FROM_EMAIL", settings.DEFAULT_FROM_EMAIL
)

SINGLE_USE_LINK = getattr(settings, "TOKENAUTH_SINGLE_USE_LINK", False)