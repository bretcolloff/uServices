FROM python:3.5

MAINTAINER Bret Colloff <bret.colloff@gmail.com>

RUN pip install uwsgi

# Standard set up Nginx
ENV NGINX_VERSION 1.9.11-1~jessie

ENV HOSTLOC localhost

RUN pip install flask
RUN pip install flask-restful
RUN pip install pika

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
	&& echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base \
	&& rm -rf /var/lib/apt/lists/*
# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log
EXPOSE 80 443
# Finished setting up Nginx

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf
# Copy the modified Nginx conf
COPY nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY app/uwsgi.ini /etc/uwsgi/

ADD https://github.com/kelseyhightower/confd/releases/download/v0.10.0/confd-0.10.0-linux-amd64 /usr/local/bin/confd
ADD buildconfig.sh /buildconfig.sh
RUN chmod +x /usr/local/bin/confd /buildconfig.sh
ADD files/confd /etc/confd

COPY nginx.conf /etc/nginx/conf.d/

COPY ./app /app

CMD ["/buildconfig.sh"]
