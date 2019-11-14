FROM tensorflow/tensorflow:2.0.0-py3
#FROM python:3.6.9-slim
ADD . /seniorproject
WORKDIR /seniorproject

# Install deps and spaCy model
RUN apt-get -qq update; apt-get install -y -qq libmysqlclient-dev gcc > /dev/null
RUN python -m pip install -r seniorproject/requirements.txt --default-timeout=600 > /dev/null

EXPOSE 8000
CMD ["gunicorn", "--timeout", "180", "--bind", "0.0.0.0:8000", "--worker-class", "gevent", "--capture-output", "seniorproject.api:API"]