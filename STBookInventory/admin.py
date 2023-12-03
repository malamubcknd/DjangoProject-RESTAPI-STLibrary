from django.contrib import admin

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import User
from .models import Book
from .models import BookCheckout

admin.site.register(Book) #Register my book model
admin.site.register(BookCheckout) #Register my BookCheckout model

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email",)
    fieldsets = (
        ('User Details', {'fields': ('name', 'email', 'account_type')}),
        ('Permissions', {'fields': ('groups','user_permissions','is_staff', 'is_active', 'is_superuser')}),
        ('User Timeline', {'fields': ('date_joined', 'last_login')}),
    )


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

