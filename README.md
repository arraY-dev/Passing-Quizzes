# Passing-Quizzes

Application Launch Steps:

1. Install all libraries from a file requirements.txt with command "pip install -r requirements.txt".
2. Make migrations and migrate data in database. ("py manage.py makemigrations", after "py manage.py migrate")
3. Dump data to database from users.json file with command "python manage.py loaddata users.json". This file added a supeuser with username admin and password admin.
4. Dump data to database from quizzes.json file with command "python manage.py loaddata tests/fixtures/quizzes.json". This file added two quizzes.
5. With command "py manage.py runserver" run server and in admin panel add Site with domain name and show name http://localhost:8000/
6. In admin panel add Social app for Google or Facebook.
Create a google app to obtain a key and secret through the developer console. 
(https://django-allauth.readthedocs.io/en/latest/providers.html#google).
7. Exit from admin panel, register and pass quizzes.
