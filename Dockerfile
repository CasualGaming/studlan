FROM python:2.7

ENV DIR=/srv/studlan

# Copy project files
COPY . $DIR
WORKDIR $DIR

# Install requirements
RUN pip install -r requirements/production.txt --upgrade

# Add tmp app config with dummy secret key
RUN echo "SECRET_KEY = 'UKf79mPQPRngeH9Qh5ZUegFuiIa68ctkmqiR2aqH8pXEwmL5tUaP37orzA7Gkx4M'" > studlan/settings/local.py

# Collect static files
RUN mkdir static
RUN python manage.py collectstatic --noinput --clear

# Remove tmp app config
RUN rm studlan/settings/local.py

# Add app user
RUN useradd -r studlan

EXPOSE 8080
EXPOSE 8081

CMD ["/bin/bash", "manage/docker-entrypoint.sh"]
