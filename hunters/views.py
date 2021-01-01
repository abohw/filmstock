from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def newUser(request):

    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            newUser = f.save()
            newUser = authenticate(email=f.cleaned_data['email'],
                        password=f.cleaned_data['password1'],)
            login(request, newUser)
            return HttpResponseRedirect(reverse_lazy('cameras'))

    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': f})


@login_required
def userSettings(request):

    return render(request, 'settings.html', { 'searches' : request.user.searches.all(), })
