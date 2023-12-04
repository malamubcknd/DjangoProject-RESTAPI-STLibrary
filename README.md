I created a book management REST API in Django for a Library

The functionalities are:
1. Users can add a book or books, Get a single book or all books (pagination feature in place) as well as see the number of books available at any point
2. Every book has a record of the id of the particular user that added the book
3. Only Admins can Delete a book
4. Only Admins and Staff can update a book 
5. Only Admins and Staff can check out a book that is being borrowed
6. Admins and Staff can keep track of who checked out a book and the date and time they checked it out
7. Anytime a user checks out a book the book inventory is updated with the number of books remaining
8. User authentication has been implemented (DRF Token) hence using an API platform like postman is highly recommended
9. I have created different types of user groups (General Users, Staff, Management). Users created are automatically assigned group "General Users"
10. General Users are not be able to delete or update a book On the API view or template view(only create and read)
11. Staff are not be able to delete a book On the API view or template view (only create, read and update)
12. Staff are not be able to edit certain important fields in the admin site
13. Staff are not be able to see certain models (Tokens) in the admin site for security reasons. Only admins can see these tokens
14. Automated docs (yasg/spectacular) have been created for this project.
15. When a user signs up, i return a harshed password and not the actual password
16. I have implement request new token if a user forgets their token and also a reset password feature which is done via the user's mail (Token is sent to the user through mail)


