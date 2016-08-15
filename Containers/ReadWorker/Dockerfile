FROM tiangolo/uwsgi-nginx:latest

MAINTAINER Bret Colloff <bret.colloff@gmail.com>

RUN pip install flask
RUN pip install flask-restful

COPY nginx.conf /etc/nginx/conf.d/
COPY ./app /app