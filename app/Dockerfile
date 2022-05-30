FROM python:3.8

RUN python -m pip install --upgrade pip

COPY ./app /app
RUN python -m pip install -r /app/requirements.txt

COPY ./app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app