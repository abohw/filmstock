from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from .models import Camera


def home(request):

    t = get_template('index.html')

    html = t.render({
        'cameras' : Camera.objects.all().order_by('-createdAt').order_by('-price'),
        })

    return HttpResponse(html)
