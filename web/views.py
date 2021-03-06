from django.shortcuts import render
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import Camera, CameraFilter, Film, FilmFilter, followedFilm
from .forms import savedSearchForm
from django.urls import reverse_lazy
from django.http import Http404
from django.utils import timezone
import pytz
from django.views.generic.list import ListView
from django.db.models import Min
from django.core.paginator import Paginator

def film(request):

    film = Film.objects.filter(stock__lastSeen__gt=(timezone.now() - timezone.timedelta(minutes=60))).annotate(price=Min('stock__price')).order_by('price')
    f = FilmFilter(request.GET, queryset=film)

    paginator = Paginator(f.qs, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'film.html', {
        'films' : f,
        'page_obj' : page_obj,
        'total' : Film.objects.filter(stock__lastSeen__gt=(timezone.now() - timezone.timedelta(minutes=60))).count()
    })

def filmStock(request, brand='', name='', format=''):

    film = Film.objects.all()

    if brand != '':
        film = film.filter(brand__iexact=brand)

    if name != '':
        film = film.filter(name__iexact=name.replace('+',' '))

    if format != '':
        film = film.filter(format__iexact=format)

    film = film[0]

    films = []

    if film.stock.count() != 0:
        for x in film.stock.filter(lastSeen__gt=(timezone.now() - timezone.timedelta(minutes=60))).order_by('-price'):

                films.append({
                    'url' : x.url,
                    'source' : x.source.name,
                    'price' : x.price,
                    'per_unit' : x.price/x.quantity,
                    'quantity' : x.quantity,
                    'shipping' : x.source.shipping,
                })

    paginator = Paginator(films, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'film-stock.html', {
        'film' : film,
        'page_obj' : page_obj,
        'stocks' : films,
    })


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

    paginator = Paginator(f.qs, 25)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'cameras.html', {
        'cameras': f,
        'page_obj' : page_obj,
        'total': Camera.objects.all().count(),
        'reddit_url' : reddit_url,
        'ebay_url' : ebay_url,
        })


@login_required
def untrackFilm(request, id):

    try:
        followedFilm.objects.get(film__id__exact=id, hunter=request.user).delete()
        return HttpResponseRedirect(reverse_lazy('settings'))

    except:
        raise Http404


@login_required
def trackFilm(request, id):

    try:
        film = Film.objects.get(id__exact=id)

        newTrack = followedFilm(
            hunter=request.user,
            film=film,
            is_subscribed=True,
        )
        newTrack.save()

        return HttpResponseRedirect(reverse_lazy('film'))

    except:
        raise Http404


@login_required
def saveSearch(request):

    if request.method == 'POST':
        form = savedSearchForm(request.POST)

        if form.is_valid():
            newSearch = form.save(commit=False)
            newSearch.hunter = request.user

            if request.user.searches.filter(is_subscribed=True).count() >= 25:
                newSearch.is_subscribed = False

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
def unsubscribeHunter(request):

    searches = request.user.searches.all()
    follows = request.user.follows.all()

    for search in searches:
        search.is_subscribed = False
        search.save()

    for follow in follows:
        follow.delete()

    return HttpResponseRedirect(reverse_lazy('settings'))


@login_required
def subscribeSearch(request, id):

    try:
        search = request.user.searches.get(id__exact=id)

        if request.user.searches.filter(is_subscribed=True).count() < 25:
            search.is_subscribed = True
            search.save()

        return HttpResponseRedirect(reverse_lazy('settings'))

    except:
        raise Http404


def help(request):

    return render(request, 'help-faq.html')
