from django.contrib import admin
from .models import Camera, savedSearch, emailTask

# Register your models here.

admin.site.register(Camera)
admin.site.register(savedSearch)
admin.site.register(emailTask)
