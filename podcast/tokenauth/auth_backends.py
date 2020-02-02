from django.contrib.auth import get_user_model

from . import settings as ta_settings
from .models import AuthToken
from .models import generate_token


class EmailTokenBackend:
    def get_user(self, user_id):
        """Get a user by their primary key."""
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, token=None):
        """Authenticate a user given a signed token."""
        AuthToken.delete_stale()

        t = AuthToken.objects.filter(token=token).first()
        if not t:
            return

        if ta_settings.SINGLE_USE_LINK:
            t.delete()

        User = get_user_model()
        user, created = User.objects.get_or_create(email=t.email)

        if not ta_settings.CAN_LOG_IN(request, user):
            return

        return user
