from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Camera, CameraFilter, Film, FilmFilter, followedFilm
from .forms import savedSearchForm
from django.urls import reverse_lazy
from django.http import Http404
from django.utils import timezone
from django import forms
import pytz
from django.db.models import Min, Max
from django.core.paginator import Paginator

def film(request):

    film = Film.objects.all().annotate(price=Min('stock__price')).annotate(lastSeen=Max('stock__lastSeen')).order_by('price')
    f = FilmFilter(request.GET, queryset=film)

    paginator = Paginator(f.qs, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'film.html', {
        'films' : f,
        'page_obj' : page_obj,
        'total' : Film.objects.count(),
    })

def filmStock(request, id):

    film = Film.objects.annotate(price=Min('stock__price')).get(id__exact=id)

    films = []

    for x in film.stock.filter(lastSeen__gt=(timezone.now() - timezone.timedelta(minutes=60))).order_by('price'):

            films.append({
                'url' : x.url,
                'source' : x.source.name,
                'price' : x.price,
                'per_unit' : x.price/x.quantity,
                'quantity' : x.quantity,
                'shipping' : x.source.shipping,
            })

    return render(request, 'film-stock.html', {
        'film' : film,
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

    except Film.DoesNotExist:
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

        if not request.user.is_subscribed:
            form.fields['is_subscribed'].widget = forms.HiddenInput()

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
