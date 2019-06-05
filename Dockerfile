# Official Python image
FROM python:3.7
ENV PYTHONUNBUFFERED 1
# create root directory for project, set the working directory and move all files
RUN mkdir /makanapp
WORKDIR /makanapp
ADD . /makanapp/
# Web server will listen to this port
EXPOSE 8000
# Install all libraries we saved to requirements.txt file
RUN pip install -r requirements.txt
CMD [ "python ./Code/manage.py test registration" ]
