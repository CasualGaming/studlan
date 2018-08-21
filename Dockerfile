FROM python:2.7.15

MAINTAINER Kristoffer Dalby

ENV NAME=studlan

ENV DIR=/srv/app

RUN mkdir $DIR
WORKDIR $DIR

# Install requirements
COPY ./requirements $DIR/requirements
RUN pip install -r requirements/production.txt --upgrade

# Copy project files
COPY . $DIR

# Collect static files
RUN mkdir static
RUN cp studlan/settings/example-local.py studlan/settings/local.py
RUN python manage.py collectstatic --noinput --clear
RUN rm studlan/settings/local.py

EXPOSE 8080
EXPOSE 8081

CMD ["sh", "docker-entrypoint.sh"]
