from django.contrib import admin
from .models import Camera, savedSearch, emailTask, Film, filmStock, Source, followedFilm

# Register your models here.

admin.site.register(Camera)
admin.site.register(savedSearch)
admin.site.register(emailTask)
admin.site.register(Film)
admin.site.register(filmStock)
admin.site.register(Source)
admin.site.register(followedFilm)
