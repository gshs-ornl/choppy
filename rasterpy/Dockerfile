FROM python:3.6.9-alpine3.10

LABEL maintainer="Joshua N. Grant <grantjn@ornl.gov>"
LABEL version='0.1.2'
COPY setup.sh /
COPY requirements.txt /

RUN apk update && apk upgrade && \
	apk add --no-cache \
		bash

RUN bash /setup.sh

RUN rm /requirements.txt
RUN rm /setup.sh
