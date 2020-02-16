FROM python:2.7

WORKDIR /srv/studlan

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
COPY VERSION ./

# Install requirements
RUN apt-get update && apt-get install -y gettext && \
    pip install -r requirements/production.txt --upgrade

# Compile translations
COPY setup/local.template.py studlan/settings/local.py
RUN python manage.py compilemessages --locale=nb && \
    rm -f studlan/settings/local.py

# HTTP
EXPOSE 8080
# uWSGI
EXPOSE 8081

CMD ["/bin/bash", "docker-entrypoint.sh"]
