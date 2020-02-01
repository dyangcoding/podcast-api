from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ClubUser

class ClubUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email.
    """

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = ClubUser
        fields = ("email",)

class ClubUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user.
    """

    def __init__(self, *args, **kargs):
        super(UserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = ClubUser
        fields = ('email',)