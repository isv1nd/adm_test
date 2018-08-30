FROM python:3
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

RUN mkdir /code
WORKDIR /code
ADD . /code
RUN pip install -r requirements/service-requirements.txt

CMD docker/start.sh