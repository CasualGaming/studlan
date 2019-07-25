# -*- coding: utf-8 -*-

import uuid
from datetime import datetime

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from apps.authentication.forms import ChangePasswordForm, LoginForm, RecoveryForm, RegisterForm
from apps.authentication.models import RegisterToken
from apps.lan.models import Attendee, LAN
from apps.misc.forms import InlineSpanErrorList
from apps.userprofile.models import UserProfile


@sensitive_post_parameters()
def login(request):
    redirect_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, _(u'You have successfully logged in.'))
            if redirect_url:
                return HttpResponseRedirect(redirect_url)
            return HttpResponseRedirect('/')
        else:
            form = LoginForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
    else:
        form = LoginForm()

    response_dict = {'form': form, 'next': redirect_url}
    return render(request, 'auth/login.html', response_dict)


def logout(request):
    auth.logout(request)
    messages.success(request, _(u'You have successfully logged out.'))
    return HttpResponseRedirect('/')


@sensitive_post_parameters()
def register(request):
    if request.user.is_authenticated():
        messages.error(request, _(u'You cannot be logged in when registering.'))
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                cleaned = form.cleaned_data

                # Create user
                user = User(
                    username=cleaned['desired_username'],
                    first_name=cleaned['first_name'],
                    last_name=cleaned['last_name'],
                    email=cleaned['email'],
                )
                user.set_password(cleaned['password'])
                user.is_active = False
                user.save()

                # Create userprofile
                up = UserProfile(
                    user=user,
                    nick=cleaned['desired_username'],
                    date_of_birth=cleaned['date_of_birth'],
                    zip_code=cleaned['zip_code'],
                    address=cleaned['address'],
                    phone=cleaned['phone'],
                )
                up.save()

                # Create the registration token
                token = uuid.uuid4().hex
                rt = RegisterToken(user=user, token=token)
                rt.save()

                link = request.build_absolute_uri(reverse('auth_verify', args=[token]))
                context = {
                    'link': link,
                }
                txt_message = render_to_string('auth/email/verify_account.txt', context, request).strip()
                html_message = render_to_string('auth/email/verify_account.html', context, request).strip()
                send_mail(
                    subject=_(u'Verify your account'),
                    from_email=settings.STUDLAN_FROM_MAIL,
                    recipient_list=[user.email],
                    message=txt_message,
                    html_message=html_message,
                )

                messages.success(request, _(u'Registration successful. Check your email for verification instructions.'))

                return HttpResponseRedirect('/')
            else:
                form = RegisterForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
        else:
            form = RegisterForm()

        return render(request, 'auth/register.html', {'form': form})


@sensitive_post_parameters()
@permission_required('lan.register_new_user')
def direct_register(request):
    lan = LAN.objects.filter(end_date__gte=datetime.now()).first()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data

            if lan is None:
                messages.error(request, u'No upcoming LAN was found.')
                return HttpResponseRedirect('/auth/direct_register')

            # Create user
            user = User(
                username=cleaned['desired_username'],
                first_name=cleaned['first_name'],
                last_name=cleaned['last_name'],
                email=cleaned['email'],
            )
            user.set_password(cleaned['password'])
            user.is_active = True
            user.save()

            # Create userprofile
            up = UserProfile(
                user=user,
                nick=cleaned['desired_username'],
                date_of_birth=cleaned['date_of_birth'],
                zip_code=cleaned['zip_code'],
                address=cleaned['address'],
                phone=cleaned['phone'],
            )
            up.save()

            attendee = Attendee(lan=lan, user=user)
            attendee.save()

            messages.success(request, _(u'Registration successful.'))

            return HttpResponseRedirect('/auth/direct_register')
        else:
            form = RegisterForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
    else:
        form = RegisterForm()

    return render(request, 'auth/direct_register.html', {'form': form, 'lan': lan})


def verify(request, token):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        rt = get_object_or_404(RegisterToken, token=token)

        if rt.is_valid:
            user = getattr(rt, 'user')

            user.is_active = True
            user.save()
            rt.delete()

            messages.success(request, _(u'User ') + user.username + _(u' successfully activated. You can now log in.'))

            return redirect('auth_login')
        else:
            messages.error(request, _(u'The token has expired. Please use the password recovery to get a new token.'))
            return HttpResponseRedirect('/')


@sensitive_post_parameters()
def recover(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = RecoveryForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                users = User.objects.filter(email__iexact=email)

                if users.count() == 0:
                    messages.error(request, _(u'No users are registered with that email address.'))
                    return HttpResponseRedirect('/')

                # Send recovery email to all associated users
                for user in users.all():
                    # Create the registration token
                    token = uuid.uuid4().hex
                    rt = RegisterToken(user=user, token=token)
                    rt.save()

                    link = request.build_absolute_uri(reverse('auth_set_password', args=[token]))
                    context = {
                        'link': link,
                        'username': user.username,
                        'email': user.email,
                    }
                    txt_message = render_to_string('auth/email/recover_account.txt', context, request).strip()
                    html_message = render_to_string('auth/email/recover_account.html', context, request).strip()
                    send_mail(
                        subject=_(u'Account recovery'),
                        from_email=settings.STUDLAN_FROM_MAIL,
                        recipient_list=[user.email],
                        message=txt_message,
                        html_message=html_message,
                    )

                messages.success(request, _('A recovery link has been sent to all users with email "') + email + '".')
                return HttpResponseRedirect('/')
            else:
                form = RecoveryForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
        else:
            form = RecoveryForm()

        return render(request, 'auth/recover.html', {'form': form})


@sensitive_post_parameters()
def set_password(request, token=None):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        rt = get_object_or_404(RegisterToken, token=token)

        if rt.is_valid:
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
                if form.is_valid():
                    user = getattr(rt, 'user')

                    user.is_active = True
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()

                    rt.delete()

                    messages.success(request, _(u'User ') + unicode(user) + _(u' successfully had it\'s password changed. You can now log in.'))

                    return HttpResponseRedirect('/')
            else:

                form = ChangePasswordForm()

                messages.success(request, _(u'Token accepted. Please insert your new password.'))

            return render(request, 'auth/set_password.html', {'form': form, 'token': token})

        else:
            messages.error(request, _(u'The token has expired. Please use the password recovery to get a new token.'))
            return HttpResponseRedirect('/')
