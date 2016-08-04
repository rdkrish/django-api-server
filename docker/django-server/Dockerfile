# django-server
# Build using: docker build -t "django-server:0.0.1" --rm=true --no-cache .
#
# NAME             django-server
# VERSION          0.0.1
# LAST_UPDATED     2016-08-03

FROM     ubuntu:14.04
MAINTAINER Radhakrishna Nayak "nayak.radhakrishna@gmail.com"

RUN  apt-get update \
  && apt-get -y upgrade \
  && apt-get -y install vim
RUN apt-get -y install python-pip python-dev libpq-dev postgresql-contrib
RUN pip install django django_extensions django-debug-toolbar django-autofixture djangorestframework psycopg2
ADD run-server .

EXPOSE 8000

CMD ["sh", "/run-server"]
