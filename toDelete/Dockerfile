from alpine:latest

RUN apk add py3-pip
RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip
RUN apk add build-base

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5500 7000
