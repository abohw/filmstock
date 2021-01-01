from django.contrib import admin
from django.urls import re_path, path, include
from web import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^cameras$', views.cameras, name='cameras'),
    path('', RedirectView.as_view(url='/cameras?new=True', permanent=False)),
    path('help/', views.help, name='help'),
    re_path(r'^cameras/save/new$', views.saveSearch, name='save-search'),
    path('users/', include('hunters.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('cameras/save/delete/<int:id>', views.deleteSearch, name='delete-search'),
    path('cameras/save/unsubscribe/<int:id>', views.unsubscribeSearch, name='unsubscribe-search'),
    path('cameras/save/subscribe/<int:id>', views.subscribeSearch, name='subscribe-search'),
]
