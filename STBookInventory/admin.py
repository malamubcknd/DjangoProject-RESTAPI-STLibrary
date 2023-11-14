from django.contrib import admin

from django.contrib.auth import get_user_model
User = get_user_model()

#from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import User
from .models import Book
from .models import BookCheckout

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookCheckout)


#I do not want staff to be able to change their status (staff, superuser, active) on the admin site
#This unregisters the Groups menu from the admin site such that you can't see
admin.site.unregister(User)
#admin.site.unregister(Group)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['is_active'].disabled = True
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['email'].disabled = True
            form.base_fields['user_permissions'].disabled = True
            form.base_fields['groups'].disabled = True
            form.base_fields['password'].disabled = True
        return form

