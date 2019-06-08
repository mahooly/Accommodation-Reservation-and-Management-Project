# Official Python image
FROM python:latest
ENV PYTHONUNBUFFERED 1
# create root directory for project, set the working directory and move all files
RUN mkdir /makanapp
WORKDIR /makanapp
ADD . /makanapp/
# Web server will listen to this port
EXPOSE 8000
# Install all libraries we saved to requirements.txt file
#RUN apt-get -y update
#RUN apt-get -y install python3-dev python3-setuptools
RUN pip install -r requirements.txt
RUN python ./Code/manage.py makemigrations
RUN python ./Code/manage.py migrate --run-syncdb