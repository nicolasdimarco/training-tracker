from django.contrib.auth.models import AbstractUser
from django.db import models


class TrainingGroup(models.Model):
    name = models.CharField('name', max_length=128, null=False, blank=False)
    description = models.TextField('description', blank=True, null=True)

    class Meta:
        verbose_name = 'routine'

    def __str__(self):
        return '{}'.format(self.name)


class User(AbstractUser):
    training_group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE, null=False, blank=False,
                                       verbose_name='training group')
    email = models.EmailField('email', unique=True)
    is_trainer = models.BooleanField('is trainer', default=False)
