from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Venue(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
    )
    description = models.TextField(max_length=1000, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('venue-details', kwargs={'pk': self.pk})