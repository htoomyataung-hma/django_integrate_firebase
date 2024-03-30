## Description
This pull request adds the boilerplate code to set up a new base API web server using Django REST Framework.

## Changes Made
- Created Virtual Environment For Project(example - virtualenv myenv).
- After created virtual environment, installed a necessary packages(You can install 'requirement.txt' in 'server' folder).(Example - pip install -r requirements.txt)
- Created a new Django project named `myproject`.(example - django-admin startproject myproject .)
- Created a new Django app named `myapp`. (example - python manage.py startapp myapp)
- In this server folder, you can easily run the django server. Before running server, you need to first create virtual environment and installed packages. (After activate virtual environment, You can install 'requirement.txt' in 'server' folder)
- Migrated the database. (example - python manage.py makemigrations). After that, run this migrate for field in database. (example- python manage.py migrate).
- Started the development server. (example- python manage.py runserver)

## Additional Notes
This is a basic setup to get started with building an API web server using Django REST Framework. Further enhancements and functionalities can be added based on project requirements.
