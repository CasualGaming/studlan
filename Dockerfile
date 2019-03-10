FROM python:2.7

ENV STUDLAN_DIR=/srv/studlan

WORKDIR $STUDLAN_DIR

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
COPY CHANGELOG.md ./
COPY CONTRIBUTORS ./
COPY LICENSE.txt ./
COPY MAINTAINERS ./

# Install requirements
RUN pip install -r requirements/production.txt --upgrade

# HTTP
EXPOSE 8080
# uWSGI
EXPOSE 8081

CMD ["/bin/bash", "docker-entrypoint.sh"]
