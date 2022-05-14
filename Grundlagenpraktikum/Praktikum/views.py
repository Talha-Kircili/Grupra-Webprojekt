from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from datetime import datetime as date
from .forms import HilfegesuchForm
from django.conf import settings
from json import loads, dumps
from .models import *


# gibt als Tupel die Priorität der Hilfesuche und Warteplatz des Praktikanten zurück
def get_help(user):
    help = Hilfesuche.objects.filter(user = user)
    if not help:
        return (0, Hilfesuche.objects.all().count()+1)
    place=1
    for i in Hilfesuche.objects.order_by('-priority', 'creation_time'):
        if i == help[0]:
            return (help[0].priority, place)
        place += 1

@login_required(redirect_field_name=None)
def index(request):
    ''' Admin weiterleiten '''
    referer = request.META.get('HTTP_REFERER')
    if referer:
        if 'login' in referer and request.user.is_staff:
            return redirect('admin/')

    if request.method == 'GET':
        ''' Hilfesuche löschen '''
        if request.GET.get('stop'):
            Hilfesuche.objects.filter(user = request.user).delete()
            return HttpResponse(1)
        # Hilfesuche Status abfragen
        elif request.GET.get('refresh'):
            return HttpResponse(dumps(get_help(request.user)))

    else:
        body_post = loads(request.body)
        fortschritt = Fortschritt.objects.filter(user = request.user)
        if "priority" in body_post:
            priority = body_post["priority"]
            if priority:
                hilfe = Hilfesuche.objects.filter(user = request.user)
                if hilfe:
                    ''' Hilfesuche aktualisieren '''
                    hilfe.update(priority = priority)
                else:
                    ''' Hilfesuche erstellen '''
                    Hilfesuche.objects.create(user = request.user, priority = priority)
        elif "finished" in body_post:
            ''' Fortschritt hinzufügen '''
            fortschritt = fortschritt[0]
            temp = body_post["finished"]
            if temp not in fortschritt.progress:
                fortschritt.progress.append(temp)
                fortschritt.save()
        elif "unfinished" in body_post:
            ''' Fortschritt entfernen '''
            fortschritt = fortschritt[0]
            temp = body_post["unfinished"]
            if temp in fortschritt.progress:
                fortschritt.progress.remove(temp)
                fortschritt.save()

    ''' Initial Werte '''
    versuch = Versuch.objects.filter(status=1)
    context = {
        'time': None,
        'help': dumps((0,0)),
        'Hilfesuche': HilfegesuchForm(),
        'versuch': "Kein Versuch aktiv",
        'document': "javascript:void(0)"
    }
    progress = []
    time = None
    ''' Versuch aktiv? '''
    if versuch:
        ''' context data '''
        temp = Wochentag.objects.filter(day = date.today().strftime("%A"))
        if temp:
            time = temp[0].time
        aufgaben = Aufgabe.objects.filter(versuch=versuch[0])
        aufgaben = list(aufgaben.values('description'))
        temp = Fortschritt.objects.filter(user = request.user)
        if temp:
            progress = temp[0].progress
        context = {
            'time': time,
            'aufgaben': aufgaben,
            'progress': list(progress), 
            'versuch': versuch[0].title,
            'Hilfesuche': HilfegesuchForm(),
            'help': dumps(get_help(request.user)),
            'document': '/media/'+str(versuch[0].document)
        }
    return render(request, 'index.html', context)

def logout_view(request):
    logout(request)
    return redirect('/login/')

def faq(request):
    return render(request, 'faq.html')
