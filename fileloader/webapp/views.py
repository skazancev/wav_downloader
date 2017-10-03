# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from webapp.forms import WAVForm, WAVChangeForm
from webapp.models import WAVFile


def wav_add_view(request):
    form = WAVForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('webapp:list'))
    return render(request, 'webapp/wav/add.html', {'form': form})


def wav_list_view(request):
    return render(request, 'webapp/wav/list.html', {'objects': WAVFile.objects.all()})


def wav_change_view(request, pk):
    obj = get_object_or_404(WAVFile, pk=pk)
    form = WAVChangeForm(instance=obj, data=request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('webapp:list'))
    return render(request, 'webapp/wav/change.html', {'form': form})


def wav_delete_view(request, pk):
    if request.method == 'POST':
        obj = get_object_or_404(WAVFile, pk=pk)
        obj.delete()
        return redirect(reverse('webapp:list'))

    raise Http404()
