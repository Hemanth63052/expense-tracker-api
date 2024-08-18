FROM python:3.11.8-slim-bullseye AS builder
WORKDIR /code
COPY requirements.txt app.py /scripts /code/
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]