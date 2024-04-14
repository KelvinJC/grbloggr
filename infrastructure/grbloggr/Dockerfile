FROM python:3.11.0-alpine

LABEL org.opencontainers.image.authors="name: Kelvin Johnson-Chu, email: ojkelvinchu@gmail.com"


# Set the desired time zone to Nigerian time (West Africa Time)
RUN ln -sf /usr/share/zoneinfo/Africa/Lagos /etc/localtime

# Get dependencies
RUN apk update && apk add python3-dev gcc libc-dev libffi-dev freetype-dev


WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
# RUN pip install gunicorn
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD ./src /app/src
ADD ./infrastructure /app/docker

RUN chmod +x /app/docker/grbloggr/server-entrypoint.sh

# # change owner of all the files to the app user
# RUN chown -R grbloggr_app:grbloggr_app /app

# create the app user
#RUN addgroup -S grbloggr_app && adduser -S grbloggr_app -G grbloggr_app

# # change to the user grbloggr_app
# USER grbloggr_app