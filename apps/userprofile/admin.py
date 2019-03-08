# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.forms import models

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


class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('groups', 'is_staff', 'is_superuser')
    filter_horizontal = ('groups',)
    actions = ['activate_users', 'deactivate_users', 'forcefully_logout_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    def deactivate_users(self, request, queryset):
        for user in queryset:
            if user.id == request.user.id:
                self.message_user(request, 'You cannot deactivate yourself! No actions were performed.', level=messages.WARNING)
                return
        queryset.update(is_active=False)

    def forcefully_logout_users(self, request, queryset):
        for session in Session.objects.all():
            session_user = int(session.get_decoded().get('_auth_user_id'))
            for user in queryset:
                if user.id == session_user:
                    session.delete()

    activate_users.short_description = 'Activate'
    deactivate_users.short_description = 'Deactivate'
    forcefully_logout_users.short_description = 'Forcefully logout'


admin.site.register(User, UserProfileAdmin)
admin.site.register(AliasType)
admin.site.register(Alias)
