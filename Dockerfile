FROM python:2.7

ENV DIR=/srv/studlan

WORKDIR $DIR

# Required files
COPY apps apps
COPY files files
COPY locale locale
COPY requirements requirements
COPY studlan studlan
COPY templates templates
COPY docker-entrypoint.sh ./
COPY manage.py ./
COPY uwsgi.ini ./
RUN mkdir -p log

# Extra files
COPY CHANGELOG.md $DIR/
COPY CONTRIBUTORS $DIR/
COPY LICENSE.txt $DIR/
COPY MAINTAINERS $DIR/

RUN pip install -r requirements/production.txt --upgrade

# HTTP
EXPOSE 8080
# uWSGI
EXPOSE 8081

CMD ["/bin/bash", "docker-entrypoint.sh"]
