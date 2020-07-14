# Passing-Quizzes

Application Launch Steps:

1. Install all libraries from a file requirements.txt
2. Make migrations and migrate.
3. Create superuser.
4. Dump data to database from file with command "python manage.py loaddata accounts/fixtures/initial_data.json"
4. In admin panel add Site with domain name and show name http://localhost:8000/
5. In admin panel add Social app for Google or Facebook.
Create a google app to obtain a key and secret through the developer console. 
(https://django-allauth.readthedocs.io/en/latest/providers.html#google)
6. Exit from admin panel, create user and pass quizzes.
