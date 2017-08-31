FROM python:2
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements-prod.txt /code/
RUN apt-get update && apt-get install --yes --force-yes build-essential python-dev liblzo2-dev liblzma-dev libsqlite3-dev python-tk
RUN pip install numpy matplotlib scipy
RUN pip install -r requirements-prod.txt
RUN pip install git+https://github.com/flowersteam/naminggamesal.git@develop
ADD . /code/
RUN echo "false" > /code/debug.txt
RUN echo
RUN echo [\"*\"] > /code/allowed_hosts.txt
# HACK UGLYYYY
RUN echo "INSTALLED_APPS += ('gunicorn',)" >> /code/main_site/settings.py
RUN echo "STATIC_ROOT = '/static/'" >> /code/main_site/settings.py

RUN python manage.py makemigrations ng && python manage.py migrate
RUN python manage.py collectstatic

# python manage.py runserver 0.0.0.0:8000