from django.shortcuts import get_object_or_404, redirect, render

from .forms import PerformerForm
from .models import Performer


def performer_list(request):
    performers = Performer.objects.all()
    context = {
        'performers': performers,
    }
    return render(request, 'performers/performer_list.html', context)


def performer_details(request, pk):
    performer = get_object_or_404(Performer, pk=pk)
    context = {
        'performer': performer,
    }
    return render(request, 'performers/performer_details.html', context)


def performer_create(request):
    form = PerformerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            performer = form.save()
            return redirect(performer.get_absolute_url())

    context = {
        'form': form,
    }
    return render(request, 'performers/performer_form.html', context)


def performer_edit(request, pk):
    performer = get_object_or_404(Performer, pk=pk)
    form = PerformerForm(request.POST or None, instance=performer)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(performer.get_absolute_url())

    context = {
        'form': form,
        'performer': performer,
    }
    return render(request, 'performers/performer_form.html', context)