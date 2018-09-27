FROM ubuntu:latest

# This docker file assumes a config_production.py file, similar to config.py file but with production variables.
ENV DB_CONFIG ./db_config_production.py
ENV JWT_CONFIG ./jwt_config_production.py

#SO updates and installations
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip 
RUN pip3 install uwsgi

COPY ./ ./app
WORKDIR ./app

# manually update all requirements
RUN pip3 install -r requirements.txt

CMD uwsgi --ini uwsgi.ini

EXPOSE 5000
EXPOSE 80
EXPOSE 443