from .serializers import BookSerializer #This line imports the BookSerializer class from a module located in the same directory as the current module. The . in the import statement indicates the current package or directory. In this context, it means that the BookSerializer class is defined in a module within the same app.
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from .models import User
from .serializers import UserSerializer
from rest_framework import status

from .models import Book #Similar to the previous line, this imports the Book model from a module located in the same directory. It's common to organize your Django app with models, views, and serializers in the same package or directory.
from .models import User
from .models import BookCheckout

from rest_framework.pagination import PageNumberPagination #Implementing pagination for REST API JSON view
from rest_framework.response import Response #This line imports the Response class from the response module of the Django REST framework. The Response class is used to create HTTP responses for API views. You can return Response objects from your API views to send data back to clients in a structured format, typically as JSON.
from rest_framework.decorators import api_view #This line imports the api_view decorator from the decorators module of the Django REST framework. The api_view decorator is used to define view functions that can handle different HTTP methods (GET, POST, PUT, DELETE, etc.)  for specific API endpoints. By applying the api_view decorator to a function, you can ensure that the view function only responds to the specified HTTP methods and follows RESTful conventions.


from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token #imports for our user authentication
from django.contrib.auth import get_user_model #from django.contrib.auth.models import User
User = get_user_model()

from .serializers import ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash

from django.shortcuts import get_object_or_404

import secrets
from django.core.mail import send_mail
from django.urls import reverse

from .serializers import ForgotPasswordSerializer
from django.core.cache import cache  # Import cache module

import json
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

from drf_spectacular.utils import extend_schema #To make the schema help details appear at the bottom of Swagger UI website
@extend_schema(responses=BookSerializer)   #BookSerializer is a reponse becuase we get the books from the database and convert it using the serializer and then present it to the user in json format as a reponse
@extend_schema(request=UserSerializer)   #UserSerializer is a request because we request a user input and that is then serialized


#CRUD Operations GET POST PUT/PATCH DELETE

