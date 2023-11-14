from django.contrib import admin
#from django.contrib.auth.models import Group
# Register your models here.

from .models import User
from .models import Book
from .models import BookCheckout

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookCheckout)
#admin.site.unregister(Group) #This unregisters the Groups menu from the admin site such that you can't see