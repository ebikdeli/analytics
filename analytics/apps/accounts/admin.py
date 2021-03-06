from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .models import Address


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'address', 'is_admin', 'picture', 'background')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'address', 'name',)}),
        ('Scores', {'fields': ('score', 'score_lifetime', 'discount_value', 'discount_percent')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('pictures', {'fields': ('picture', 'background',)})
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Address)