@api_view(["POST"]) ##This is a decorator provided by Django REST framework (DRF). It specifies that the add_book_view function should only respond to HTTP POST requests. This means that the view will handle requests where clients want to create new book records. It enforces the RESTful convention of using specific HTTP methods for specific actions. #This is the view function that handles the incoming HTTP POST request for adding a new book. It takes a request object as a parameter, which contains information about the client's request, including the data sent in the request.
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_book_view(request):
    if not request.auth: # Your custom authentication logic to check for the presence of the token
        return Response({"detail": "Authentication token is required."}, status=status.HTTP_401_UNAUTHORIZED)
        
    if request.method == "POST": #This conditional checks if the HTTP method used for the request is indeed a POST request. This is a safety measure to ensure that the view only processes POST requests.
        request.data['user'] = request.user.id # Ensure the 'user' field in the posted JSON data is equal to the id of the logged-in user
        if isinstance(request.data, dict):  #Check if the data is a single JSON object
            data = [request.data]  # Convert the single object to a list
        elif isinstance(request.data, list): #Check if the data is a multiple JSON objects
            data = request.data #No convertion needed if input data is a list
        else:
            return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)

        responses = []   #create an empty list array

        for book_data in data: #this iterates over each element in the data list the user provided
            serializer = BookSerializer(data=book_data) #Here, a BookSerializer instance is created for each book_data, and it's initialized with the data extracted from the request. The purpose of the serializer is to validate the incoming data and convert it into a format suitable for creating a new book record in the database
            if serializer.is_valid(): #This conditional checks if the data provided in the request is valid according to the rules specified in the BookSerializer class. The is_valid() method is a validation step provided by DRF to ensure the data complies with the defined model and serializer rules
                serializer.save()
                responses.append(serializer.data) # Append the serialized data to the empty responses list
            else:
                responses.append(serializer.errors) # If any single book_data is not valid, append that particular book's validation errors to the responses list. So if in your json list provided to create multiple books, some few books had error with their syntax, all the other books will still be created and the ones that had errors will show error in their particular json response
                
        return Response(responses, status=status.HTTP_201_CREATED) # Return the combined responses for all books
    else:
        return Response({"error": "Invalid HTTP method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        

@api_view(["GET"]) #This is the view function that handles the incoming HTTP GET request. It takes two parameters: request and book_id. The request parameter contains information about the client's request, and book_id is a parameter extracted from the URL, typically used to identify the specific book to retrieve.
@authentication_classes([TokenAuthentication,SessionAuthentication])
@permission_classes([IsAuthenticated])
def get_book_view(request, book_id):
    if not request.auth: # Your custom authentication logic to check for the presence of the token
        return Response({"detail": "Authentication token is required."}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        book = Book.objects.filter(id=book_id).first() #In this line, the view retrieves a book record from the database using the book_id provided in the URL. It uses the Django Object-Relational Mapping (ORM) to filter the Book model by the id field, which should match the book_id provided in the URL. The first() method is used to get the first matching book if it exists. We removed .first() so that the try except function is able to read the error, otherwise it returns the first occurence of the book which in this case are empty fields
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data)
        else:
            return Response({'error': 'Book does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except: #This conditional checks if a book with the specified book_id was found in the database. If a book exists, the condition evaluates to True.
        return Response({'error': 'Book does not exist'}, status=status.HTTP_404_NOT_FOUND)    
    

@api_view(["GET"]) #This is the view function that handles the incoming HTTP GET request. It takes two parameters: request and book_id. The request parameter contains information about the client's request, and book_id is a parameter extracted from the URL, typically used to identify the specific book to retrieve.
@authentication_classes([TokenAuthentication,SessionAuthentication]) #Session Auth makes it possible for user login in browsable api
@permission_classes([IsAuthenticated])
def get_all_books_view(request):
    if not request.auth: # Your custom authentication logic to check for the presence of the token
        return Response({"detail": "Authentication token is required."}, status=status.HTTP_401_UNAUTHORIZED)
        
    paginator = PageNumberPagination()
    paginator.page_size = 10
    books = Book.objects.all()
    if books: #This conditional checks if a book with the specified book_id was found in the database. If a book exists, the condition evaluates to True.
        result_page = paginator.paginate_queryset(books,request)
        serializer = BookSerializer(result_page, many=True) #Here, a BookSerializer instance is created, and it's initialized with the book object that was retrieved from the database. The purpose of the serializer is to convert the book object into a serialized format that can be easily rendered as JSON or another content type for the response.
        return paginator.get_paginated_response(serializer.data) #If a book was found and successfully serialized, this line returns a DRF Response object. The response contains the serialized data of the book, which is typically returned to the client as a JSON response. This allows the client to receive detailed information about the book. The HTTP status code of the response will be 200 (OK) by default, indicating a successful GET request.

    return Response({"detail": "No books found."}, status=status.HTTP_404_NOT_FOUND) # If no books were found, return a 404 response


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_book_view(request, book_id):
    if not request.auth: # Your custom authentication logic to check for the presence of the token
        return Response({"detail": "Authentication token is required."}, status=status.HTTP_401_UNAUTHORIZED)
    
    user = request.user # Get the user associated with the token

    if user.account_type == 'Admin' or user.account_type == 'Staff Member':  # Check if the user has the required account_type
        book = get_object_or_404(Book, id=book_id) # User has the required account_type, proceed with the update
        data = request.data
        serializer = BookSerializer(book, data=data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    else: # User does not have the required account_type
        return Response("Permission Denied: User does not have the required account_type", status=403)



@api_view(["PATCH"]) #This (@api_view) is a decorator provided by Django Rest Framework. It specifies that the decorated function is intended to handle HTTP PATCH requests. In your case, the function checkout_book_view is designed to handle partial updates to a book resource.
@authentication_classes([TokenAuthentication]) #This decorator specifies the authentication classes that will be used to authenticate the user making the request. Here, TokenAuthentication is used, which means that the user must provide a valid token in the request header for authentication.
@permission_classes([IsAuthenticated]) #This decorator specifies the permission classes that control access to the view. IsAuthenticated ensures that only authenticated users can access the view. If a user is not authenticated, a 401 Unauthorized response will be returned.
def checkout_book_view(request, book_id):  #This is the function definition. It declares a view function named checkout_book_view that takes two parameters: request (representing the HTTP request) and book_id (representing the identifier of the book to be checked out).
    try: #try-except block: This is used to handle the case where the specified book with the given book_id is not found in the database. If the book is not found, a 404 Not Found response is returned with a message indicating that the book was not found
        book = Book.objects.get(id=book_id) # It attempts to retrieve a Book object from the database using the provided book_id. If the book is not found, a Book.DoesNotExist exception is caught, and a response is returned with a message indicating that the book was not found, along with a 404 Not Found status code.
    except Book.DoesNotExist:
        return Response({"detail": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    if not request.auth: #This checks if there is an authentication token in the request (request.auth) database #if not request.auth:: Checks if there is an authentication token in the request. If not, it returns a 401 Unauthorized response, indicating that an authentication token is required.
        return Response({"detail": "Authentication token is required."}, status=status.HTTP_401_UNAUTHORIZED)

    user = request.user #user = request.user: Retrieves the user making the request from the request object.

    if user.account_type in ['Admin', 'Staff Member']: #if user.account_type in ['Admin', 'Staff Member']:: Checks if the user has an account type of 'Admin' or 'Staff Member'. If yes, it proceeds to the next level of checks.
        if book.available_copies > 0: #if book.available_copies > 0:: Checks if there are available copies of the book. If yes, it creates a new BookCheckout instance, saves it to the database, updates theavailable_copies field of the book, and saves the changes to the book model.
            checkout = BookCheckout(book=book, user=request.user)
            checkout.save()

            book.available_copies -= 1  # Update available_copies field directly
            book.save()  # Save the changes to the book model

            return Response({"detail": "Book checked out successfully."}, status=status.HTTP_200_OK) #If everything is successful, it returns a 200 OK response with a message indicating that the book was checked out successfully
        else:
            return Response({"detail": "No available copies of the book."}, status=status.HTTP_400_BAD_REQUEST) #else:: If there are no available copies, it returns a 400 Bad Request response indicating that there are no available copies of the book.
    else:
        return Response({"detail": "Permission Denied: User does not have the required account_type"}, status=status.HTTP_403_FORBIDDEN) #If the user does not have the required account type ('Admin' or 'Staff Member'), it returns a 403 Forbidden response with a message indicating that the user does not have the required account type



@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_book_view(request, book_id): 
    if not request.auth: # Your custom authentication logic to check for the presence of the token
        return Response({"detail": "Authentication token is required."}, status=status.HTTP_401_UNAUTHORIZED)
        
    user = request.user # Get the user associated with the token

    if user.account_type == 'Admin': # Check if the user has the required account_type
        book = get_object_or_404(Book, id=book_id) # User has the required account_type, proceed with the delete
        book.delete()
        return Response("Book successfully deleted", status=204)
    else:
        return Response("Permission Denied: User does not have the required account_type", status=403) # User does not have the required account_type


@api_view(['POST']) #This decorator specifies that the view function should only respond to HTTP POST requests
@parser_classes([JSONParser])
def login(request):
    user = get_object_or_404(User, email=request.data['email']) #This line retrieves a user from the database based on the provided username in the request data (meaning your json POST request for postman should have a username key). get_object_or_404 is a helper function provided by Django that retrieves an object from the database and raises a 404 Not Found exception if the object doesn't exist. In this case, it's used to retrieve the user based on the username provided in the request data.
    if not user.check_password(request.data['password']): #This condition checks whether the provided password in the request data matches the user's password stored in the database if no error shows up. check_password is a method provided by Django's user model to compare a plaintext password with the hashed password stored in the database.
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND) #If the passwords don't match, it returns a 404 Not Found response, indicating that the user was not found
    token, created = Token.objects.get_or_create(user=user) #    This line generates an authentication token for the user. It uses DRF's Token model to create or retrieve a token associated with the user. The created variable indicates whether a new token was created for the user. If a token already exists, it returns the existing token.
    serializer = UserSerializer(instance=user) #This line creates a serializer for the user instance. UserSerializer is assumed to be a serializer that you've defined for your User model. It's used to convert the user object into a JSON response
    return Response({"token": token.key, "user": serializer.data}) #This line sends a response with the token and user data in JSON format. The token.key attribute provides the generated authentication token key.serializer.data contains the serialized user data.


@api_view(['POST'])
def logout(request):
    user = request.user
    token = Token.objects.filter(user=user)
    token.delete()
    return Response({"message": "User logged out"})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data) #This line creates an instance of the UserSerializer to serialize and validate the data received in the request. The UserSerializer is assumed to be a serializer that you've defined for your User model
    if serializer.is_valid(): #This condition checks if the serializer's data is valid. If the data is valid, it proceeds to create a new user
        serializer.save()
        user = User.objects.get(email=request.data['email']) #This line retrieves the newly created user from the database based on the username provided in the request data. However, this step seems unnecessary because you've already created the user with serializer.save()
        user.set_password(request.data['password']) #This line sets the user's password. It's essential to hash the password using Django's built-in password hashing mechanisms.
        user.save() #This line saves the user object with the updated password
        token = Token.objects.create(user=user) #This code generates an authentication token for the newly created user using DRF's Token model.
        return Response({"token":token.key}) #If the data is valid, the code returns a JSON response with the user's token and serialized user data
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_unique_token():
    return secrets.token_urlsafe(32)

def send_reset_email(email, token):
    reset_url = reverse('password_reset', kwargs={'token': token})  # Construct the URL for the password reset view #The token has been infused into the password_url endpoint in order to provide a unique url so the user does not have to input the url again. #This modification uses the reverse function to dynamically generate the URL for the password_reset view based on its name and includes it in the email message
    absolute_reset_url = f'http://127.0.0.1:8000/stbookinventory/{reset_url}'  # input your url endpoint here minus the view

    # Message with the URL and instructions
    message = f'To reset your password, make a POST request to:\n\n{absolute_reset_url}\n\n' \
              'Include the following JSON data in your request body:\n\n' \
              '[{"email": "your_email_address"},{"new_password": "your_new_password"}]\n\n' \
              'This link will expire in 15 minutes.'

    subject = 'Password Reset Request'
    from_email = 'marvinalamu@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@api_view(['POST'])
def forgot_password(request):
    serializer = ForgotPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        token = generate_unique_token() # Generate a unique one-time token
        cache_key = f'password_reset_token_{token}' 
        cache.set(cache_key, email, timeout=900)  # Store the token in the cache with a short expiration time (e.g., 15 minutes) # 900 seconds = 15 minutes

        send_reset_email(email, token)  #i have Implemented a function for send_email already above # i have also set the logic to send the email with the reset link and token

        return Response({'message': 'Password reset link sent successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(['POST'])
def password_reset(request, token):
    cache_key = f'password_reset_token_{token}' # Retrieve the email associated with the token from the cache
    email = cache.get(cache_key)
    if not email:
        return JsonResponse({'error': 'Invalid or expired password reset link.'}, status=400)

    new_password = json.loads(request.body.decode('utf-8')).get('new_password') # Reset the user's password
    user = User.objects.get(email=email)
    user.password = make_password(new_password)
    user.save()

    cache.delete(cache_key) # Remove the token from the cache after using it

    return JsonResponse({'message': 'Password reset successful.'}, status=200)


@api_view(['GET']) #this function will be responsible for handling GET requests to a specific URL endpoint.
@authentication_classes([SessionAuthentication, TokenAuthentication]) #This class is used for session-based authentication, which is common for web applications. This class is used for token-based authentication, often used for RESTful APIs
@permission_classes([IsAuthenticated]) #This permission class ensures that only authenticated users (users who have provided valid authentication credentials) are allowed to access the view.
def test_token(request): #This is the definition of the view function named test_token. It takes a single argument, request, which represents the HTTP request made to this view.
    return Response("passed for {}".format(request.user.email)) #The {} part is a placeholder for the user's email, which is retrieved from request.user.email. The request.user object represents the currently authenticated user, and request.user.email retrieves the user's email address.
