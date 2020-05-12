from django.db import models


class Routine(models.Model):
    name = models.CharField('name', max_length=128, null=False, blank=False)
    description = models.TextField('description', blank=True, null=True)

    class Meta:
        verbose_name = 'routine'

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def instructions_qty(self):
        return RoutineInstruction.objects.filter(routine=self).count()


class RoutineInstruction(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, null=False, blank=False, verbose_name='routine')
    title = models.CharField('name', max_length=128, null=False, blank=False)
    description = models.TextField('description', blank=True, null=True)
    video_link = models.CharField('link', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'routine instruction'

    def __str__(self):
        return '{}'.format(self.title)
