FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /u-mts

COPY ./requirements.txt /u-mts
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app/__init__.py
ENV STATIC_URL /static
ENV STATIC_PATH /u-mts/app/static

COPY . /u-mts
EXPOSE 5000