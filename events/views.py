from django.shortcuts import render

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