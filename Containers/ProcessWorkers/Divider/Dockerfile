FROM tiangolo/uwsgi-nginx:python3.5

MAINTAINER Bret Colloff <bret.colloff@gmail.com>

RUN pip install flask
RUN pip install flask-restful
RUN pip install pika

COPY nginx.conf /etc/nginx/conf.d/
COPY ./app /app
