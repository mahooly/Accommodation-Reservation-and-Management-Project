# Official Python image
FROM python:3.7
# create root directory for project, set the working directory and move all files
RUN mkdir /cryptoapp
WORKDIR /cryptoapp
ADD . /cryptoapp
# Web server will listen to this port
EXPOSE 8000
# Install all libraries we saved to requirements.txt file
RUN pip install -r requirements.txt