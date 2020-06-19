# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.forms import models
from django.utils.translation import ugettext_lazy as _

from apps.userprofile.models import Alias, AliasType, UserProfile

admin.site.unregister(User)


class NoDeleteInline(models.BaseInlineFormSet):
    """ Custom formset to prevent deletion
    Used by the inline for userprofiles to prevent the possibility
    of deleting the profile object
    """
    def __init__(self, *args, **kwargs):
        super(NoDeleteInline, self).__init__(*args, **kwargs)
        self.can_delete = False


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    formset = NoDeleteInline


class UserCustomPermissionFilter(admin.SimpleListFilter):
    title = _(u'custom permissions')
    parameter_name = u'custom_permissions'

    def lookups(self, request, model_admin):
        return (
            (u'some', _(u'Some')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'some':
            return queryset.exclude(user_permissions=None)
        else:
            return queryset


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('groups', 'is_staff', 'is_superuser', 'is_active', UserCustomPermissionFilter)
    filter_horizontal = ('groups',)
    actions = ['activate_users', 'deactivate_users', 'forcefully_logout_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        messages.success(request, _(u'Successfully activated the selected users.'))

    def deactivate_users(self, request, queryset):
        for user in queryset:
            if user.id == request.user.id:
                messages.warning(request, _(u'You cannot deactivate yourself! No actions were performed.'))
                return

        queryset.update(is_active=False)
        messages.success(request, _(u'Successfully deactivated the selected users.'))

    def forcefully_logout_users(self, request, queryset):
        # Works only with session engine
        count = 0
        for session in Session.objects.all():
            session_user_str = session.get_decoded().get('_auth_user_id')
            if session_user_str is None:
                continue
            session_user = int(session_user_str)
            for user in queryset:
                if user.id == session_user:
                    session.delete()
                    count += 1

        messages.success(request, _(u'Successfully invalidated {count} user sessions.').format(count=count))

    activate_users.short_description = _(u'Activate')
    deactivate_users.short_description = _(u'Deactivate')
    forcefully_logout_users.short_description = _(u'Forcefully log out')


admin.site.register(User, UserProfileAdmin)
admin.site.register(AliasType)
admin.site.register(Alias)
