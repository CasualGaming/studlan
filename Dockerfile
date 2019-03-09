FROM python:2.7

ENV DIR=/srv/studlan

# Required files
COPY apps $DIR/apps
COPY files $DIR/files
COPY locale $DIR/locale
COPY requirements $DIR/requirements
COPY studlan $DIR/studlan
COPY templates $DIR/templates
COPY docker-entrypoint.sh $DIR/
COPY manage.py $DIR/
COPY uwsgi.ini $DIR/
RUN mkdir log

# Extra files
COPY CHANGELOG.md $DIR/
COPY CONTRIBUTORS $DIR/
COPY LICENSE.txt $DIR/
COPY MAINTAINERS $DIR/

WORKDIR $DIR

RUN pip install -r requirements/production.txt --upgrade

# HTTP
EXPOSE 8080
# uWSGI
EXPOSE 8081

CMD ["/bin/bash", "docker-entrypoint.sh"]
