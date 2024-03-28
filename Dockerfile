FROM python:3.8
WORKDIR /app
RUN mkdir -p /to_upload

COPY ./app/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app/
CMD ["./docker-entrypoint.sh"]

