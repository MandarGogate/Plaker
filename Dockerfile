FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
COPY ./static /static
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -U pip
RUN pip install -r /var/www/requirements.txt
COPY ./ /app
