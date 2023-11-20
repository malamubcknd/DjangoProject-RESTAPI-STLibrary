#Lets reference our custom user model other than django's built-in authentication
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

from django.db import models
from django.utils.translation import gettext as _

# Import the User model if you're using Django's built-in authentication
#from django.contrib.auth.models import User
from django.utils import timezone

#from django.contrib.auth.models import AbstractUser

# Create your models here.

#When adding a book in admin site, these are the five field you will have to fill, namely isbn, title, author, available copies (a drop down) and person (a list of registered users will appear in a drop down, choose one)
class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    available_copies = models.PositiveIntegerField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    #person = models.ForeignKey('User', default=None, on_delete=models.CASCADE)
    #When you submit the book and hit enter, the title of the book will be returned
    def __str__(self):
        return self.title
        
    # Increment is a positive or negative value to increase or decrease available copies. This means you will have a dropdown menu with numbers from -infinity to positive infinity and the difference between each number is 1 (gaps of 1)    
    def update_available_copies(self, increment=1):
        #This will add the new increment value to the available_copies field of that respective book id        
        self.available_copies += increment
        #There will be a save button available        
        self.save()


class BookCheckout(models.Model):
    checkout_date_time = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} checked out {self.book.title} on {self.checkout_date_time}"

    class Meta:
        ordering = ['-checkout_date_time']

#For our command line user creation. This is not a typical django model. This a customised user manager class defined
#This class extends the UserManager class and customizes the behavior of user creation, specifically for creating regular users and superusers (admin users).This class, named CustomUserManager, is intended to customize the creation of user objects. It is a subclass of Django's built-in UserManager class, which provides default methods for creating and managing user accounts
class CustomUserManager(UserManager):
    #This method is a custom implementation for creating a user. It is a "protected" method (denoted by the underscore prefix) and is intended to be used internally within the class. It takes several parameters: self: The reference to the instance of the class. email: The user's email address, a required field. password: The user's password, a required field. **extra_fields: Any additional fields that can be passed during user creation
    def _create_user(self, email, password, **extra_fields):
        #it checks whether the email parameter is provided. If not, it raises a ValueError
        if not email:
            raise ValueError("You have not provided a value e-mail address")
        #It normalizes the email address to ensure consistent formatting
        email = self.normalize_email(email)
        #It creates a new user object using the self.model (which is assumed to be a user model class) with the provided email and any additional fields
        user = self.model(email=email, **extra_fields)
        #It sets the user's password using the set_password method, which securely hashes the password and then we save the user to our database
        user.set_password(password)
        user.save(using=self.db)
        #returns the user object
        return user
    
    #The create_user and create_super methods below are not directly related to command-line commands like python manage.py createuser or interactions with the Django admin website. The admin site often uses the standard User.objects.create() method for user creation
    #This is a wrapper method for creating a regular user. It calls the _create_user method internally and sets default values for the is_staff and is_superuser fields to False
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields) #calls the _create_user method
    
    #Similar to the create_user method, this is a wrapper method for creating a superuser (admin user). It also calls the _create_user method internally but sets default values for is_staff and is_superuser to True
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


#For our Admin interface user creation
#We are using functions from our Custom User Manager Class
#This custom user model extends Django's built-in AbstractBaseUser and PermissionsMixin classes, allowing you to create a user model with customized fields and permissions    
class User(AbstractBaseUser, PermissionsMixin):
    
    class AccountType(models.TextChoices):

        GENERAL_USER = 'General User'
        STAFF_MEMBER = 'Staff Member'
        ADMIN = 'Admin'
    
    #Our fields for User Model are email, name, is_active, is_superuser, is_staff, date_joined, last_login
    email = models.EmailField(blank=True, default='', unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    account_type = models.CharField(_('Account Type'), max_length=100, choices=AccountType.choices, default=AccountType.GENERAL_USER)
    
    #Adding the fields that django depends on(must add since we defined our own custom user model). This determines whether a user registered via REST can log into the admin site
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    #In Django, every model class (a Python class that inherits from django.db.models.Model) includes an automatically created manager called objects by default. This manager is responsible for querying and managing database records for that model. The code snippet objects = CustomUserManager() is replacing the default manager for the model with a custom manager named CustomUserManager. By doing this, you are essentially instructing Django to use your custom manager for database operations related to instances of the model. CustomUserManager is expected to be a custom manager class that you've defined elsewhere in your code. It's used to extend or customize the default behavior of the manager.
    objects = CustomUserManager()

    #We Specify that the email field should be used as the unique identifier for user authentication when filling the username field
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    #A list of additional other fields required for creating a user, though in this case, it's an empty list, indicating that only the email and password are required.
    REQUIRED_FIELDS = []

    #The Meta class is used in Django models to provide additional information about the model class, such as its human-readable name and plural form. This metadata is used by Django for various purposes, including generating user-friendly display names in the admin interface
    class Meta:
        #verbose_name: This attribute is set to 'User', indicating the singular name or label for a single instance of this model. In this case, it specifies that a single instance of this model should be referred to as 'User
        verbose_name = 'User'
        #verbose_name_plural: This attribute is set to 'Users', indicating the plural name or label for multiple instances of this model. It specifies that when referring to multiple instances of this model, they should be called 'Users
        verbose_name_plural = 'Users'

    #This method is defined within the User model and returns the user's full name. It retrieves the value of the name attribute of the user. This method is intended to provide a convenient way to get the user's full name
    def get_full_name(self):
        return self.name
    
    #This method is also defined within the model and returns a shorter name or identifier for the user. It first checks if the name attribute has a value. If it does, it returns the name. If name is empty, it takes the first part of the user's email address before the '@' symbol and returns that as the short name
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
 