FROM alpine:3.4

MAINTAINER Kristoffer Dalby


ENV LIBRARY_PATH=/lib:/usr/lib
ENV DIR=/srv/app

RUN apk update && \
    apk add postgresql-dev \
        mailcap \
        build-base \
        python-dev \
        py-pip \
        jpeg-dev \
        zlib-dev \
        python \
        linux-headers \
        pcre-dev


WORKDIR $DIR

# Install requirements
COPY ./requirements $DIR/requirements
RUN pip install -r requirements/production.txt --upgrade

# Delete unneeded files.
RUN apk del build-base \
        python-dev

# Copy project files
COPY . $DIR

# Collect static files
RUN mkdir static
RUN cp studlan/settings/example-local.py studlan/settings/local.py
RUN python manage.py collectstatic --noinput --clear
RUN rm studlan/settings/local.py

EXPOSE 8080

ENTRYPOINT ["/srv/app/docker-entrypoint.sh"]
