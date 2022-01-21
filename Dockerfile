FROM python:3.9.5

RUN apt-get update -y && apt-get upgrade -y && \
      apt-get install -y libgl1 p7zip-full

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
      pip install -r /tmp/requirements.txt && \
      rm /tmp/requirements.txt

COPY src/ /tmp/src
RUN set -eux && cd /tmp/src && pip install -e .
