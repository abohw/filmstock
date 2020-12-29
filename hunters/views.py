from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm


def newUser(request):

    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(reverse_lazy('login'))

    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': f})
