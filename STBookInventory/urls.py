from django.urls import path,re_path
from . import views  # Import your views from views.py
from .import api_views


urlpatterns = [
    path('add/', views.add_book, name='add_the_book'), #the name makes it possible to reference this link in the html template
    path('update/<int:book_id>/', views.update_book, name='update_the_book'), # We use <int:book_id> because id is our primary key #This is a GET request because of the parameter we insert which is the book_id
    path('book/<int:book_id>/', views.get_book, name='list_book'), #This is a GET request because of the parameter we insert which is the book_id
    path('list/', views.get_books, name='list_books'),
    path('search/', views.search_results, name='search_result'),
    path('', views.get_books, name='list_books'), #This is our home/index view for our templates html pages
    path('delete/<int:book_id>/', views.delete_book, name='delete_the_book'), #This is a GET request because of the parameter we insert which is the book_id
    path('checkout/<int:book_id>/', views.checkout_book, name='checkout_the_book'), #This is a GET request because of the parameter we insert which is the book_id
    path('return/<int:book_id>/', views.return_book, name='return_the_book'), #This is a GET request because of the parameter we insert which is the book_id
    path('create/api/',api_views.add_book_view, name='create_book_api'), #This is an API POST request
    path('read/api/<int:book_id>/',api_views.get_book_view, name='read_book_api'), #This is an API GET request
    path('read/api/',api_views.get_all_books_view, name='read_all_books_api'), #This is an API GET request
    path('update/api/<int:book_id>/',api_views.update_book_view, name='update_book_api'), #This is an API UPDATE request
    path('checkout/api/<int:book_id>/',api_views.checkout_book_view, name='update_book_api'),
    path('delete/api/<int:book_id>/',api_views.delete_book_view, name='delete_book_api'), #This is an API DELETE request
    re_path('login',api_views.login),
    re_path('logout',api_views.logout),
    re_path('signup',api_views.signup),
    re_path('test_token',api_views.test_token), #used for my token testing
    path('change_password/', api_views.change_password, name='change_password'),
    path('forgot_password/', api_views.forgot_password, name='forgot-password'),
    path('password_reset/<str:token>/', api_views.password_reset, name='password_reset'),
]


