from django.db import models
from django.urls import reverse


class Venue(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('venue-details', kwargs={'pk': self.pk})