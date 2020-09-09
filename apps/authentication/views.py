# -*- coding: utf-8 -*-

import uuid
from datetime import datetime

from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST, require_safe

from apps.authentication.forms import ChangePasswordForm, LoginForm, RecoveryForm, RegisterForm
from apps.authentication.models import RegisterToken
from apps.lan.models import Attendee, LAN
from apps.misc.forms import InlineSpanErrorList
from apps.userprofile.models import UserProfile


@sensitive_post_parameters()
def login(request):
    # Parse next URL
    if request.method == 'POST':
        redirect_url = request.POST.get('next', '/')
    else:
        redirect_url = request.GET.get('next', '/')
    redirect_url_safe = is_safe_url(
        url=redirect_url,
        allowed_hosts=settings.ALLOWED_HOSTS,
        require_https=request.is_secure(),
    )
    if not redirect_url_safe:
        redirect_url = '/'

    # Redirect silently to home if already logged in
    # This prevents missing permission redirect loops and login redirect chains
    if request.user.is_authenticated():
        return redirect('/')

    # Attempt login or show login form
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, _(u'You have successfully logged in.'))
            return redirect(redirect_url)
        else:
            form = LoginForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
    else:
        form = LoginForm()

    response_dict = {'form': form, 'next': redirect_url}
    return render(request, 'auth/login.html', response_dict)


@require_POST
@login_required
def logout(request):
    redirect_url = request.GET.get('next', '/')
    redirect_url_safe = is_safe_url(
        url=redirect_url,
        allowed_hosts=settings.ALLOWED_HOSTS,
        require_https=request.is_secure(),
    )
    if not redirect_url_safe:
        redirect_url = '/'

    auth.logout(request)

    messages.success(request, _(u'You have successfully logged out.'))
    return redirect(redirect_url)


@sensitive_post_parameters()
def register(request):
    if request.user.is_authenticated():
        messages.warning(request, _(u'You\'re already logged in.'))
        return redirect('/')

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

            return redirect('/')
        else:
            form = RegisterForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


@require_safe
@permission_required('lan.register_new_user')
def direct_register_list(request):
    context = {}
    context['upcoming_lans'] = LAN.objects.filter(end_date__gte=datetime.now()).order_by('start_date')
    context['previous_lans'] = LAN.objects.filter(end_date__lt=datetime.now()).order_by('-start_date')
    return render(request, 'auth/direct_register_list.html', context)


@sensitive_post_parameters()
@permission_required('lan.register_new_user')
def direct_register(request, lan_id):
    lan = get_object_or_404(LAN, id=lan_id)

    if lan.is_ended():
        messages.error(request, _(u'The LAN is ended, arrivals can\'t be changed.'))
        return redirect('/')

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

            return redirect('/auth/direct_register')
        else:
            form = RegisterForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
    else:
        form = RegisterForm()

    breadcrumbs = (
        (lan, lan.get_absolute_url()),
        (_(u'Manual Registration'), ''),
    )
    context = {
        'breadcrumbs': breadcrumbs,
        'lan': lan,
        'form': form,
    }

    return render(request, 'auth/direct_register.html', context)


@require_safe
def verify(request, token):
    if request.user.is_authenticated():
        messages.error(request, _(u'You can\'t do that while logged in.'))
        return redirect('/')

    rt = get_object_or_404(RegisterToken, token=token)

    if rt.is_valid:
        user = getattr(rt, 'user')

        user.is_active = True
        user.save()
        rt.delete()

        messages.success(request, _(u'User {user} was successfully activated. You can now log in.').format(user=user))

        return redirect('auth_login')
    else:
        messages.error(request, _(u'The activation link has expired. Please use the password recovery form to get a new link.'))
        return redirect('/')


@sensitive_post_parameters()
def recover(request):
    if request.user.is_authenticated():
        messages.error(request, _(u'You can\'t do that while logged in.'))
        return redirect('/')

    if request.method == 'POST':
        form = RecoveryForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(email__iexact=email)

            if users.count() == 0:
                messages.error(request, _(u'No users are registered with that email address.'))
                return redirect('/')

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

            messages.success(request, _(u'A recovery link has been sent to all users with email address "{email}".').format(email=email))
            return redirect('/')
        else:
            form = RecoveryForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
    else:
        form = RecoveryForm()

    return render(request, 'auth/recover.html', {'form': form})


@sensitive_post_parameters()
def set_password(request, token=None):
    if request.user.is_authenticated():
        messages.error(request, _(u'You can\'t do that while logged in.'))
        return redirect('/')

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

                messages.success(request, _(u'Successfully changed password for user {user}. You can now log in.').format(user=user))
                return redirect('/')
        else:
            form = ChangePasswordForm()
            messages.info(request, _(u'Please set a new password.'))

        return render(request, 'auth/set_password.html', {'form': form, 'token': token})

    else:
        messages.error(request, _(u'The recovery link has expired. Please use the password recovery form to get a new link.'))
        return redirect('/')
