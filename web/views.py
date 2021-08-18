from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Camera, CameraFilter, Film, FilmFilter, followedFilm, filmStock
from .forms import savedSearchForm
from django.urls import reverse_lazy
from django.http import Http404
from django.utils import timezone
from django import forms
import pytz
from django.db.models import Min, Max
from django.core.paginator import Paginator


def home(request):

    cameras = Camera.objects.filter(image__isnull=False).exclude(name__icontains='lens')
    latest = cameras.order_by('-id')[:6]
    cheapest = cameras.filter(price__lt=100).order_by('?')[:6]

    return render(request, 'home.html', { 'latest': latest, 'cheapest': cheapest, })


def redirectCamera(request, id):

    try:
        camera = Camera.objects.get(id__exact=id)
        return HttpResponseRedirect(camera.url)

    except Camera.DoesNotExist:
        return HttpResponseRedirect(reverse_lazy('cameras') + '?redirect=true')


def redirectFilmStock(request, id):

    try:
        stock = filmStock.objects.get(id__exact=id)
        return HttpResponseRedirect(stock.url)

    except filmStock.DoesNotExist:

        return HttpResponseRedirect(reverse_lazy('film') + '?redirect=true')


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


def privacyPolicy(request):
    return render(request, 'privacy.html', { })


def termsOfUse(request):
    return render(request, 'terms-of-use.html', { })


def viewFilmStock(request, id, brand='', name='', format='35mm', exposures=36):

    try:
        film = Film.objects.get(id__exact=id)
        return filmStockLookup(request, film.id)

    except Film.DoesNotExist:
        raise Http404


def filmStockLookup(request, id):

    film = Film.objects.annotate(price=Min('stock__price')).get(id__exact=id)

    similar = Film.objects.exclude(id__exact=film.id).filter(experimental=False, format=film.format, type=film.type)

    if similar.count() > 3:
        similar = similar.filter(iso__range=[(film.iso - 120), (film.iso + 240)])

    similar = similar.order_by('?')[:3]

    films = []

    for x in film.stock.filter(lastSeen__gt=(timezone.now() - timezone.timedelta(minutes=60))).order_by('price'):

            films.append({
                'url' : x.url,
                'source' : x.source.name,
                'price' : x.price,
                'per_unit' : x.price/x.quantity,
                'quantity' : x.quantity,
                'shipping' : x.source.shipping,
                'id' : x.id,
            })

    return render(request, 'film-stock.html', {
        'film' : film,
        'stocks' : films,
        'similar' : similar,
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

        try:
            followedFilm.objects.get(hunter=request.user, film=film)

        except followedFilm.DoesNotExist:

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

