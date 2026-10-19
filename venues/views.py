from django.shortcuts import get_object_or_404, redirect, render

from .forms import VenueForm
from .models import Venue


def venue_list(request):
    venues = Venue.objects.all()
    context = {
        'venues': venues,
    }
    return render(request, 'venues/venue_list.html', context)


def venue_details(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    context = {
        'venue': venue,
    }
    return render(request, 'venues/venue_details.html', context)


def venue_create(request):
    form = VenueForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            venue = form.save()
            return redirect(venue.get_absolute_url())

    context = {
        'form': form,
    }
    return render(request, 'venues/venue_create.html', context)