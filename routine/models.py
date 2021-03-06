from urllib.parse import urlparse, parse_qs
from django.db import models
from authentication.models import TrainingGroup


class EffortLevel(models.TextChoices):
    LOW = 'LW', 'Bajo'
    MEDIUM = 'MD', 'Medio'
    HIGH = 'HI', 'Alto'


class Routine(models.Model):
    training_group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE, blank=True, null=True,
                                       verbose_name='training group')
    name = models.CharField('name', max_length=128, null=False, blank=False)
    description = models.TextField('description', blank=True, null=True)
    estimated_duration = models.DurationField('estimated duration', null=True, blank=True)
    effort_level = models.CharField(blank=True, null=True, max_length=2, choices=EffortLevel.choices,
                                    default=EffortLevel.LOW)
    order = models.IntegerField('order', null=True, blank=True)

    class Meta:
        verbose_name = 'routine'

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def instructions_qty(self):
        return RoutineInstruction.objects.filter(routine=self).count()

    @property
    def effort_level_desc(self):
        return EffortLevel(self.effort_level).label


class RoutineInstruction(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, null=True, blank=True, verbose_name='routine')
    title = models.CharField('name', max_length=128, null=False, blank=False)
    description = models.TextField('description', blank=True, null=True)
    video_link = models.CharField('link', max_length=128, null=True, blank=True)
    order = models.IntegerField('order', null=True, blank=True)

    class Meta:
        verbose_name = 'routine instruction'

    def __str__(self):
        return '{}'.format(self.title)

    @property
    def get_yt_video_id(self):
        """
            Returns Video_ID extracting from the given url of Youtube

            Examples of URLs:
              Valid:
                'http://youtu.be/_lOT2p_FCvA',
                'www.youtube.com/watch?v=_lOT2p_FCvA&feature=feedu',
                'http://www.youtube.com/embed/_lOT2p_FCvA',
                'http://www.youtube.com/v/_lOT2p_FCvA?version=3&amp;hl=en_US',
                'https://www.youtube.com/watch?v=rTHlyTphWP0&index=6&list=PLjeDyYvG6-40qawYNR4juzvSOg-ezZ2a6',
                'youtube.com/watch?v=_lOT2p_FCvA',

              Invalid:
                'youtu.be/watch?v=_lOT2p_FCvA',
        """
        url = self.video_link
        if url.startswith(('youtu', 'www')):
            url = 'http://{}'.format(url)

        query = urlparse(url)

        if 'youtube' in query.hostname:
            if query.path == '/watch':
                return parse_qs(query.query)['v'][0]
            elif query.path.startswith(('/embed/', '/v/')):
                return query.path.split('/')[2]
        elif 'youtu.be' in query.hostname:
            return query.path[1:]
        else:
            raise ValueError
