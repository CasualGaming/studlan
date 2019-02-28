FROM python:2.7

ENV DIR=/srv/studlan

# Copy project files
COPY . $DIR
WORKDIR $DIR

# Install requirements
RUN pip install -r requirements/production.txt --upgrade

# HTTP
EXPOSE 8080
# uWSGI
EXPOSE 8081

CMD ["/bin/bash", "docker-entrypoint.sh"]
