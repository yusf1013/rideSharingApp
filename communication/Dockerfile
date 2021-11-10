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

EXPOSE 5500

CMD ["python3", "communication.py"]
