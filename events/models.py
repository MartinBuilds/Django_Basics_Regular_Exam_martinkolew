from django.db import models
from django.urls import reverse
from django.utils import timezone

from performers.models import Performer
from venues.models import Venue


class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
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
    def is_upcoming(self):
        return self.start_datetime >= timezone.now()