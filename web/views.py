from django.shortcuts import render
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import Camera, CameraFilter
from .forms import savedSearchForm
from django.urls import reverse_lazy
from django.http import Http404


def cameras(request):

    f = CameraFilter(request.GET, queryset=Camera.objects.all())

    terms = request.GET.get('name')
    if terms is None: terms = ''

    price_min = request.GET.get('price_min')
    if price_min is None: price_min = ''

    price_max = request.GET.get('price_max')
    if price_max is None: price_max = ''

    sort = request.GET.get('sort')
    if sort is None: sort = ''

    reddit_url = 'https://www.reddit.com/r/photomarket/search?q=%s flair:\"selling\"&restrict_sr=1&t=week' % (terms)
    ebay_url = 'https://www.ebay.com/sch/15230/i.html?_from=R40&_nkw=%s&LH_PrefLoc=1&rt=nc&_udlo=%s&_udhi=%s' % (terms, price_min, price_max)

    return render(request, 'cameras.html', {
        'cameras': f,
        'total': Camera.objects.all().count(),
        'reddit_url' : reddit_url,
        'ebay_url' : ebay_url,
        })


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
