FROM python:slim

RUN apt-get update && apt-get install libpq-dev gcc python3-dev musl-dev -y

RUN useradd django    

WORKDIR /home/django

RUN chown django -R /home/django

COPY requirements.txt .

USER django

RUN pip install -r requirements.txt

USER root

COPY django_kc .

RUN pip install gunicorn && \
    chown django -R /home/django

USER django

CMD gunicorn -w 3 -b 0.0.0.0:8000 django_kc.wsgi

