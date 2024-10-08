FROM python:3.11

RUN apt update -y \
    && apt upgrade -y

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
ENV STATICFILES_HOME=/tmp/staticfiles
RUN mkdir -p $STATICFILES_HOME

WORKDIR $APP_HOME

WORKDIR /usr/src/app

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .