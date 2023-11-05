from django.contrib import admin

# Register your models here.

from .models import User
from .models import Book
from .models import BookCheckout

admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookCheckout)