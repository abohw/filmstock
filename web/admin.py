from django.contrib import admin
from django.utils.html import mark_safe
from .models import Camera, savedSearch, emailTask, Film, filmStock, Source, followedFilm


class FilmAdmin(admin.ModelAdmin):
    readonly_fields = ["filmUrl"]

    def filmUrl(self, obj):
        return mark_safe('<a href="%s" target="_blank" />%s</a>' % (obj.url, obj.url))

admin.site.register(Film, FilmAdmin)
admin.site.register(Camera)
admin.site.register(savedSearch)
admin.site.register(emailTask)
admin.site.register(filmStock)
admin.site.register(Source)
admin.site.register(followedFilm)
