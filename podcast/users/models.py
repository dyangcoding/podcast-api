from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from ..api.models import RssItem

class ClubUserManager(BaseUserManager):

    def _create_user(self, email, is_staff, is_superuser, 
                        **extra_fields):
        """
        Creates and saves a User with the given email.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, **extra_fields):
        return self._create_user(email, False, False, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        return self._create_user(email, True, True, **extra_fields)

class ClubUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email is required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    display_name = models.CharField(_('display name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    newsletter_active = models.BooleanField(_('newsletter submission status'), default=False,
        help_text=_('Designates whether the user submits to the newsletter.'))
    
    playing_list = models.ManyToManyField(RssItem)

    objects = ClubUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_display_name(self):
        "Returns the display name for the user."
        return self.display_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])