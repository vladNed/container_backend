start:
	- python3 manage.py runserver 0.0.0.0:8000

migrations:
	- python3 manage.py makemigrations
	- python3 manage.py migrate

superuser:
	- python3 manage.py createsuperuser