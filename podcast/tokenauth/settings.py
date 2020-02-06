from django.conf import settings

# The rate at which people will be able to request logins.
RATELIMIT_RATE = getattr(settings, "TOKENAUTH_RATELIMIT_RATE", "3/h")

# A function that gets passed a user's email address and returns a normalized/cleaned
# up version.
NORMALIZE_EMAIL = getattr(settings, "TOKENAUTH_NORMALIZE_EMAIL", lambda e: e)

# A function that gets passed a user object and returns True if that user should
# be allowed to log in.
CAN_LOG_IN = getattr(settings, "TOKENAUTH_CAN_LOG_IN", lambda request, user: True)

DEFAULT_FROM_EMAIL = getattr(
    settings, "TOKENAUTH_DEFAULT_FROM_EMAIL", settings.DEFAULT_FROM_EMAIL
)

SINGLE_USE_LINK = getattr(settings, "TOKENAUTH_SINGLE_USE_LINK", False)

# The Algorithm to encode JWT Token
JWT_ALGORITHM = getattr(settings, "TOKENAUTH_JWT_ALGORITHM", "HS256")

# How long the token is validated after creation
JWT_EXP_DELTA_DAYS = getattr(settings, "TOKENAUTH_JWT_EXP_DELTA_DAYS", 1)