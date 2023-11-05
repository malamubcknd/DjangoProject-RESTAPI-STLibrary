#This line imports the BookSerializer class from a module located in the same directory as the current module. The . in the import statement indicates the current package or directory. In this context, it means that the BookSerializer class is defined in a module within the same app.
from .serializers import BookSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


#Similar to the previous line, this imports the Book model from a module located in the same directory. It's common to organize your Django app with models, views, and serializers in the same package or directory.
from .models import Book
from .models import User


#This line imports the Response class from the response module of the Django REST framework. The Response class is used to create HTTP responses for API views. You can return Response objects from your API views to send data back to clients in a structured format, typically as JSON.
from rest_framework.response import Response

#This line imports the api_view decorator from the decorators module of the Django REST framework. The api_view decorator is used to define view functions that can handle different HTTP methods (GET, POST, PUT, DELETE, etc.)  for specific API endpoints. By applying the api_view decorator to a function, you can ensure that the view function only responds to the specified HTTP methods and follows RESTful conventions.
from rest_framework.decorators import api_view

#imports for our user authentication
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model


from django.shortcuts import get_object_or_404


#CRUD Operations GET POST PUT/PATCH DELETE

#This is a decorator provided by Django REST framework (DRF). It specifies that the create_book_view function should only respond to HTTP POST requests. This means that the view will handle requests where clients want to create new book records. It enforces the RESTful convention of using specific HTTP methods for specific actions.
@api_view(["POST"])
#This is the view function that handles the incoming HTTP POST request for adding a new book. It takes a request object as a parameter, which contains information about the client's request, including the data sent in the request.
def add_book_view(request):
    #This conditional checks if the HTTP method used for the request is indeed a POST request. This is a safety measure to ensure that the view only processes POST requests.
    if request.method == "POST":
        #This line extracts the data sent in the request from the request object. The data is typically in JSON format and contains information about the book to be created.
        data = request.data
        #Here, a BookSerializer instance is created, and it's initialized with the data extracted from the request. The purpose of the serializer is to validate the incoming data and convert it into a format suitable for creating a new book record in the database
        serializer = BookSerializer(data=data)
        #This conditional checks if the data provided in the request is valid according to the rules specified in the BookSerializer class. The is_valid() method is a validation step provided by DRF to ensure the data complies with the defined model and serializer rules
        if serializer.is_valid():
            serializer.save()
            #If the book creation is successful, the view returns a Response object. This response includes the serialized data of the newly created book, which is typically returned to the client as a JSON response. A status code of 201 (Created) is also included in the response to indicate that the request was successful.
            return Response(serializer.data, status=201)
        else:
            #If the data provided in the request is not valid according to the serializer's rules, the view returns a Response object with the validation errors (found in serializer.errors) and a status code of 400 (Bad Request)
            return Response(serializer.errors, status=400)
        

