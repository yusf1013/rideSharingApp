#FROM python:3.8-alpine
#
#RUN  mkdir /app
#WORKDIR /app
#
#ADD requirements.txt /app/requirements.txt
#RUN pip install -r /app/requirements.txt
#
#ADD . /app
#
#EXPOSE 5000
#
#CMD ["python", ".app/app.py"]

from alpine:latest

RUN apk add py3-pip
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip
RUN apk add build-base

WORKDIR /app
COPY requirements.txt /app

#RUN pip3 --no-cache-dir install -r requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app

EXPOSE 8000

CMD ["python3", "app.py"]
