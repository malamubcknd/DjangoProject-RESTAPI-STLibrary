#Lets reference our custom user model other than django's built-in authentication
# from django.contrib.auth import get_user_model

# Create your views here.

from django.shortcuts import render, redirect
from .models import Book

# Create a form for adding books
from .forms import BookForm  

#Create a view to add a book
#The add_book view function is responsible for handling HTTP requests to create new book records
def add_book(request):
# If the request is a POST request, it creates a BookForm instance using the data from the request 
# (request.POST) to populate the form fields. If its a GET request or any other scenario, it will return reload the 
# page again. We can actually make sure if its a GET request, we return the list of books.
    if request.method == 'POST':
        form = BookForm(request.POST)
#if the inputs into the form via the view are all correct, it wil successfuly save and
#  redirect to show the list of books else it will reload the page again
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'STBookInventory/add_book.html', {'form': form})


#Create a view to update a book
#it takes two parameters, request and book_id. Remember HTTP request is POST GET UPDATE PATCH or DELETE
def update_book(request, book_id):
#This line fetches a book object from the database based on the book_id parameter passed in the URL.
#It uses Book.objects.get() to retrieve a specific book by its primary key (pk). 
    book = Book.objects.get(pk=book_id)
#This conditional statement checks if the HTTP request method is a POST request. 
#In Django, POST requests are typically used when submitting form data to the server.    
    if request.method == 'POST':
#When the request is a POST request, it means the user is submitting data to update the book. 
#To handle this, a BookForm instance is created using the data from the POST request (request.POST) and
#the existing book object (instance=book). This allows the form to be pre-populated with the current book's data.        
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
#    If the request is not a POST request (i.e., it's a GET request), the view creates a new BookForm instance 
# using the book's data as an initial instance. This means that when a user accesses the update page, the form
#  will be pre-filled with the existing book's data, allowing them to make modifications.        
    else:
        form = BookForm(instance=book)
    return render(request, 'STBookInventory/update_book.html', {'form': form})


#Create a view to get a single book
def get_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'STBookInventory/book_detail.html', {'book': book})


#Create a view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'STBookInventory/book_list.html', {'books': books})


#Create a view to delete a book
def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'STBookInventory/delete_book.html', {'book': book})


from .models import BookCheckout
def checkout_book(request, book_id):
#it goes into the BookCheckout model to pick up the respective book_id the viewer inputted
    book = Book.objects.get(pk=book_id)
#The method needs to be a post request specified in the html file also
    if book.available_copies > 0:
        # Assuming you have a BookCheckout model to track checkouts, create a new checkout instance.
        # You'll need to pass the user who is checking out the book (e.g., request.user).
        # This code assumes you're using Django's built-in authentication system.
        
        # from .models import BookCheckout  # Import the BookCheckout model
       
        # Create a new checkout instance
        checkout = BookCheckout(book=book, user=request.user)  # Pass the book and user
        #form = BookForm(request.POST, instance=book)
        # Save the checkout instance to the database
        checkout.save()
        
        # Decrease available copies when a book is checked out
        #This only works for when a person checks out 1 book at a time. What if multiple books are checked 
        #out at the same time? I will get back to this later
        book.update_available_copies(increment=-1)
        
        # Redirect to a success or confirmation page
        #return redirect('STBookInventory/checkout_success.html')
        return render(request, 'STBookInventory/checkout_success.html')
    else:
        # Handle the case where no copies are available
        # You can return an error or a message to the user
        return render(request, 'STBookInventory/checkout_error.html')


#The return view likewise, uses the Book Model
#We are goint to use the Book Model to Update the Total number of books now that a certain book is returned
#we define a function called return_book which takes two parameters
def return_book(request, book_id):
    book = Book.objects.get(pk=book_id)    

#This conditional statement checks if the HTTP request method is a POST request. 
#In Django, POST requests are typically used when submitting form data to the server.    
    if request.method == 'POST':
#When the request is a POST request, it means the user is submitting data to update the book. 
#To handle this, a BookForm instance is created using the data from the POST request (request.POST) and
#the existing book object (instance=book). This allows the form to be pre-populated with the current book's data.        
        
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
#    If the request is not a POST request (i.e., it's a GET request), the view creates a new BookForm instance 
# using the book's data as an initial instance. This means that when a user accesses the update page, the form
#  will be pre-filled with the existing book's data, allowing them to make modifications.        
    else:
        form = BookForm(instance=book)
    return render(request, 'STBookInventory/update_book.html', {'form': form})