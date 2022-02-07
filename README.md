# Audio-File-Server-Rest-Api

Django Web API that simulates the behavior of an audio file server while using a SQL database.

Postman Collection-https://www.getpostman.com/collections/67999f74528d8ada9c0d

# To Run Development Server

1. cd to development directory
2. mkvirtualenv audio_server
3. mkdir audio_server_sample
4. clone repository to new directory
5. pip install -r requirements.txt
6. Create and update settings with your database credentials
7. python manage.py makemigrations
8. python manage.py migrate
9. python manage.py runserver
10. Use postman collection to test CRUD endpoints