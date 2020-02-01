from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import ClubUser
from .forms import ClubUserChangeForm, ClubUserCreationForm

class ClubUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'display_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    form = ClubUserChangeForm
    add_form = ClubUserCreationForm
    list_display = ('email', 'display_name', 'is_staff')
    search_fields = ('email', 'display_name')
    ordering = ('email',)

admin.site.register(ClubUser, ClubUserAdmin)