@api_view(["GET"])
#This is the view function that handles the incoming HTTP GET request. It takes two parameters: request and book_id. The request parameter contains information about the client's request, and book_id is a parameter extracted from the URL, typically used to identify the specific book to retrieve.
def get_book_view(request, book_id):
    try:
    #In this line, the view retrieves a book record from the database using the book_id provided in the URL. It uses the Django Object-Relational Mapping (ORM) to filter the Book model by the id field, which should match the book_id provided in the URL. The first() method is used to get the first matching book if it exists. We removed .first() so that the try except function is able to read the error, otherwise it returns the first occurence of the book which in this case are empty fields
        book = Book.objects.filter(id=book_id).first()
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data)
        else:
            return Response({
            'error': 'Book does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    #This conditional checks if a book with the specified book_id was found in the database. If a book exists, the condition evaluates to True.
    except:
        return Response({
            'error': 'Book does not exist'
        }, status=status.HTTP_404_NOT_FOUND)    
    

@api_view(["GET"])
#This is the view function that handles the incoming HTTP GET request. It takes two parameters: request and book_id. The request parameter contains information about the client's request, and book_id is a parameter extracted from the URL, typically used to identify the specific book to retrieve.
def get_all_books_view(request):
    #In this line, the view retrieves a book record from the database using the book_id provided in the URL. It uses the Django Object-Relational Mapping (ORM) to filter the Book model by the id field, which should match the book_id provided in the URL. The first() method is used to get the first matching book if it exists
    books = Book.objects.all()
    #This conditional checks if a book with the specified book_id was found in the database. If a book exists, the condition evaluates to True.
    if books:
        ##Here, a BookSerializer instance is created, and it's initialized with the book object that was retrieved from the database. The purpose of the serializer is to convert the book object into a serialized format that can be easily rendered as JSON or another content type for the response.
        serializer = BookSerializer(books, many=True)
        #If a book was found and successfully serialized, this line returns a DRF Response object. The response contains the serialized data of the book, which is typically returned to the client as a JSON response. This allows the client to receive detailed information about the book. The HTTP status code of the response will be 200 (OK) by default, indicating a successful GET request.
        return Response(serializer.data)
    

@api_view(["PATCH"])
def update_book_view(request, book_id):    
    book = Book.objects.filter(id=book_id).first()
    if book:
        data = request.data
        #When working with serializers in Django REST framework, make sure to use the partial=True option when updating instances. This allows you to perform partial updates, meaning you can update only the fields that you provide in the request without requiring all fields to be present. This prevents an error when i try updating the book and i do not change the book's unique field, it gives me an error even though i am not changing the unique field of the particular book
        serializer = BookSerializer(book, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    else:
        return Response("Book not found", status=404)
       

@api_view(["DELETE"])
def delete_book_view(request, book_id):
    book = Book.objects.filter(id=book_id).first()
    if book:
        book.delete()
        return Response("Book successfully deleted", status=204)
    else:
        return Response("Book not found", status=404)



#CREATING OUR AUTHENTICATION API VIEW

#This decorator specifies that the view function should only respond to HTTP POST requests
@api_view(['POST'])
def login(request):
    #This line retrieves a user from the database based on the provided username in the request data (meaning your json POST request for postman should have a username key). get_object_or_404 is a helper function provided by Django that retrieves an object from the database and raises a 404 Not Found exception if the object doesn't exist. In this case, it's used to retrieve the user based on the username provided in the request data.
    user = get_object_or_404(User, username=request.data['username'])
    #This condition checks whether the provided password in the request data matches the user's password stored in the database if no error shows up. check_password is a method provided by Django's user model to compare a plaintext password with the hashed password stored in the database. 
    if not user.check_password(request.data['password']):
        #If the passwords don't match, it returns a 404 Not Found response, indicating that the user was not found
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    #    This line generates an authentication token for the user. It uses DRF's Token model to create or retrieve a token associated with the user. The created variable indicates whether a new token was created for the user. If a token already exists, it returns the existing token.
    token, created = Token.objects.get_or_create(user=user)
    #This line creates a serializer for the user instance. UserSerializer is assumed to be a serializer that you've defined for your User model. It's used to convert the user object into a JSON response
    serializer = UserSerializer(instance=user)
    #This line sends a response with the token and user data in JSON format. The token.key attribute provides the generated authentication token key.serializer.data contains the serialized user data.
    return Response({"token": token.key, "user": serializer.data})
    

#from django.views.decorators.csrf import csrf_exempt
@api_view(['POST'])
#@csrf_exempt
def signup(request):
    #This line creates an instance of the UserSerializer to serialize and validate the data received in the request. The UserSerializer is assumed to be a serializer that you've defined for your User model
    serializer = UserSerializer(data=request.data)
    #This condition checks if the serializer's data is valid. If the data is valid, it proceeds to create a new user
    if serializer.is_valid():
        #user_data = serializer.validated_data
        serializer.save()
        #This line retrieves the newly created user from the database based on the username provided in the request data. However, this step seems unnecessary because you've already created the user with serializer.save()
        user = User.objects.get(username=request.data['username'])
        #This line sets the user's password. It's essential to hash the password using Django's built-in password hashing mechanisms.
        user.set_password(request.data['password'])
        #This line saves the user object with the updated password
        user.save()
        #This code generates an authentication token for the newly created user using DRF's Token model.
        token = Token.objects.create(user=user)
        #If the data is valid, the code returns a JSON response with the user's token and serialized user data
        return Response({"token":token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#this function will be responsible for handling GET requests to a specific URL endpoint.
@api_view(['GET'])
#This class is used for session-based authentication, which is common for web applications. This class is used for token-based authentication, often used for RESTful APIs.
@authentication_classes([SessionAuthentication, TokenAuthentication])
#This permission class ensures that only authenticated users (users who have provided valid authentication credentials) are allowed to access the view.
@permission_classes([IsAuthenticated])
#This is the definition of the view function named test_token. It takes a single argument, request, which represents the HTTP request made to this view.
def test_token(request):
    #The {} part is a placeholder for the user's email, which is retrieved from request.user.email. The request.user object represents the currently authenticated user, and request.user.email retrieves the user's email address.
    return Response("passed for {}".format(request.user.email))
