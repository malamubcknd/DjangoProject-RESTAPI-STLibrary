#Because we want the views webpage to have a forms layout, we import forms and link it to Book Model

from django import forms
from .models import Book  # Import the Book model to work with forms

#We create a class called BookForm
#Its purpose is to represent and handle form data related to the Book model
# The BookForm class itself is a subclass of forms.ModelForm, which means it's a ModelForm.
# ModelForms are a convenient way to create forms that are tied to a specific database model.
# In this case, the BookForm class is associated with the Book model, and it will automatically generate
# form fields based on the model's fields.
class BookForm(forms.ModelForm):
#"class Meta" This inner class within BookForm allows you to specify metadata for the form.   
# The Meta class allows you to configure and customize how the form should behave and interact with 
# the associated model and how it will look like in views site
#There are a lot of customizations you can do llke changing the order of your fileds, excluding fields, help menu, 
#adding widgets and even changing the field names to your choice
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'available_copies']


"""
In a Django web application, the forms.py file serves as a crucial component for managing and handling form-related functionality. Here's why we need forms.py in Django:

    Data Validation: Forms in web applications serve as a way for users to input data. It's important to validate this data to ensure it's accurate and conforms to specific requirements. The forms.py file allows you to define form classes with fields and validation rules. This keeps the validation logic organized and consistent.

    Security: Properly validating user input helps prevent common security vulnerabilities like SQL injection, cross-site scripting (XSS), and cross-site request forgery (CSRF). By using Django forms, you can implement these security measures in a standardized and efficient manner.

    Reusability: Forms defined in forms.py can be reused across multiple views or even in different applications within the same project. This promotes the DRY (Don't Repeat Yourself) principle and reduces code duplication.

    Integration with Models: Django forms can be closely tied to models using ModelForms. This makes it easy to create, update, and validate model instances based on user input. It simplifies the process of working with database records and forms.

    Error Handling: Forms in Django can automatically generate error messages for invalid data, making it easier to present feedback to users and guide them in providing the correct information.

    Rendering HTML Forms: Django forms can generate HTML form elements, making it easier to create consistent and well-structured forms in your templates. You can customize form rendering while maintaining a clean separation between form logic and presentation.

    Complex Data Processing: In some cases, you might need to perform complex data processing when handling user input. Django forms allow you to encapsulate this logic within the form classes.

    Validation Logic Centralization: By placing form validation logic in forms.py, you keep it centralized and separate from your views. This separation of concerns enhances the maintainability and readability of your code.

    Testability: By using Django forms, you can easily write unit tests to ensure that your forms are working as expected. Django provides testing utilities for forms that simplify the testing process.

    Reduced Boilerplate Code: Django forms provide a high-level and declarative way to define form structures and validation rules, reducing the amount of boilerplate code you need to write when working with forms.
"""