import datetime
from django.db import models

from authentication.models import User
from routine.models import Routine


class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='user')
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, null=False, blank=False, verbose_name='routine')
    date = models.DateField('date', default=datetime.date.today)
    duration = models.TimeField('duration')

    class Meta:
        verbose_name = 'training'

    def __str__(self):
        return '{} - {}'.format(self.routine.name, self.date)
