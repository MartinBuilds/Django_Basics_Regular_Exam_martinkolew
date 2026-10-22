from django.shortcuts import get_object_or_404, redirect, render

from performers.models import Performer
from venues.models import Venue

from .forms import EventForm
from .models import Event


def home(request):
    latest_events = Event.objects.all()[:5]
    context = {
        'latest_events': latest_events,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def event_list(request):
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'events/event_list.html', context)


def event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event,
    }
    return render(request, 'events/event_details.html', context)


def event_create(request):
    form = EventForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            event = form.save()
            return redirect(event.get_absolute_url())

    context = {
        'form': form,
        'has_venues': Venue.objects.exists(),
        'has_performers': Performer.objects.exists(),
    }
    return render(request, 'events/event_form.html', context)


def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=event)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(event.get_absolute_url())

    context = {
        'form': form,
        'event': event,
        'has_venues': Venue.objects.exists(),
        'has_performers': Performer.objects.exists(),
    }
    return render(request, 'events/event_form.html', context)