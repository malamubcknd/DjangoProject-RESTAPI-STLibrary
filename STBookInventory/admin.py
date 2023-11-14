from django.contrib import admin

from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
User = get_user_model()

#from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import User
from .models import Book
from .models import BookCheckout

#admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookCheckout)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['is_active'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['is_staff'].disabled = True
            form.base_fields['email'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['groups'].disabled = True
            form.base_fields['password'].disabled = True
            form.base_fields['name'].disabled = True
            form.base_fields['date_joined'].disabled = True
            form.base_fields['last_login'].disabled = True
            # form.base_fields['save'].disabled = True
        return form
    
    def has_delete_permission(self, request, obj=None):
            return False
    
    def has_change_permission(self, request, obj=None):
        if request.user.has_perm('STBookInventory.change_user'):
            return True
        else:
            return False
    
    def has_view_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return False 

