FROM python:2.7

WORKDIR /srv/studlan

# Install requirements
COPY requirements/ requirements/
RUN \
apt-get update && \
apt-get install -y gettext && \
rm -rf /var/lib/apt/lists/* && \
python -m pip install --no-cache-dir -r requirements/production.txt --upgrade

# Add app files
COPY studlan studlan
COPY apps apps
COPY files files
COPY templates templates
COPY locale locale
COPY manage.py ./
COPY docker-entrypoint.sh ./
COPY uwsgi.ini ./
RUN mkdir -p log

# Compile translations
COPY setup/local.template.py studlan/settings/local.py
RUN python manage.py compilemessages --locale=nb
RUN rm -f studlan/settings/local.py

# Add misc files
COPY CHANGELOG.md ./
COPY CONTRIBUTORS ./
COPY LICENSE.txt ./
COPY MAINTAINERS ./
COPY VERSION ./

# HTTP
EXPOSE 8080
# uWSGI
EXPOSE 8081

CMD ["/bin/bash", "docker-entrypoint.sh"]
