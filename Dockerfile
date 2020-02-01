FROM tensorflow/tensorflow:2.0.0-py3
#FROM python:3.6.9-slim

WORKDIR /seniorproject

# Copying over *only* the requriements files and fetching dependencies via pip
# first allows us to use this step as a cache rather than have to re-download
# dependencies with each build.
COPY seniorproject/requirements.txt seniorproject/requirements.txt
COPY seniorproject/recommendation/simpletocompound/requirements.txt seniorproject/recommendation/simpletocompound/requirements.txt
COPY seniorproject/recommendation/simpletocompound/semanticsimilarity/requirements.txt seniorproject/recommendation/simpletocompound/semanticsimilarity/requirements.txt
COPY seniorproject/recommendation/passivetoactive/requirements.txt seniorproject/recommendation/passivetoactive/requirements.txt
COPY seniorproject/recommendation/sentimentreversal/requirements.txt seniorproject/recommendation/sentimentreversal/requirements.txt

# Install deps and spaCy model
RUN apt-get -qq update; apt-get install -y -qq libmysqlclient-dev libssl-dev gcc > /dev/null
RUN python -m pip install -r seniorproject/requirements.txt --default-timeout=600 > /dev/null

COPY . /seniorproject
EXPOSE 8000
CMD ["gunicorn", "--timeout", "180", "--bind", "0.0.0.0:8000", "--worker-class", "gevent", "--capture-output", "seniorproject.api:API"]