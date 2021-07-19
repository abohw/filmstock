from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.core import mail
from django.template import loader
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import CustomUserCreationForm
from .tokens import account_activation_token
from .models import Hunter

import stripe
import os

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


def newUser(request):

    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            newUser = f.save()

            html_message = loader.render_to_string(
                'emails/account_activation_email.html',
                {
                    'user': newUser,
                    'domain': request.build_absolute_uri('/').strip("/"),
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

            newUser = authenticate(email=f.cleaned_data.get('email'),
                        password=f.cleaned_data.get('password1'),)
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
        user.is_verified = True
        user.save()
        return HttpResponseRedirect(reverse_lazy('cameras'))
    else:
        return HttpResponseRedirect(reverse_lazy('home'))

@login_required
def subscribe(request):

    if request.GET.get('return'):
        returnUrl = '%s%s' % (request.build_absolute_uri('/').strip("/"), request.GET.get('return'))

    else:
        returnUrl = request.build_absolute_uri('/').strip("/") + '?'

    successUrl = returnUrl + '&sub=success'
    cancelUrl = '%s%s?sub=cancelled' % (request.build_absolute_uri('/').strip("/"), reverse_lazy('settings'))

    session = stripe.checkout.Session.create(
        success_url=successUrl,
        cancel_url=cancelUrl,
        payment_method_types=['card'],
        mode='subscription',
        line_items=[{
            'price': os.getenv('STRIPE_PRICE_ID'),
            'quantity': 1,
        }],
    )

    request.user.stripe_session_id = session.id
    request.user.save()

    return render(request, 'registration/subscribe.html', {
        'stripeSession': session.url,
        'returnUrl': returnUrl,
    })


@login_required
def manageSubscription(request):

    try:

        session = stripe.billing_portal.Session.create(
            customer=request.user.stripe_customer_id,
            return_url='https://filmstock.app/users/settings',
        )

        return HttpResponseRedirect(session.url, status=303)

    except:

        return HttpResponse(status=404)


@csrf_exempt
def provisionStripe(request):

    if request.method == 'POST':

            event = stripe.Webhook.construct_event(
                payload=request.body,
                sig_header=request.META['HTTP_STRIPE_SIGNATURE'],
                secret=os.getenv('STRIPE_WEBHOOK_SECRET'))
            data = event['data']
            event_type = event['type']

            if event_type == 'checkout.session.completed':
                try:
                    user = Hunter.objects.get(stripe_session_id__exact=data['object']['id'])
                    user.stripe_customer_id = data['object']['customer']
                    user.is_subscribed = True
                    user.save()
                    return HttpResponse(status=200)

                except Hunter.DoesNotExist:
                    return HttpResponse(status=404)

            elif event_type == 'invoice.paid':
                try:
                    user = Hunter.objects.get(stripe_customer_id__exact=data['object']['customer'])
                    user.is_subscribed = True
                    user.save()

                    return HttpResponse(status=200)

                except Hunter.DoesNotExist:
                    return HttpResponse(status=404)

            elif event_type == 'invoice.payment_failed':
                try:
                    user = Hunter.objects.get(stripe_customer_id__exact=data['object']['customer'])
                    user.is_subscribed = False
                    user.was_subscribed = True
                    user.save()
                    return HttpResponse(status=200)

                except Hunter.DoesNotExist:
                    return HttpResponse(status=404)

            else:
                print('Unhandled event type {}'.format(event_type))

            return HttpResponse(status=500)

    else: return HttpResponse(status=404)
