from django.urls import path,re_path
from . import views  # Import your views from views.py
from .import api_views


urlpatterns = [
    path('add/', views.add_book, name='add_book'),
    path('update/<int:book_id>/', views.update_book, name='update_book'), #This is a GET request because of the parameter we insert which is the book_id
    path('book/<int:book_id>/', views.get_book, name='book_detail'), #This is a GET request because of the parameter we insert which is the book_id
    path('list/', views.list_books, name='list_books'),
    path('', views.list_books, name='list_books'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'), #This is a GET request because of the parameter we insert which is the book_id
    path('checkout/<int:book_id>/', views.checkout_book, name='checkout_book'), #This is a GET request because of the parameter we insert which is the book_id
    path('return/<int:book_id>/', views.return_book, name='return_book'), #This is a GET request because of the parameter we insert which is the book_id
    path('create/api/',api_views.add_book_view, name='create_book_api'), #This is an API POST request
    path('read/api/<int:book_id>/',api_views.get_book_view, name='read_book_api'), #This is an API GET request
    path('read/api/',api_views.get_all_books_view, name='read_all_books_api'), #This is an API GET request
    path('update/api/<int:book_id>/',api_views.update_book_view, name='update_book_api'), #This is an API UPDATE request
    path('checkout/api/<int:book_id>/',api_views.checkout_book_view, name='update_book_api'),
    path('delete/api/<int:book_id>/',api_views.delete_book_view, name='delete_book_api'), #This is an API DELETE request
    re_path('login',api_views.login),
    re_path('logout',api_views.logout),
    re_path('signup',api_views.signup),
    re_path('test_token',api_views.test_token),
    path('change_password/', api_views.change_password, name='change_password'),
]


