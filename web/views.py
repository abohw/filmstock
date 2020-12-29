from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from .models import Camera, CameraFilter


def home(request):

    t = get_template('index.html')

    html = t.render({'cameras': None}, request)

    return HttpResponse(html)

def cameraFilterView(request):

    f = CameraFilter(request.GET, queryset=Camera.objects.all())
    return render(request, 'cameras.html', {'cameras': f})


def cameras(request):

    t = get_template('cameras.html')

    html = t.render(
        {
            'cameras' : Camera.objects.all().order_by('-createdAt').order_by('-price')
        },
        request)

    return HttpResponse(html)


def film(request):

    return cameras(request)
