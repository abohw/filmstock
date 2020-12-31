from django.shortcuts import render
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import Camera, CameraFilter
from .forms import savedSearchForm
from django.urls import reverse_lazy
from django.http import Http404

def home(request):

    t = get_template('index.html')

    html = t.render({'cameras': None}, request)

    return HttpResponse(html)


def cameras(request):

    f = CameraFilter(request.GET, queryset=Camera.objects.all().order_by('-createdAt'))
    return render(request, 'cameras.html', {'cameras': f, 'total': Camera.objects.all().count(), })


@login_required
def saveSearch(request):

    if request.method == 'POST':
        form = savedSearchForm(request.POST)

        if form.is_valid():
            newSearch = form.save(commit=False)
            newSearch.hunter = request.user
            newSearch.save()

            return HttpResponseRedirect(reverse_lazy('cameras') + '?' + newSearch.url)

        else: raise Http404

    else:
        data = {
            'terms' : request.GET.get('name'),
            'source' : request.GET.getlist('source'),
            'price_min' : request.GET.get('price_min'),
            'price_max' : request.GET.get('price_max'),
            'sort' : request.GET.get('sort'),
            'new' : request.GET.get('new'),
            'url' : request.GET.urlencode(),
        }
        form = savedSearchForm(initial=data)

    return render(request, 'save-search.html', {'save': form})


@login_required
def deleteSearch(request, id):

    try:
        request.user.searches.get(id__exact=id).delete()
        return HttpResponseRedirect(reverse_lazy('settings'))

    except:
        raise Http404


@login_required
def unsubscribeSearch(request, id):

    try:
        search = request.user.searches.get(id__exact=id)
        search.is_subscribed = False
        search.save()

        return HttpResponseRedirect(reverse_lazy('settings'))

    except:
        raise Http404


@login_required
def subscribeSearch(request, id):

    try:
        search = request.user.searches.get(id__exact=id)
        search.is_subscribed = True
        search.save()

        return HttpResponseRedirect(reverse_lazy('settings'))

    except:
        raise Http404

def help(request):

    return render(request, 'help-faq.html')
