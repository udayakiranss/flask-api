#FROM python:3.5
#ENV PYTHONUNBUFFERED 1
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends \
#        libatlas-base-dev gfortran



FROM ubuntu:latest
MAINTAINER Udaya Kiran S S "udaykiranss@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
