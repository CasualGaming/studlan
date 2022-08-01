FROM python:2.7

ARG python_requirements=requirements/production.txt

WORKDIR /srv/studlan

# Install requirements
COPY requirements/ requirements/
RUN \
apt-get update && \
apt-get install -y gettext cron && \
rm -rf /var/lib/apt/lists/* && \
python -m pip install --no-cache-dir -r "$python_requirements" --upgrade

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
RUN chmod +x docker-entrypoint.sh

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

CMD ["./docker-entrypoint.sh"]
