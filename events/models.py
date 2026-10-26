from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from performers.models import Performer
from venues.models import Venue


class Event(models.Model):
    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(3)],
    )
    description = models.TextField(max_length=1000)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    ticket_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000),
        ],
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name='events',
    )
    performers = models.ManyToManyField(
        Performer,
        related_name='events',
    )

    class Meta:
        ordering = ('-start_datetime',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event-details', kwargs={'pk': self.pk})

    @property
    def status(self):
        now = timezone.now()
        if now < self.start_datetime:
            return 'upcoming'
        if now <= self.end_datetime:
            return 'ongoing'
        return 'past'

    @property
    def status_label(self):
        labels = {
            'upcoming': 'Предстоящо',
            'ongoing': 'Започнало',
            'past': 'Минало',
        }
        return labels[self.status]

    def clean(self):

        from django.core.exceptions import ValidationError

        super().clean()
        if self.start_datetime and self.end_datetime:
            if self.end_datetime < self.start_datetime:
                raise ValidationError(
                    'Крайната дата трябва да е след или равна на началната.'
                )