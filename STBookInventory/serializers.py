#We are going to defines a Django REST framework (DRF) serializer class

#Importing rest_framework from serializers imports the serializers module from the Django REST framework (DRF).The serializers module provides a set of classes and functions that help you serialize and deserialize data in various formats, such as JSON, XML, or other content types, to work with Django models and querysets.
from rest_framework import serializers

#This line imports the Book model from the current package (or directory) where the serializers.py file is located. The dot (.) signifies the current directory. The Book model is likely defined in a models.py file in the same app.
from .models import Book

#Here, a new Python class BookSerializer is defined by us, which inherits from serializers.ModelSerializer.This class is used to create a serializer for the Book model. Serializers in DRF are responsible for converting complex data types, such as Django model instances, into native Python data types that can be rendered into JSON, XML, or other content types. In this case, BookSerializer is tailored for serializing Book model instances.
class BookSerializer(serializers.ModelSerializer):
    #Inside the BookSerializer class, a nested Meta class is defined. This inner class is used to provide metadata about the serializer.
    class Meta:
        #In the Meta class, the model attribute is set to Book. This specifies which Django model the serializer is associated with. In this case, it's associated with the Book model, meaning the serializer will be used to serialize and deserialize Book instances.
        model = Book
        #The fields attribute is a list that specifies which fields from the Book model should be included when serializing an instance of the model. This list is used to determine which attributes of the Book model should be included in the serialized representation. In this example, it includes the id, isbn, title, author, and available_copies fields.
        fields = ['id','isbn','title','author', 'available_copies','user']


from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['email','password', 'account_type']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

# class ResetPasswordEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()