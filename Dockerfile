FROM python:3.11.8-slim-bullseye AS builder
WORKDIR /code
COPY requirements.txt app.py  /code/
COPY scripts/ /code/scripts
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]