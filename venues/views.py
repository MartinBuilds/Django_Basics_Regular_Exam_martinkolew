from django.shortcuts import render

from .models import Venue


def venue_list(request):
    venues = Venue.objects.all()
    context = {
        'venues': venues,
    }
    return render(request, 'venues/venue_list.html', context)