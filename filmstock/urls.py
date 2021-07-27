from django.contrib import admin
from django.urls import re_path, path, include
from web import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap, FilmSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'film': FilmSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.home, name='home'),
    path('film/', views.film, name='film'),
    path('film/track/<int:id>', views.trackFilm, name='track-film'),
    path('film/untrack/<int:id>', views.untrackFilm, name='untrack-film'),
    path('film/<str:brand>/<str:name>/<str:format>/<int:exposures>/', views.filmStock),
    path('film/<str:brand>/<str:name>/<str:format>/', views.filmStock),
    path('film/<str:brand>/<str:name>/', views.filmStock),
    re_path(r'^cameras$', views.cameras, name='cameras'),
    path('help/', views.help, name='help'),
    re_path(r'^cameras/save/new$', views.saveSearch, name='save-search'),
    path('users/unsubscribe', views.unsubscribeHunter, name='unsubscribe-all'),
    path('users/', include('hunters.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('cameras/save/delete/<int:id>', views.deleteSearch, name='delete-search'),
    path('cameras/save/unsubscribe/<int:id>', views.unsubscribeSearch, name='unsubscribe-search'),
    path('cameras/save/subscribe/<int:id>', views.subscribeSearch, name='subscribe-search'),
    path('privacy/', views.privacyPolicy, name='privacy'),
    path('terms-of-use/', views.termsOfUse, name='terms-of-use'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap')
]
