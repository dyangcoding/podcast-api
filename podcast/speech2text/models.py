from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..users import ClubUser

class Transcript(models.Model):
    file_name = models.CharField(_('file name'), max_length=254, unique=True)
    counter = models.IntegerField(_('transcribe counter'))