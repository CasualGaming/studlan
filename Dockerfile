FROM python:2.7

ENV DIR=/srv/studlan

# Copy project files
COPY . $DIR
WORKDIR $DIR

# Install requirements
RUN pip install -r requirements/production.txt --upgrade

# Add tmp app config with dummy secret key
RUN cp sample-configs/local-empty.py studlan/settings/local.py

# Collect static files
RUN mkdir static
RUN python manage.py collectstatic --noinput --clear

# Remove tmp app config
RUN rm studlan/settings/local.py

# Add app user
RUN useradd -r studlan

EXPOSE 8080

CMD ["/bin/bash", "docker-entrypoint.sh"]
