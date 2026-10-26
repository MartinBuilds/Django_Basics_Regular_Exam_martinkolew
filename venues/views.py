from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VenueForm
from .models import Venue


def venue_list(request):
    venues = Venue.objects.annotate(events_count=Count('events'))
    context = {
        'venues': venues,
    }
    return render(request, 'venues/venue_list.html', context)


def venue_details(request, pk):
    venue = get_object_or_404(
        Venue.objects.annotate(events_count=Count('events')),
        pk=pk,
    )
    events = venue.events.all()
    context = {
        'venue': venue,
        'events': events,
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


def venue_edit(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    form = VenueForm(request.POST or None, instance=venue)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(venue.get_absolute_url())

    context = {
        'form': form,
        'venue': venue,
    }
    return render(request, 'venues/venue_create.html', context)


def venue_delete(request, pk):
    venue = Venue.objects.filter(pk=pk).first()

    if request.method == 'POST':
        if venue is not None:
            venue.delete()
        return redirect('venue-list')

    if venue is None:
        return redirect('venue-list')

    return redirect(venue.get_absolute_url())
