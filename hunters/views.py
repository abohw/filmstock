from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core import mail
from django.template import loader
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import Hunter


def newUser(request):

    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            newUser = f.save()

            html_message = loader.render_to_string(
                'emails/account_activation_email.html',
                {
                    'user': newUser,
                    'domain': 'filmstock.app',
                    'uid': urlsafe_base64_encode(force_bytes(newUser.pk)),
                    'token': account_activation_token.make_token(newUser),
                }
            )

            mail.send_mail(
                'Please confirm your registration',
                'Filmstock',
                'Filmstock <alerts@mail.filmstock.app>',
                [newUser.email],
                fail_silently=True,
                html_message=html_message,
            )

            newUser = authenticate(email=f.cleaned_data['email'],
                        password=f.cleaned_data['password1'],)
            login(request, newUser)
            return HttpResponseRedirect(reverse_lazy('cameras'))

    else:
        f = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': f})


@login_required
def userSettings(request):

    return render(request, 'settings.html', {
        'searches' : request.user.searches.all(),
        'follows' : request.user.follows.all(),
    })


@login_required
def activateUser(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Hunter.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Hunter.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_subscribed = True
        user.save()
        return HttpResponseRedirect(reverse_lazy('cameras'))
    else:
        return HttpResponseRedirect(reverse_lazy('home'))
