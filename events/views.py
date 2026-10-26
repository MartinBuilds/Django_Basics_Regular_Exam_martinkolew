from django.shortcuts import get_object_or_404, redirect, render

from performers.models import Performer
from venues.models import Venue

from .forms import EventFilterForm, EventForm
from .models import Event


SORT_OPTIONS = {
    'date_asc': 'start_datetime',
    'date_desc': '-start_datetime',
    'title': 'title',
    'title_desc': '-title',
}


def home(request):
    latest_events = Event.objects.all()[:5]
    context = {
        'latest_events': latest_events,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def page_not_found(request, exception):
    return render(request, '404.html', status=404)



def event_list(request):
    events = Event.objects.all()
    filter_form = EventFilterForm(request.GET or None)

    if filter_form.is_valid():
        q = filter_form.cleaned_data.get('q')
        sort = filter_form.cleaned_data.get('sort')

        if q:
            events = events.filter(title__icontains=q)

        if sort in SORT_OPTIONS:
            events = events.order_by(SORT_OPTIONS[sort])

    context = {
        'events': events,
        'filter_form': filter_form,
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


def event_delete(request, pk):
    event = Event.objects.filter(pk=pk).first()

    if request.method == 'POST':
        if event is not None:
            event.delete()
        return redirect('event-list')

    if event is None:
        return redirect('event-list')

    return redirect(event.get_absolute_url())
