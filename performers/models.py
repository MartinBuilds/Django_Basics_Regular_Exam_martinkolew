from django.db import models
from django.urls import reverse


class Performer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('performer-details', kwargs={'pk': self.pk})