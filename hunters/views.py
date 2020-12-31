from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


def newUser(request):

    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect(reverse_lazy('login'))

    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': f})

@login_required
def userSettings(request):



    return render(request, 'settings.html', { 'searches' : request.user.searches.all(), })
