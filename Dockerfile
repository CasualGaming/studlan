FROM alpine:3.4

MAINTAINER Kristoffer Dalby

EXPOSE 8080

ENV DIR=/srv/studlan

RUN apk update
RUN apk add postgresql-dev \
        build-base \
        python-dev \
        py-pip \
        jpeg-dev \
        zlib-dev \
        python \
        linux-headers \
        pcre-dev

ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR $DIR

COPY . $DIR

RUN mkdir static
RUN pip install -r requirements/production.txt --upgrade

RUN python manage.py collectstatic --noinput --clear --link

ENTRYPOINT ["$DIR/docker-entrypoint.sh"]
