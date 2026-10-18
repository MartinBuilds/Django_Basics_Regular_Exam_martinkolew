from django.shortcuts import render

from .models import Performer


def performer_list(request):
    performers = Performer.objects.all()
    context = {
        'performers': performers,
    }
    return render(request, 'performers/performer_list.html', context)